---
tags:
  - decision
status: accepted
created: 2026-11-11
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Policies and estimates
---
# Policies and estimates

> [!QUESTION] Goal: which parameters may the logs revise, so that the feedback does not ratify the drift that the method exists to prevent?

The first statement of the feedback held that a deviation persisting over a cycle changes a value. Read literally, a floor under-spent for a cycle would be lowered, and the starvation of deferred work would be ratified by the logs.

## Decision

Every number of the kernel is a [parameter](../kernel/foundations/parameters.md) of one of three kinds. An **estimate**, a quantity of the world, is recomputed from the logs at each cycle. A **policy**, a rule of conduct, changes only by a recorded decision at the strategic review. An **authored** quantity is a judgment on one item. A deviation from a policy is recorded as a finding.

## Constraints that decide the split

- **A floor exists because the agent would under-spend it.** A rule that adjusts the floor to the observed spending removes the floor.
- **Estimates must follow the world.** Latencies, ratios and loads change, and a plan that uses stale values fails its tests.
- **Every number must be visible.** The second review found about twenty numbers in the kernel that no profile could override, contrary to the layer test.

## Options weighed

- **All parameters revised from the logs.** Rejected for the first constraint.
- **All parameters fixed by decision.** Rejected for the second.

## Consequences

- The [parameter table](../kernel/foundations/parameters.md#^parameter-table) lists every policy with its default, and the profile record can override each.
- The weekly review records findings, and the strategic review closes them.
- The layer test now forbids a number in the kernel other than a named default.
