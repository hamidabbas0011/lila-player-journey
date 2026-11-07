# Gameplay Insights - LILA BLACK Player Journey Analysis

## 1. Overview

This document summarizes observations from the supplied LILA BLACK telemetry dataset using the Player Journey Visualization Tool.

The dataset covers February 10-14, 2026, across three maps:

- Ambrose Valley
- GrandRift
- Lockdown

The dataset contains 89,104 imported telemetry events from 1,243 Parquet files.

The dashboard supports analysis of player movement, kills, deaths, loot pickups and traffic patterns.

### Important Data Caveat

February 14 is a partial collection day.

Daily comparisons involving February 14 should therefore be treated cautiously.

The observations below are descriptive. They identify patterns worth investigating and do not establish causation.

---

## 2. Finding One: Loot Collection Is a Major Part of Observed Gameplay Activity

### Evidence

The dashboard's Ambrose Valley, all-dates view reports:

| Metric | Count |
|---|---:|
| Loot pickups | 9,955 |
| Player kills | 1,799 |
| Total deaths | 505 |

Loot pickups are substantially more frequent than recorded kills and deaths in this view.

There are approximately 5.53 loot pickups for every recorded player kill.

### Interpretation

Loot collection represents a significant part of the recorded gameplay activity.

This suggests that loot locations and the routes connecting them deserve attention during map-design analysis.

### Recommendation

- Review the traffic heatmap alongside loot pickup locations.
- Examine whether frequently visited loot areas have multiple viable approaches.
- Investigate whether important loot areas create excessive player concentration.
- Compare loot activity across individual matches before changing loot placement.

### Product Question

Are players being encouraged to explore multiple routes, or are loot locations unintentionally concentrating traffic into a small number of areas?

---

## 3. Finding Two: Player Movement and Combat Activity Should Be Evaluated Together

### Evidence

In the same dashboard view:

| Metric | Count |
|---|---:|
| Players in view | 268 |
| Player kills | 1,799 |
| Total deaths | 505 |

The dashboard displays extensive overlapping player journeys and event markers across the Ambrose Valley minimap.

### Interpretation

Movement patterns alone do not explain how players experience a map.

Combining movement paths with kill and death markers provides more useful context for understanding where player encounters occur.

Areas with overlapping journeys may be worth investigating for combat concentration.

However, overlapping paths alone do not prove that a location is unfair or unbalanced.

### Recommendation

- Compare player journey paths with kill and death zones.
- Identify locations where repeated player encounters occur.
- Inspect individual matches to determine whether the same areas repeatedly produce combat.
- Review visibility, cover, approach routes and escape options in frequently contested areas.

### Product Question

Do high-traffic locations provide enough tactical alternatives, or do they funnel players into predictable encounters?

---

## 4. Finding Three: Bot Activity Should Be Evaluated Separately from Human Player Activity

### Evidence

The dataset contains:

- UUID-based human player identifiers.
- Numeric bot identifiers.
- Separate position event types for human and bot movement.

The visualization tool includes independent visibility controls for human players and bots.

### Interpretation

Combining human and bot movement into a single visualization can make it harder to understand actual player behavior.

Separating these entities allows designers to examine their movement patterns independently.

This is particularly useful when investigating whether bot activity contributes to congestion or influences player encounters.

### Recommendation

- Compare human-only and bot-only traffic heatmaps.
- Examine whether bots repeatedly occupy the same routes as human players.
- Investigate areas where bot activity overlaps with frequent human combat.
- Evaluate bot movement and placement against intended gameplay objectives.

### Product Question

Are bots supporting the intended gameplay experience, or are their movement patterns creating unnecessary congestion in important areas?

---

## 5. Recommended Next Steps

Based on these observations, the following analysis would provide additional value:

| Priority | Action | Expected Value |
|---|---|---|
| High | Compare loot locations with traffic heatmaps | Identify potential loot concentration |
| High | Compare kill/death zones with player journeys | Investigate combat concentration |
| Medium | Separate human and bot movement | Understand entity-specific behavior |
| Medium | Compare individual matches | Distinguish recurring patterns from isolated matches |
| Medium | Exclude or separately analyze February 14 | Avoid misleading daily comparisons |

---

## 6. Conclusion

The telemetry visualization tool provides a way to move beyond isolated gameplay statistics and examine how players move through, interact with and experience the maps.

The strongest next step is to combine movement, loot and combat analysis at the individual match level.

This can help the level-design and gameplay teams identify areas that deserve closer inspection and make more informed decisions about map layout, loot distribution and bot behavior.

