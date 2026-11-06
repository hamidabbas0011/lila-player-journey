# LILA BLACK — Player Journey Explorer (Django)

A Django-powered internal telemetry explorer for LILA BLACK level designers. This Django application imports the supplied LILA BLACK telemetry into SQLite and provides a browser-based player journey and event explorer.

## Stack

- Python + Django 5.1+
- SQLite for the assessment dataset (89K-ish events)
- Pandas + PyArrow for Parquet ingestion
- Django JSON endpoints
- HTML, CSS and vanilla JavaScript Canvas for the dashboard

## Project layout

```text
lila-django-player-journey/
├── config/                         # Django project settings, URLs, ASGI/WSGI
├── telemetry/
│   ├── management/commands/
│   │   └── load_telemetry.py       # Parquet -> SQLite importer
│   ├── migrations/
│   ├── static/telemetry/
│   │   ├── css/dashboard.css
│   │   ├── js/dashboard.js
│   │   └── minimaps/               # Actual supplied minimap assets
│   ├── templates/telemetry/
│   │   └── dashboard.html
│   ├── models.py
│   ├── urls.py
│   └── views.py                    # Dashboard + JSON APIs
├── data/player_data/               # Place the supplied dataset here (README included)
├── manage.py
└── requirements.txt
```

## Dataset setup

The raw `.nakama-0` Parquet files are intentionally excluded from this source repository. Obtain `player_data.zip` from the assessment materials, extract it so the five `February_*` folders are inside `data/player_data/`, and keep the supplied `data/player_data/README.md` alongside them. Then run the import command below.

## Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt

python manage.py migrate
python manage.py load_telemetry

python manage.py runserver
```

Open http://127.0.0.1:8000/

If PowerShell blocks virtual-environment activation, run the commands from Command Prompt instead:

```bat
.venv\\Scripts\\activate.bat
```

## Run locally (macOS/Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py load_telemetry
python manage.py runserver
```

## Importing data

The importer reads files matching:

`data/player_data/February_*/*.nakama-0`

The source README specifies:
- Each Parquet file represents one player in one match.
- UUID user IDs are humans; numeric IDs are bots.
- `event` is stored as bytes and is decoded to UTF-8.
- `ts` is match-relative elapsed time represented as a timestamp in milliseconds.
- February 14 is a partial collection day.

To replace all previously imported telemetry and reload:

```bash
python manage.py load_telemetry --replace
```

The importer uses Django bulk inserts and database indexes for map/date/match/event queries.

## API endpoints

- `GET /api/filters/?map=AmbroseValley&date=all`
  - Returns available dates and matches for the selected map/date.
- `GET /api/telemetry/?map=AmbroseValley&date=all&match=all&humans=1&bots=1`
  - Returns filtered event rows and summary metrics.
  - Returns all rows matching the selected map/date/match filters. The all-matches view can return a larger payload; select a date or match if browser performance becomes slow.

## Coordinate mapping

The source README defines the world-to-minimap projection:

```text
u = (x - origin_x) / scale
v = (z - origin_z) / scale
canvas_x = u * canvas_width
canvas_y = (1 - v) * canvas_height
```

Map configuration:

| Map | Scale | Origin X | Origin Z |
|---|---:|---:|---:|
| AmbroseValley | 900 | -370 | -473 |
| GrandRift | 581 | -290 | -290 |
| Lockdown | 1000 | -500 | -500 |

Only world X and Z are used for the top-down map; Y is elevation. The provided images have different native dimensions, so the browser draws the image and canvas into the same square stage and applies normalized UV coordinates. Verify known sample points against the minimap before claiming final coordinate accuracy.

## Deployment notes

For a public deployment:
1. Set `DEBUG = False`.
2. Set a strong `SECRET_KEY` via environment variable.
3. Configure `ALLOWED_HOSTS`.
4. Use PostgreSQL for a hosted environment rather than SQLite.
5. Run migrations and `python manage.py load_telemetry` as a one-time release/import step.
6. Run `python manage.py collectstatic`.
7. Serve with Gunicorn, for example `gunicorn config.wsgi:application`.
8. Configure HTTPS and appropriate static-file hosting.

Do not expose this internal telemetry dashboard publicly without access control. Add authentication before sharing a production URL.

## Current scope and known limitations

- Journey lines, kill/death/traffic heatmaps, event markers, human/bot filters, map/date/match filters and timeline playback are implemented.
- Playback is most meaningful with one match selected. “All matches” combines multiple match-relative timelines.
- The API currently returns all rows matching the selected filters. Large all-matches responses may affect browser performance; narrow by date or match if needed.
- Heatmaps use simple spatial bins, not a smoothed kernel-density estimator.
- This repository is a local project scaffold. It has not been deployed or runtime-tested in this environment.

## Hosted deployment configuration

The project includes a `Procfile` for Gunicorn and `render-build.sh` for a Render-style build. Configure these environment variables in the hosting service:

- `DJANGO_SECRET_KEY`: a long, random secret (never commit it).
- `DJANGO_DEBUG`: `False`.
- `DJANGO_ALLOWED_HOSTS`: the assigned hostname, without `https://`.
- `DATABASE_URL`: PostgreSQL connection URL supplied by the host. If omitted, Django uses local SQLite, which is suitable for development but not an ephemeral hosted filesystem.

The source dataset is not bundled into the source repository. For a hosted deployment, arrange a secure one-time data import into the hosted database before opening the dashboard. Do not expose the dashboard publicly without authentication or other access control; the current assessment build has no login gate.
