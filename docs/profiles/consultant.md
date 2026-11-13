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

| Stream | Role | Regime | Capacity |
| --- | --- | --- | --- |
| Engagements sold by result | production | `planned` | share |
| Engagements sold by time | production | `appointed` | blocks agreed with each client |
| Templates and process | tooling | `pulled` | ceiling |
| Market watch | survey | `floor` | floor |
| Upskilling | training | `floor` | floor |
| Proposals and client meetings | exchange | `appointed` | cap per meeting |
| Accounting | upkeep | `batched` | slots |
| Client requests | production | `reactive` | reserve, with the classes of service that each contract states |

## Names

| Kernel | Consultant |
| --- | --- |
| Purpose · deliverable | practice · engagement |
| Exploration · validation · delivery | scoping · proposal · delivery |
| Cycle | the cadence of the consultant, with the steering meetings of each client as milestones of exchange |

## Options

| Option | Setting |
| --- | --- |
| Reactive work | on, medium to heavy |
| External parties | on: each client is the principal of its engagement (`imposes`, `consumes`, `reviews`, `requests`); subcontractors (`delegates`) |
| Imposed deadlines | on, dominant: contractual dates, `hard` where a penalty applies |
| Valuation | quantified: fees for the value, penalties for the cost of delay, the daily rate for the cost of capacity |

## Notes specific to the domain

- **Time sold is not a share.** An engagement sold by time removes its blocks from the [plannable capacity](../kernel/objects/availability.md#^plannable-capacity), and the shares apply to what remains. Within a block, the work of the client is ordered by the selection rule, but no appetite bounds the block, whose length the contract fixes.
- **Several principals.** Each engagement has its own principal, and the agent alone sees the sum of the commitments. The [cumulative test](../kernel/processes/imposed-deadlines.md#^feasibility-test) is therefore run over the whole plan before a new engagement is accepted or a date is promised.
- **The floors have no price.** An hour sold has an observed value and an hour of upskilling has none. The ninth [commitment](../kernel/foundations/commitments.md#^c-valuation) forbids a reduction of the floors on that ground, and the [admissibility of the profile](../specification/profile-record.md) bounds the time that can be sold.
- **Ordering by the ratio.** Among the milestones of client work that no deadline orders, the [ratio of the cost of delay to the remaining work](../kernel/processes/task-selection.md#^valuation-key) decides.
