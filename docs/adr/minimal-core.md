---
tags:
  - decision
status: proposed
created: 2026-11-11
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Minimal core
  - Bounded overhead
---
# Minimal core

> [!QUESTION] Goal: how is the overhead of the method bounded, so that it does not become the sink of attention that it corrects?

The second review counted about 79 fields, 8 stores and 20 constants with all extensions on, and found that the planning acts alone exceeded the stated two hours a week, before logging. A consultant or a developer would spend three to four hours a week on the method.

## Decision

The method is installed as a [minimal core](../kernel/foundations/core-and-options.md#^core), and every further part is an [option](../kernel/foundations/core-and-options.md#^options) turned on when its modulator is present or when a decision lacked it. The durations of the rituals are shortened, and the overhead of the core is budgeted at about 105 minutes a week. The tenth [commitment](../kernel/foundations/commitments.md#^c-core) states the principle.

## Constraints that decide the core

- **The original failure is a sink of attention.** A planning system that absorbs the time owed to the work reproduces it.
- **Most of the overhead is computation.** Percentiles, slacks, buffers and views can be computed by the tool, and the core keeps only what the agent must judge.
- **Options must still be complete.** Each option, once on, keeps all its rules, so that turning it on does not require a redesign.

## Options weighed

- **All extensions on by default.** Rejected for the first constraint.
- **A lighter kernel without extensions.** Rejected: the extensions answer real modulators of other domains.

## Consequences

- Each option declares its fields, its procedure and at most one metric.
- An overrun of the overhead budget over a cycle is a deviation, answered by turning an option off or shortening a ritual.
