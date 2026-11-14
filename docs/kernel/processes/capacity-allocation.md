---
tags:
  - theory
index: "[Processes](docs/kernel/processes/_index.md)"
aliases:
  - Allocation of capacity
  - Forms of capacity
  - Forms of allocation
---
# Allocation of capacity

> [!QUESTION] Goal: how is the capacity of a week divided among the streams, so that work of deferred payoff receives its share and unplanned work does not take the rest?

Capacity is allocated to [streams](../objects/stream.md) before any task is selected, by the second [commitment](../foundations/commitments.md#^c-capacity). The divided quantity is the [plannable capacity](../objects/availability.md#^plannable-capacity): the available time less the appointments and less the reserves. The allocation is realized by [blocks](../objects/horizon.md#^block) and [request windows](../objects/horizon.md#^window) placed in the calendar, and not by a ranking of tasks.

## Allocation of a stream

The allocation of a stream states four independent properties. A profile states their values, which are [policies](../foundations/parameters.md#^parameter-kinds). ^forms

| Property | Values | Meaning |
| --- | --- | --- |
| `mode` | `share` · `reserve` | a share is a fraction of the plannable capacity; a reserve is a duration |
| `bound` | `at_least` · `at_most` · `exact` | the amount is a minimum, a maximum, or a value met within `allocation_tolerance` |
| `amount` | a fraction, or a duration | the fraction of a share, or the duration of a reserve |
| `per` | `day` · `week` · `cycle` · `event`; `week` when absent | the period of the amount; a reserve per event may name in `events` the appointments that it concerns |

The order of computation fixes the base of each share. The appointments and the reserves are removed from the available time first, and the shares divide the remainder.

- **A share fits only time that the agent divides.** Time whose amount a party sets, such as the requests of others, or that one event calls for, such as the preparation of a meeting, is a reserve.
- **A reserve per event counts only for a prepared appointment.** The preparation of an appointment is a task that names it in `prepares` and bears a budget, which is removed from the plannable capacity of the week of the appointment, and held by a block of the stream that the [weekly review](../../procedures/weekly-review.md) adds to that week. A preparation task that states no budget takes the amount of the reserve. An appointment that no task prepares removes no time of preparation.
- **A reserve per cycle is removed from the capacity of the cycle,** and from no single week. It suits episodic work, such as the follow-up of conferences, whose blocks are placed in the calendar of dates.
- **Committed work has time.** A stream that holds an item selected for the cycle, or a task committed for the week, states an allocation, since a stream without one receives no block.
- **The reserve of a stream triggered by arrival is a prior.** The logged load replaces it, as the [reserve](reactive-work.md#^reserve) of reactive work states.

The [trigger](../objects/regime.md) of a stream suggests a usual allocation and does not fix it. `check` rejects only an incoherent combination, such as a share stated as a duration.

| Triggered by | Usual allocation |
| --- | --- |
| `selection` | an exact share, placed in the longest blocks at the hours of high energy |
| `demand` | a share at most, for the work that blocks nothing |
| `calendar` | a share at least, protected by a fixed position in the calendar; a reserve per week at most, for the planning acts |
| `accumulation` | none: positions of low energy, and the cool-down |
| `arrival` | a reserve per day or per week, held by the request windows |
| `appointment` | none for the appointments, which are removed beforehand; a reserve per event at most, for their preparation |

The hours of a stream are compared with its amount according to its bound: at least the amount, at most the amount, or equal to it within `allocation_tolerance`. The hours of a stream without an allocation are not compared, and a reserve per event or per cycle is not compared with the typical week.

A profile is admissible when, at the low quantile of the [availability](../objects/availability.md), the appointments and the reserves leave a plannable capacity, and the minimum and the exact shares sum to at most the whole of it. When they do not fit, the profile is revised at the strategic review, and the minima are not reduced to make it fit.

## Rules

- **Minima are protected.** A minimum is never traded for time on another stream. Its suspension is the last [adjustment](../objects/deadline.md#^adjustment-order) under a deadline, and is recorded. While an item is marked [non-negotiable](../foundations/commitments.md#^c-non-negotiable), the minima serve that item. ^floors
- **Blocking tooling is charged to its consumer.** A means that blocks a milestone of the cycle is built under the budget of the consuming milestone, as the [constraint rule](tooling.md#^constraint-rule) requires, and its time counts in the allocation of that stream.
- **Overrun only toward a stream without a minimum.** A block may extend into the next block when the work is in flow, only if the next block belongs to the same stream, or to a stream without a minimum while the extending stream states one. A stream without a minimum never extends into another stream, and no stream extends into the block of a stream with a minimum, bounded `at_least` or `exact`. ^overrun
- **Estimates are revised from the logs, policies by decision.** A deviation of the hours from an allocation is a deviation for the strategic review, as the [parameters](../foundations/parameters.md#^policy-not-from-logs) state.
- **Worth never reduces a minimum or the reserve,** by the ninth [commitment](../foundations/commitments.md#^c-valuation).

*Example*: the [research profile](../../profiles/research.md#^shares) states the allocations of one domain.
