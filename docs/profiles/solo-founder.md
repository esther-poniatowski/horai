---
tags:
  - profile
  - wip
index: "[Profiles](docs/profiles/_index.md)"
aliases:
  - Solo founder profile
---
# Solo founder

> [!QUESTION] Goal: which values configure the kernel for the founder of an early company, who builds a product, seeks its market and answers to the funds that remain?

> [!WARNING] Sketch
> This profile tests the generality of the kernel. No use has validated its values.

## Streams

| Stream | Yields | Triggered by | Allocation |
| --- | --- | --- | --- |
| Product | results | `selection` | an exact share |
| Internal tooling | means | `demand` | a share at most |
| Customer and market discovery | knowledge | `calendar` | a share at least, in fixed sessions of interviews |
| Skills | competence | `calendar` | a share at least |
| Investors and partners | coordination | `appointment` | a reserve per event, at most, for each meeting that a task prepares |
| Administration | integrity | `accumulation` | none: the positions of low energy |
| Customer support | coordination | `arrival` | a reserve; kinds outage (`immediate`) and question (`windowed`) |
| Planning | organization | `calendar` | a reserve per week, of at most `PT1H45M` by default |

## Types of deliverable

| Type | Description | Predictability | Starting phase | Stages |
| --- | --- | --- | --- | --- |
| `offer` | tests whether customers want a product | `exploratory` | exploration | interviews · prototype · first sale |
| `release` | delivers a version of the product to its customers | `routine` | validation | build · test · launch |

## Cadences

| Horizon | Solo founder |
| --- | --- |
| Cycle | the cadence of the founder, with the updates to investors as milestones of a stream that yields coordination |

## Enabled mechanisms

| Mechanism | Setting |
| --- | --- |
| Reactive work | on, medium |
| External parties | on: customers (`consumes`, `requests`), contractors (`delegates`), investors (`reviews`) |
| Imposed deadlines | on: the end of the funds is a `hard` deadline on the purpose itself; launches promised to customers are deadlines on deliverables |
| Worth | cardinal: revenue for the value; the worth per hour rises as the funds run out |

## Notes specific to the domain

- **The runway is a hard deadline.** Its date is the funds divided by the burn rate, revised by the agent at each cycle planning. When the test fails, the third [adjustment](../kernel/objects/deadline.md#^adjustment-order) is to cut the burn or raise funds, levers that lie outside the allocation of attention and are recorded as such.
- **The phase governs the tooling.** Tooling built during exploration serves a product that may not be wanted. The [pull rule](../kernel/processes/tooling.md#^pull-rule) admits only the means that an experiment of discovery consumes.
- **Discovery is a minimum, not a phase that ends.** The sessions with customers continue during delivery, since the stream that yields knowledge is the one that building displaces.
- **The stop by value applies fully.** The [checkpoint](../kernel/processes/uncertainty-control.md#^stop-by-value) compares the expected worth of one more interval with its cost at the current worth per hour.
