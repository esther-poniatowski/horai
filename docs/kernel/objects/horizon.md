---
tags:
  - definition
index: "[Objects](docs/kernel/objects/_index.md)"
aliases:
  - Horizon
  - Cycle
  - Cool-down
  - Block
  - Window
---
# Horizon

> [!QUESTION] Goal: at which time scales are plans stated, and which object does each scale plan?

A **horizon** is a time scale at which a plan is stated and reviewed. Five horizons are nested, and a profile fixes their lengths. ^horizons

| Horizon | Object planned | Limit |
| --- | --- | --- |
| Strategic | the active deliverables, their phases and deadlines | `active_deliverables_max` |
| Cycle | milestones with budgets, questions of explorations | `milestones_per_cycle` per active deliverable |
| Week | committed tasks, blocks, windows, appointed blocks | tasks drawn from the cycle, or entered laterally |
| Day | one main objective, and the other marks | `daily_marks` |
| Block | one stream for one contiguous span of a day | no change of stream within a block |

- **Cycle.** A cycle spans `cycle_length` and ends with a **cool-down**, which receives the debt of the means, the upkeep, the pruning of the holding file and the shaping of the next cycle. Its boundaries follow the dates of the [principal](external-party.md#^principal) when there is one, and the cadence of the agent otherwise. ^cycle
- **Block.** A block assigns one [stream](stream.md) to a contiguous span of a day, of length `block_length`, in place of many short spans, as the decision on [day theming](../../adr/day-theming.md) records. A block of the regime [`appointed`](regime.md#^regimes) has the length that its party fixes, and its preparation is a task of its stream, linked to the appointment that it prepares. When the [availability](availability.md#^slots) is fragmented, blocks become slots of the available length. ^block
- **Window.** A window is a short slot between two blocks, in which the reactive requests are served and the short tasks that [release a wait](../processes/task-selection.md#^release-key) are done, whatever their stream. ^window

The acts that link the horizons are stated in the [planning process](../processes/planning-horizons.md).
