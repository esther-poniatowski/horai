---
tags:
  - definition
index: "[Objects](docs/kernel/objects/_index.md)"
aliases:
  - Value
  - Cost of delay
  - Valuation
---
# Value

> [!QUESTION] Goal: how is the worth of a result stated, when can it be stated in a unit, and what does a cost of delay measure?

## Two scales

The worth of a result is stated on one of two scales, which a profile declares. Worth is stated at the [milestone](milestone.md), the smallest item whose completion delivers it. ^scales

| Scale | Statement | Use |
| --- | --- | --- |
| Ordinal | a **rank** of each milestone of the cycle within its stream, set at the cycle planning | the last key of the [selection rule](../processes/task-selection.md#^valuation-key) |
| Quantified | amounts in a unit, such as a currency | the three quantities below |

## Quantities

Where the scale is quantified, a milestone can state three quantities. ^quantities

- **Marginal value** $V$: the worth that the completion of the milestone adds to its deliverable. For a milestone without which the deliverable is worthless, $V$ is the value of the deliverable less the remaining cost of its other milestones.
- **Cost of delay** $\gamma$: the value lost per unit of time while the milestone is not done. For a `hard` [deadline](deadline.md), the loss is a step at the date instead of a rate.
- **Cost of capacity** $\kappa$: the cost of one hour of the time of the agent. It is authored per cycle, and may rise as a resource is exhausted, as the shadow price of time does when funds run out.

## Uses

- **Ordering.** Within one stream, milestones are ordered by the ratio of $\gamma$ to their remaining work, as the [selection rule](../processes/task-selection.md#^valuation-key) states. Tasks are then ordered within the chosen milestone.
- **Termination.** At a checkpoint, the expected worth of one more interval is compared with its expected cost, as the [stop by value](../processes/uncertainty-control.md#^stop-by-value) states.
- **Make or obtain.** For an [enablement](../processes/enablement.md), the cost of building a means is compared with the cost of obtaining it from outside.

## Limits

- **Valuation never reduces a floor or the reserve,** by the ninth [commitment](../foundations/commitments.md#^c-valuation). The streams of deferred payoff have a cost of delay that is real and cannot be observed in time, so a comparison in a unit would starve them. Between streams of the regimes `planned` and `pulled`, a quantified comparison may inform a recorded decision at the strategic review.
- **A quantity is an authored judgment.** Each value is stated by the agent with its basis, and its precision is that of the basis.
