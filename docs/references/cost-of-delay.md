---
tags:
  - reference
index: "[References](docs/references/_index.md)"
aliases:
  - Cost of delay
  - Weighted shortest job first
  - Smith's rule
---
# Cost of delay

## Concept

The **cost of delay** of an item is the value lost per unit of time while the item is not delivered. Reinertsen makes it the central quantity of the economics of product development, and orders a queue by the cost of delay divided by the duration, a rule known as *weighted shortest job first* [reinertsen2009].

## Result

The rule is a theorem of scheduling due to Smith [smith1956]. For one server and $n$ items of known durations $d_j$ and weights $\gamma_j$, with no precedence and all items available at the start, the order of decreasing $\gamma_j / d_j$ minimizes $\sum_j \gamma_j C_j$, where $C_j$ is the completion time of item $j$.

*Proof sketch*: exchanging two adjacent items $i$ and $j$ changes the total by $\gamma_j d_i - \gamma_i d_j$, which is negative exactly when $\gamma_j/d_j > \gamma_i/d_i$, so any order that violates the rule is improved by an exchange.

The assumptions matter: with items that arrive over time, or with a cost that is not linear in the delay, the rule is no longer optimal in general. With precedence constraints, the problem is strongly NP-hard [lawler1978], and Sidney's decomposition orders the sets of jobs closed under precedence by their ratio, as a principled extension [sidney1975].

## Bearing on `horai`

- The last key of the [selection rule](../kernel/processes/task-selection.md#^valuation-key) applies the ratio to milestones, with their remaining work as the duration, since completing a task stops no cost of delay. Precedence is handled by the filter of candidates, so the composition is a heuristic.
- The result concerns one queue. It gives no ground for comparing streams, which the ninth [commitment](../kernel/foundations/commitments.md#^c-valuation) excludes.
- The durations of exploratory items are not known. The rule is then applied with budgets in place of durations, and its optimality is lost.

## Sources

- [reinertsen2009] ○ Reinertsen, *The Principles of Product Development Flow: Second Generation Lean Product Development*, Celeritas, 2009
- [smith1956] ○ Smith, "Various optimizers for single-stage production", *Naval Research Logistics Quarterly*, 3, 1956, pp. 59–66
- [lawler1978] ○ Lawler, "Sequencing jobs to minimize total weighted completion time subject to precedence constraints", *Annals of Discrete Mathematics*, 2, 1978, pp. 75–90
- [sidney1975] ○ Sidney, "Decomposition algorithms for single-machine sequencing with precedence relations and deferral costs", *Operations Research*, 23(2), 1975, pp. 283–298
