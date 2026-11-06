# Gameplay Insights — LILA BLACK Telemetry (10–14 February 2026)

## Scope and interpretation

These findings were calculated from the supplied SQLite import containing **89,104 telemetry records** from **796 matches** across three maps. The source README notes that February 14 is a partial collection day. Counts below describe records present in this extract; they are not automatically equivalent to unique player actions, match outcomes, map popularity, or player-experience quality.

## Insight 1 — The extract is heavily weighted toward Ambrose Valley

- **What caught my eye:** Ambrose Valley contributes most of the telemetry in this five-day extract.
- **Evidence:** Ambrose Valley has **61,013 records (68.5%) across 566 matches**. Lockdown has **21,238 records (23.8%) across 171 matches**. Grand Rift has **6,853 records (7.7%) across 59 matches**.
- **Action:** When comparing maps, normalize metrics by match count and, where appropriate, by match duration or active-player count. Do not compare raw event totals as if each map had equal exposure. Confirm whether this distribution reflects the intended sampling or actual live traffic before using it for prioritization.
- **Metrics affected:** Events per match, player-minutes per map, event rate per match, and map-level sample coverage.
- **Why a level designer should care:** An unnormalized comparison could make Ambrose Valley appear more active simply because it has substantially more observations in this extract.

## Insight 2 — Loot telemetry is also concentrated on Ambrose Valley

- **What caught my eye:** Loot events follow the same uneven map coverage, with most recorded loot events on Ambrose Valley.
- **Evidence:** The extract contains **12,885 Loot records**: **9,955 on Ambrose Valley (77.3%)**, **2,050 on Lockdown (15.9%)**, and **880 on Grand Rift (6.8%)**. These are event counts, not counts of unique loot items or unique players.
- **Action:** Review loot-event rates per match and per player-minute for each map before changing loot placement. If Ambrose Valley remains higher after normalization, inspect its loot routes and compare the spatial distribution with player traffic to identify whether loot is concentrated along common routes or in isolated areas.
- **Metrics affected:** Loot events per match, loot events per player-minute, unique loot pickups per player, and route-to-loot distance (if item identity and player linkage are available).
- **Why a level designer should care:** Loot availability and accessibility influence routing and exploration. Raw counts alone are insufficient to justify moving loot spawns, so normalized rates and spatial review should be the next analysis step.

## Insight 3 — Recorded human-versus-human combat events are too sparse for PvP conclusions

- **What caught my eye:** The event extract contains very few explicitly named human kill/death events compared with bot combat events.
- **Evidence:** There are **3 `Kill` records and 3 `Killed` records** in the entire database (6 records combined). By comparison, there are **2,415 `BotKill` records and 700 `BotKilled` records**. There are also **39 `KilledByStorm` records**. These figures are event-type record counts; the source extract does not establish whether every combat interaction is represented symmetrically or whether event capture is complete.
- **Action:** Do not use this extract alone to tune PvP balance, weapon lethality, or player-versus-player hotspots. Validate the event instrumentation and capture rules with the telemetry owner, then collect a larger or more representative sample of human combat events. In the meantime, bot-combat and storm-death patterns can be explored separately, with their own caveats.
- **Metrics affected:** Human kills per match, human deaths per match, PvP encounters per player-minute, bot kills/deaths per match, and event-capture completeness.
- **Why a level designer should care:** Sparse or incomplete PvP telemetry can lead to incorrect balance and encounter-design decisions if treated as representative evidence.

## Limitations

- The five-day extract is not stated to be a randomized or equally sampled map cohort; map totals must be normalized before comparisons.
- February 14 is a partial day.
- The three `Kill` and three `Killed` records are too few to support broad PvP conclusions.
- These insights are descriptive of the supplied extract. They identify follow-up analyses, not causal explanations.
