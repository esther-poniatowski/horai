---
tags:
  - decision
status: proposed
created: 2026-11-11
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Variance classes in place of a Pareto law
---
# Variance classes in place of a Pareto law

> [!QUESTION] Goal: on which work does a fixed budget replace an estimate, and on which argument?

The first statement of the method assumed that durations follow a Pareto law, for which the expected remaining time is $t/(\alpha - 1)$, and concluded that no work can be estimated.

## Decision

Work is assigned to one of two [classes of variance](../kernel/objects/appetite.md#^variance-classes). Work of the class `routine`, named `production` before the second review, is estimated and corrected by the logs. Work of the class `exploratory` receives an appetite and a checkpoint, whose default outcome at the second overrun is the stop.

## Constraints that decide the classes

- **The Pareto assumption has no support for tasks.** Observed ratios of actual to estimated duration are close to log-normal, as the [distributions of duration](../references/duration-distributions.md) report.
- **Under a log-normal law, the conclusion depends on the variance.** The [mean residual life](../kernel/processes/uncertainty-control.md#^mrl) stays near half a budget at $\sigma = 0.5$, and exceeds the budget and grows at $\sigma = 1$.

## Options weighed

- **Appetites on all work.** Rejected: it discards estimates that are reliable for routine work.
- **Estimates on all work, with a buffer.** Rejected: at high variance, no buffer of reasonable size covers the tail.

## Consequences

- Each item selected for a cycle states its class.
- The proportional formula is removed from the method.
- Renewal at a checkpoint requires a justification, since a renewal by default would cancel the control.
