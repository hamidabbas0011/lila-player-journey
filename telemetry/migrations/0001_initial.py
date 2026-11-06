# Generated for the LILA BLACK telemetry schema.
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="TelemetryEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("user_id", models.CharField(max_length=80)),
                ("match_id", models.CharField(max_length=100)),
                ("map_id", models.CharField(max_length=40)),
                ("event_type", models.CharField(max_length=32)),
                ("x", models.FloatField()),
                ("y", models.FloatField()),
                ("z", models.FloatField()),
                ("timestamp_ms", models.BigIntegerField(db_index=True)),
                ("date", models.CharField(max_length=20)),
                ("is_bot", models.BooleanField(default=False)),
            ],
            options={"ordering": ["timestamp_ms"]},
        ),
        migrations.AddIndex(model_name="telemetryevent", index=models.Index(fields=["map_id", "date"], name="tel_map_date_idx")),
        migrations.AddIndex(model_name="telemetryevent", index=models.Index(fields=["map_id", "match_id"], name="tel_map_match_idx")),
        migrations.AddIndex(model_name="telemetryevent", index=models.Index(fields=["map_id", "date", "match_id"], name="tel_map_date_match_idx")),
        migrations.AddIndex(model_name="telemetryevent", index=models.Index(fields=["event_type"], name="tel_event_type_idx")),
    ]
