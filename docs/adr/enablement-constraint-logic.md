---
tags:
  - decision
status: proposed
created: 2026-11-11
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Constraint logic for tool work
---
# Constraint logic for tool work

> [!QUESTION] Goal: how is the time given to tools bounded, without starving a project that a tool really blocks?

The first statement of the method capped all tool work at 20% of the week.

## Decision

Tool work is divided by its effect on the projects, under the [constraint rule](../kernel/processes/tooling.md#^constraint-rule). A tool that blocks the critical result of a project is driven to a thin slice under an appetite charged to the consuming milestone. The ceiling of the stream T applies to the other tool work. A tool that is a research contribution is planned in the stream P.

## Constraints that decide the rule

- **A flat cap rations the constraint.** Three days of blocking tool work, under a cap of 20%, spread over three weeks during which the project waits. The [theory of constraints](../references/critical-path-and-constraints.md) prescribes the opposite: to exploit the constraint and subordinate the rest to it.
- **The original failure remains.** Tool work without a consumer absorbed whole days, so tool work that blocks nothing still needs a ceiling.
- **Agents shift the cost** from building to verifying and maintaining, as the note on [AI delegation](../references/ai-delegation.md) reports.

## Options weighed

- **Flat cap.** Rejected for the first constraint.
- **No cap, pull rule only.** Rejected: the pull rule bounds the scope of a tool, and not the time spent on tools that block nothing.

## Consequences

- A tool request states whether its consumer is on the critical path.
- The blocking slice has an appetite and a checkpoint, like any exploratory work.
