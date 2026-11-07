# LILA BLACK - Player Journey Visualization Tool

A web-based telemetry visualization tool for exploring player movement, combat events, loot collection, and activity patterns across LILA BLACK maps.

**Live Application:** https://lila-player-journey-iky1.onrender.com

**GitHub Repository:** https://github.com/hamidabbas0011/lila-player-journey

---

## 1. Project Overview

The Player Journey Visualization Tool helps game designers and analysts understand how players interact with different maps.

It processes gameplay telemetry stored in Parquet files and visualizes player activity on the corresponding minimaps.

The application supports three maps:

- Ambrose Valley
- GrandRift
- Lockdown

The dataset contains five days of telemetry, from February 10 to February 14, 2026.

### Dataset Summary

| Metric | Value |
|---|---:|
| Dataset files | 1,243 |
| Telemetry events imported | 89,104 |
| Unique players | 339 |
| Matches | 796 |
| Maps | 3 |
| Collection period | February 10-14, 2026 |

Note: February 14 is a partial collection day.

---

## 2. Features

### Player Journey Visualization
- Displays player movement paths on the correct minimap.
- Distinguishes human players from bots.
- Supports visibility controls for human players and bots.
- Uses world-coordinate conversion to position telemetry correctly.

### Event Markers
Visualizes important gameplay events:

- Kills
- Deaths
- Bot kills and deaths
- Storm deaths
- Loot pickups

### Filters
- Map selection
- Date selection
- Match selection
- Human player visibility
- Bot visibility
- Event marker visibility

### Visualization Modes
- Player Journeys
- Kill Zones
- Death Zones
- Traffic Heatmap

### Match Playback
- Timeline slider
- Playback controls
- Time-based visualization of player activity

### Dashboard Statistics
Displays:
- Players in view
- Player kills
- Total deaths
- Loot pickups
- Events loaded

---

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development and data processing |
| Django | Web framework and API endpoints |
| SQLite | Local development database |
| PostgreSQL | Production database |
| Pandas | Parquet data processing |
| PyArrow | Parquet file reading |
| HTML | Dashboard structure |
| CSS | Dashboard styling |
| JavaScript | Interactive visualizations |
| HTML Canvas | Rendering player paths and event markers |
| Render | Application hosting |
| GitHub | Version control and source code hosting |

---

## 4. Dataset Structure

The original dataset is organized by date.

```text
player_data/
├── February_10/
├── February_11/
├── February_12/
├── February_13/
└── February_14/
```

Each Parquet file represents one player or bot in one match.

The filename follows this format:

```text
{user_id}_{match_id}.nakama-0
```

Human players are identified by UUID user IDs, while bots use short numeric user IDs.

The telemetry schema includes:

- user_id
- match_id
- map_id
- x
- y
- z
- ts
- event

The `y` coordinate represents elevation. The dashboard uses `x` and `z` for its top-down projection.

---

## 5. Coordinate Mapping

World coordinates are converted into minimap pixel coordinates.

The conversion formula is:

```text
u = (x - origin_x) / scale
v = (z - origin_z) / scale

pixel_x = u * 1024
pixel_y = (1 - v) * 1024
```

Map configuration:

| Map | Scale | Origin X | Origin Z |
|---|---:|---:|---:|
| Ambrose Valley | 900 | -370 | -473 |
| GrandRift | 581 | -290 | -290 |
| Lockdown | 1000 | -500 | -500 |

---

## 6. Local Setup

### Requirements

- Python 3
- pip
- Git

### Clone the repository

```bash
git clone https://github.com/hamidabbas0011/lila-player-journey.git

cd lila-player-journey
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure the dataset

Extract the supplied Parquet dataset into:

```text
data/player_data/
```

The date folders should be directly inside `player_data`.

### Run database migrations

```bash
python manage.py migrate
```

### Import telemetry

```bash
python manage.py load_telemetry
```

### Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 7. Database Configuration

The application uses:

- SQLite for local development.
- PostgreSQL for production deployment on Render.

The production database is configured through the `DATABASE_URL` environment variable.

Database credentials and secret keys must not be committed to GitHub.

---

## 8. Deployment

The application is deployed on Render as a Django Web Service.

The deployment uses:

**Build command**

```bash
./render-build.sh
```

**Start command**

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

Production environment variables:

```text
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<your-secret-key>
DJANGO_ALLOWED_HOSTS=<your-render-hostname>
DATABASE_URL=<your-postgresql-connection-url>
```

The production database is PostgreSQL.

The raw Parquet dataset and local SQLite database are excluded from the Git repository.

---

## 9. API Endpoints

The application exposes endpoints for retrieving filter options and telemetry data.

### Filter API

```text
/api/filters/
```

Supports map and date filtering.

Example:

```text
/api/filters/?map=AmbroseValley&date=all
```

### Telemetry API

```text
/api/telemetry/
```

Supports filtering by map, date, match, and entity visibility.

Example:

```text
/api/telemetry/?map=AmbroseValley&date=all&match=all&humans=1&bots=1
```

The telemetry endpoint limits returned event rows to 60,000 per request to control response size. Summary statistics are calculated separately from the full filtered queryset.

---

## 10. Repository Structure

```text
lila-player-journey/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── telemetry/
│   ├── management/
│   │   └── commands/
│   │       └── load_telemetry.py
│   ├── migrations/
│   ├── static/
│   │   └── telemetry/
│   │       ├── css/
│   │       ├── js/
│   │       └── minimaps/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── ARCHITECTURE.md
├── INSIGHTS.md
├── WALKTHROUGH.md
├── requirements.txt
├── render-build.sh
├── Procfile
└── manage.py
```

---

## 11. Notes and Limitations

- February 14 contains partial telemetry and should be compared carefully against complete collection days.
- The API limits the number of returned event rows per request.
- Player journeys are visualized using the available position telemetry.
- The tool is intended for internal gameplay analysis and level-design exploration.

---

## 12. Links

- Live Dashboard: https://lila-player-journey-iky1.onrender.com
- Source Code: https://github.com/hamidabbas0011/lila-player-journey

