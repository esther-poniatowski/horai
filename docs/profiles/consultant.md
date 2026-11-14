---
tags:
  - profile
  - wip
index: "[Profiles](docs/profiles/_index.md)"
aliases:
  - Consultant profile
---
# Consultant

> [!QUESTION] Goal: which values configure the kernel for an independent consultant, who serves several clients under contractual dates and sells its time at a known price?

> [!WARNING] Sketch
> This profile tests the generality of the kernel. No use has validated its values.

## Streams

| Stream | Yields | Triggered by | Allocation |
| --- | --- | --- | --- |
| Engagements sold by result | results | `selection` | an exact share |
| Engagements sold by time | results | `appointment` | blocks agreed with each client |
| Templates and process | means | `demand` | a share at most |
| Market watch | knowledge | `calendar` | a share at least |
| Upskilling | competence | `calendar` | a share at least |
| Proposals and client meetings | coordination | `appointment` | a reserve per event, at most, for each meeting that a task prepares |
| Accounting | integrity | `accumulation` | none: the positions of low energy |
| Client requests | results | `arrival` | a reserve, with the classes of service that each contract states |
| Planning | organization | `calendar` | a reserve of at most `PT2H30M` per week: the default, raised by the time of the options turned on |

## Types of deliverable

| Type | Description | Predictability | Starting phase | Review latency | Stages |
| --- | --- | --- | --- | --- | --- |
| `proposal` | answers a call for a new engagement | `routine` | delivery | the latency of the client | draft · submission |
| `engagement` | delivers the result that a contract sells | `exploratory` | exploration | the latency of the client | scoping note · deliverable · acceptance |

## Cadences

| Horizon | Consultant |
| --- | --- |
| Cycle | the cadence of the consultant, with the steering meetings of each client as appointments of a stream triggered by appointment |

## Enabled mechanisms

| Mechanism | Setting |
| --- | --- |
| Reactive work | on, medium to heavy |
| External parties | on: each client is the party to whom the agent is accountable for its engagement (`imposes`, `consumes`, `reviews`, `requests`); subcontractors (`delegates`) |
| Imposed deadlines | on, dominant: contractual dates, `hard` where a penalty applies |
| Worth | cardinal: fees for the value, penalties for the cost of delay, the daily rate for the worth per hour |

## Notes specific to the domain

- **Time sold is not a share.** An engagement sold by time removes its blocks from the [plannable capacity](../kernel/objects/availability.md#^plannable-capacity), and the shares apply to what remains. Within a block, the work of the client is ordered by the selection rule, but no appetite bounds the block, whose length the contract fixes.
- **Several parties to whom the agent is accountable.** Each client holds the agent accountable for its own engagement, and the agent alone sees the sum of the commitments. The [cumulative test](../kernel/processes/imposed-deadlines.md#^feasibility-test) is therefore run over the whole plan before a new engagement is accepted or a date is promised.
- **The minimums have no price.** An hour sold has an observed value and an hour of upskilling has none. The ninth [commitment](../kernel/foundations/commitments.md#^c-valuation) forbids a reduction of the minimums on that ground, and the [admissibility of the profile](../specification/profile-record.md) bounds the time that can be sold.
- **Ordering by the ratio.** Among the milestones of client work that no deadline orders, the [ratio of the cost of delay to the remaining work](../kernel/processes/task-selection.md#^valuation-key) decides.
