---
tags:
  - theory
index: "[Foundations](docs/kernel/foundations/_index.md)"
aliases:
  - Status of the evidence
  - Review of 2026-11-11
  - Second review of 2026-11-11
---
# Status of the evidence

> [!QUESTION] Goal: which mechanisms of the method rest on tested findings, which on theorems, which on practitioner methodologies, and which on default parameters?

The method was submitted on 2026-11-11 to two adversarial reviews. The first traced each mechanism of the research instance to its source. The second examined the general kernel, its four extensions, its consistency and its overhead, and verified its formulas numerically. The amendments of the second review are recorded in the [architecture decisions](../../adr/_index.md). Four levels of support are distinguished. ^support-levels

- **E, empirical:** a finding of controlled or observational studies supports the principle.
- **M, mathematical:** a theorem supports the rule under stated assumptions, which the situation satisfies.
- **P, practitioner:** an established methodology prescribes the mechanism, without controlled evidence, or a theorem supports it under assumptions that the situation does not satisfy.
- **D, default:** the value has no source and stands until a decision or the logs revise it.

| Mechanism | Source | Level |
| --- | --- | --- |
| Inventory and commitment, hidden backlog | [Kanban](../../references/kanban-and-lean-pull.md) | P |
| Yields and allocation by class | [strategic buckets](../../references/portfolio-and-phase-frameworks.md) | P |
| Milestone graph for precedence and latency | [critical path and constraints](../../references/critical-path-and-constraints.md) | P |
| Pull rule, artifact dependency | [Lean pull](../../references/kanban-and-lean-pull.md) | P |
| Constraint logic for blocking tooling | [theory of constraints](../../references/critical-path-and-constraints.md) | P |
| Appetite, checkpoint, cool-down | [Shape Up](../../references/shape-up.md) | P, anecdotal |
| Unreliable estimates of exploratory work | [distributions of duration](../../references/duration-distributions.md) | E for the bias and the heavy tail |
| Mean residual life of a log-normal law | [control of uncertainty](../processes/uncertainty-control.md#^mrl) | M, verified numerically |
| Phases | [research phases](../../references/research-phases.md), [phase frameworks](../../references/portfolio-and-phase-frameworks.md) | P |
| Fewer switches between kinds of work | [attention and switching](../../references/attention-and-switching.md) | E in the laboratory, extrapolated |
| Cumulative feasibility of deadlines | [earliest deadline first](../../references/critical-path-and-constraints.md) | M for one agent, with estimated work |
| Pooled buffer of a deadline | [critical chain](../../references/critical-path-and-constraints.md) | P |
| Request window sized on a quantile of the load | [queueing](../../references/queueing-and-reactive-work.md) | P; stability ($\rho < 1$) is M |
| Ordering of milestones by cost of delay over remaining work | [cost of delay](../../references/cost-of-delay.md) | P: the theorem assumes known durations and no precedence |
| Stop rule looking one interval ahead | [control of uncertainty](../processes/uncertainty-control.md#^stop-by-value) | P: a myopic rule, not proven optimal |
| Logged verification of delegated output | [AI delegation](../../references/ai-delegation.md) | E for the unreliability of perceived speedup |
| Logged latency of external parties | none | D |
| All [policies](parameters.md#^parameter-table) | none | D |

> [!WARNING] Optimality and generality
> No claim of optimality is defensible: the method has no objective function and no comparative trial. Its generality is conceptual: the profiles other than research are sketches that no use has tested, and the second review found domains, such as the direction of a team, that remain outside the class.
