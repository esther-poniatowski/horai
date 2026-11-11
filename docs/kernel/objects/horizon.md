---
tags:
  - definition
index: "[Objects](docs/kernel/objects/_index.md)"
aliases:
  - Horizon
  - Cycle
  - Cool-down
  - Theme
  - Window
---
# Horizon

> [!QUESTION] Goal: at which time scales are plans stated, and which object does each scale plan?

A **horizon** is a time scale at which a plan is stated and reviewed. Five horizons are nested, and a profile fixes their lengths. ^horizons

| Horizon | Object planned | Limit |
| --- | --- | --- |
| Strategic | the active deliverables, their phases and deadlines | `active_deliverables_max` |
| Cycle | milestones with budgets, questions of explorations | `milestones_per_cycle` per active deliverable |
| Week | committed tasks, themes, windows, committed blocks | tasks drawn from the cycle, or entered laterally |
| Day | one main objective, and the other marks | `daily_marks` |
| Theme | one stream for one block | no change of stream within a theme |

- **Cycle.** A cycle spans `cycle_length` and ends with a **cool-down**, which receives the debt of the means, the upkeep, the pruning of the backlog and the shaping of the next cycle. Its boundaries follow the dates of the [principal](external-party.md#^principal) when there is one, and the cadence of the agent otherwise. ^cycle
- **Theme.** A theme assigns one [stream](stream.md) to a block of `theme_length`, in place of short blocks, as the decision on [day theming](../../adr/day-theming.md) records. When the [availability](availability.md#^slots) is fragmented, themes become slots of the available length. ^theme
- **Window.** A window is a short slot between two themes, in which the reactive requests are served and the short tasks that [release a wait](../processes/task-selection.md#^release-key) are done, whatever their stream. ^window

The acts that link the horizons are stated in the [planning process](../processes/planning-horizons.md).
