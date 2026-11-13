---
tags:
  - theory
index: "[Processes](docs/kernel/processes/_index.md)"
aliases:
  - Protection of imposed deadlines
  - Feasibility test
---
# Protection of imposed deadlines

> [!QUESTION] Goal: how are the dates that the agent cannot move tested together for feasibility, and what is adjusted when the test fails?

## Feasibility test

At the acceptance or the proposal of a [deadline](../objects/deadline.md), and at each cycle planning, the [cumulative slack](../objects/deadline.md#^slack) is computed for every deadline of the plan, in two passes. ^feasibility-test

1. **Per stream.** The deadlines whose work lies in one stream are tested against the capacity of that stream.
2. **Over the plan.** All deadlines are tested together against the capacity of all streams of the regimes `planned` and `pulled`.

A deadline whose work spans several streams enters the pass of each stream with the part of its work that lies there. A failure in the first pass with success in the second is resolved by the second adjustment, the transfer of capacity. A failure in the second pass requires the first, the third or the fourth adjustment.

## Outcomes

| Condition, for every $k$ | Outcome |
| --- | --- |
| $s_k \ge 0$ | accepted |
| $s_k < 0$, but $C(D_k) \ge \sum_{j \le k} W_j$ | accepted with a warning: the buffers are partly unfunded |
| $C(D_k) < \sum_{j \le k} W_j$ | the [adjustments](../objects/deadline.md#^adjustment-order) are opened |

Each adjustment is recorded with what it displaces, so that the cost of the deadline is visible. ^recorded-adjustment

## Particular cases

- **Exploration gives no estimate.** A deliverable in [exploration](../objects/phase.md) has no estimate of its remaining work. Its demand is the appetite of its exploration, and the plan states the date at which it must have left that phase. The test reports the deadline as a risk until then.
- **A deadline set by a resource is re-estimated.** The exhaustion of a resource, such as funds, is a `hard` deadline. The agent re-estimates its date, which no party can move, at each cycle planning, from the quantity left and its rate of consumption.
- **External dependencies give latest dates.** The [latest date of each request](external-coordination.md#^three-acts) is computed with the test, and a request whose latest date has passed opens its fallback.

## Guards

- **Only dates that the agent cannot move alone are deadlines.** A date set for oneself [is not one](../objects/deadline.md#^no-self-deadline), which prevents the inflation of dates that the [diagnosis](../foundations/diagnosis.md) describes. A date proposed to a party passes the test first.
- **A deadline does not cancel a checkpoint.** An exploratory item under a deadline keeps its appetite, which is part of the demand that the test checks.
- **Repeated suspension of the floors is a deviation.** It shows that the commitments accepted exceed the capacity, which the [admission](planning-horizons.md#^admission) corrects.

The steps are given in the [procedure for a deadline](../../procedures/deadline-feasibility.md).
