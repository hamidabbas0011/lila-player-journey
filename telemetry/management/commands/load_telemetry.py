from pathlib import Path
import re
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from telemetry.models import TelemetryEvent

UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
REQUIRED = {"user_id", "match_id", "map_id", "x", "y", "z", "ts", "event"}

class Command(BaseCommand):
    help = "Import LILA BLACK Parquet telemetry files into the Django database."

    def add_arguments(self, parser):
        parser.add_argument("--replace", action="store_true", help="Delete existing telemetry before importing.")
        parser.add_argument("--batch-size", type=int, default=2000)

    def handle(self, *args, **options):
        base = Path(__file__).resolve().parents[3] / "data" / "player_data"
        if not base.exists():
            raise CommandError(f"Dataset folder not found: {base}")
        paths = sorted(p for p in base.glob("February_*/*") if p.is_file() and p.suffix == ".nakama-0")
        if not paths:
            raise CommandError(f"No .nakama-0 Parquet files found under {base}")
        if options["replace"]:
            TelemetryEvent.objects.all().delete()
        batch_size = options["batch_size"]
        pending, total, skipped = [], 0, 0

        for i, path in enumerate(paths, 1):
            try:
                frame = pd.read_parquet(path)
                if frame.empty:
                    continue
                missing = REQUIRED - set(frame.columns)
                if missing:
                    raise ValueError(f"missing columns: {', '.join(sorted(missing))}")
                frame["event"] = frame["event"].map(
                    lambda value: value.decode("utf-8", errors="replace") if isinstance(value, bytes) else str(value)
                )
                # The source README defines UUID user IDs as humans and numeric IDs as bots.
                frame["user_id"] = frame["user_id"].astype(str)
                frame["is_bot"] = ~frame["user_id"].str.match(UUID_RE)
                date_label = path.parent.name.replace("_", " ")
                frame = frame.dropna(subset=["x", "z", "ts"])
                for row in frame.itertuples(index=False):
                    raw_ts = getattr(row, "ts")
                    # Parquet exposes ts as a pandas/Python datetime representing match elapsed time.
                    if hasattr(raw_ts, "value"):
                        ts_ms = int(raw_ts.value // 1_000_000)
                    elif hasattr(raw_ts, "timestamp"):
                        ts_ms = int(raw_ts.timestamp() * 1000)
                    else:
                        ts_ms = int(raw_ts)
                    pending.append(TelemetryEvent(
                        user_id=str(row.user_id),
                        match_id=str(row.match_id),
                        map_id=str(row.map_id),
                        event_type=str(row.event),
                        x=float(row.x),
                        y=float(row.y) if pd.notna(row.y) else 0.0,
                        z=float(row.z),
                        timestamp_ms=ts_ms,
                        date=date_label,
                        is_bot=bool(row.is_bot),
                    ))
                    if len(pending) >= batch_size:
                        TelemetryEvent.objects.bulk_create(pending, batch_size=batch_size)
                        total += len(pending)
                        pending.clear()
                if i % 100 == 0:
                    self.stdout.write(f"Read {i}/{len(paths)} files...")
            except Exception as exc:
                skipped += 1
                self.stderr.write(f"Skipped {path.name}: {exc}")

        if pending:
            TelemetryEvent.objects.bulk_create(pending, batch_size=batch_size)
            total += len(pending)
        self.stdout.write(self.style.SUCCESS(
            f"Import complete. Inserted {total:,} events from {len(paths)-skipped:,}/{len(paths):,} files; skipped {skipped}."
        ))
        self.stdout.write(f"Database now contains {TelemetryEvent.objects.count():,} telemetry events.")
