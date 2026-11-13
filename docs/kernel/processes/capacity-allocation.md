---
tags:
  - theory
index: "[Processes](docs/kernel/processes/_index.md)"
aliases:
  - Allocation of capacity
  - Forms of capacity
---
# Allocation of capacity

> [!QUESTION] Goal: how is the capacity of a week divided among the streams, so that work of deferred payoff receives its share and unplanned work does not take the rest?

Capacity is allocated to [streams](../objects/stream.md) before any task is selected, by the second [commitment](../foundations/commitments.md#^c-capacity). The divided quantity is the [plannable capacity](../objects/availability.md#^plannable-capacity): the available time less the appointed blocks. The allocation is realized by [blocks](../objects/horizon.md#^block) and [windows](../objects/horizon.md#^window) placed in the calendar, and not by a ranking of tasks.

## Forms of capacity

The [regime](../objects/regime.md) of a stream fixes the form in which it receives capacity, and the comparison by which its hours are checked. A profile states the values, which are [policies](../foundations/parameters.md#^parameter-kinds). ^forms

| Form | Regime | Meaning | Hours are compared as |
| --- | --- | --- | --- |
| Share | `planned` | a fraction of the plannable capacity, placed in the longest blocks at the hours of highest energy | equal to the share, within a tolerance |
| Ceiling | `pulled` | a maximum for the work that blocks nothing | at most the ceiling |
| Floor | `floor` | a minimum, protected by a fixed position in the calendar | at least the floor |
| Slots | `batched` | positions of low energy, and the cool-down | not compared |
| Reserve | `reactive` | windows sized on the logged load | the load against the windows |
| Appointment | `appointed` | blocks fixed by a party, removed beforehand; a share for their preparation, and optionally a maximum of preparation per appointment, stated for the stream and overridable by an appointment | the blocks are not allocated; the preparation equal to its share, and at most the cap of each appointment |

A profile is admissible when the floors, the reserve and the shares fit in the plannable capacity at the low quantile of the [availability](../objects/availability.md). When they do not fit, the profile is revised at the strategic review, and the floors are not reduced to make it fit.

## Rules

- **Floors are protected.** A floor is never traded for time on a `planned` or `pulled` stream. Its suspension is the last [adjustment](../objects/deadline.md#^adjustment-order) under a deadline, and is recorded. While an item is marked [non-negotiable](../foundations/commitments.md#^c-non-negotiable), the floors serve that item. ^floors
- **Blocking tooling is charged to its consumer.** A means that blocks a milestone of the cycle is built under the budget of the consuming milestone, as the [constraint rule](tooling.md#^constraint-rule) requires, and its time counts in the allocation of that stream.
- **Overrun only toward the subordinate stream.** A block may extend into the next block when the work is in flow, only if the next block belongs to the same stream, or the extending stream is `planned` and the next block belongs to a `pulled` stream. A `pulled` stream never extends into another stream, and no stream extends into a floor. ^overrun
- **Estimates are revised from the logs, policies by decision.** A deviation of the hours from a form is a deviation for the strategic review, as the [parameters](../foundations/parameters.md#^policy-not-from-logs) state.
- **Valuation never reduces a floor or the reserve,** by the ninth [commitment](../foundations/commitments.md#^c-valuation).

*Example*: the [research profile](../../profiles/research.md#^shares) states the values of these forms for one domain.
