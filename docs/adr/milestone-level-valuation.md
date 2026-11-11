---
tags:
  - decision
status: accepted
created: 2026-11-11
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Valuation at the milestone
---
# Valuation at the milestone

> [!QUESTION] Goal: at which level is the worth of a result stated and compared, and how is the decision to continue an item judged on worth?

The first statement of the extension ordered tasks by the ratio of the cost of delay of their parent to their duration, and stopped an item when the cost of its whole remainder exceeded the value of the result.

## Decision

- **Worth is stated at the milestone,** as an ordinal rank or as a marginal value and a cost of delay. The selection rule chooses a milestone by the ratio of its cost of delay to its remaining work, then a task within it, as the [selection rule](../kernel/processes/task-selection.md#^valuation-key) states.
- **The stop by value looks one interval ahead,** and compares the expected worth of a renewal with its expected cost in hours, as the [stop by value](../kernel/processes/uncertainty-control.md#^stop-by-value) states.

## Constraints that decide the level

- **Finishing a task stops no cost of delay.** Ordering tasks by an inherited ratio interleaves milestones and delays the completion of each.
- **The task record has no reliable duration,** whereas the remaining work of a milestone is the sum of the budgets of its open tasks.
- **Stopping now is not the only alternative to finishing.** The option of a further checkpoint has value. At $\sigma = 1$, $t = 1$ and $V = 1.5\,\kappa b$, the former rule stops, whereas a renewal of one budget has a positive expected worth of about $0.06\,\kappa b$, a value verified numerically.

## Options weighed

- **The ratio on tasks.** Rejected for the first two constraints.
- **An optimal stopping rule over all future checkpoints.** Not adopted: it requires a model of the whole future, and the one-interval rule captures the main option at a fraction of the cost.

## Consequences

- The ratio becomes a stated heuristic: with precedence and estimated durations, no ordering is guaranteed optimal.
- The value $V$ is the marginal value of the milestone, and the cost of capacity $\kappa$ is authored per cycle.
