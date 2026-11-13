---
tags:
  - decision
status: proposed
created: 2026-11-11
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Phase-dependent planning
---
# Phase-dependent planning

> [!QUESTION] Goal: where does a plan state milestones, a graph of dependencies and a critical path?

The first statement of the method required a graph of 20 to 40 milestones over all projects.

## Decision

Each project bears a [phase](../kernel/objects/phase.md#^phases). Milestones, their graph and the critical path apply to the phases of understanding and of distillation. A project in exploration is planned by questions under time boxes, judged by the information gained.

## Constraints that decide the scope

- **The structure of exploratory work is unknown in advance.** The critical path method presupposes a known network of activities, as the note on the [critical path](../references/critical-path-and-constraints.md) states.
- **The absence of a next step is normal in exploration,** as the [phases of research](../references/research-phases.md) describe.

## Options weighed

- **One graph for all work.** Rejected: the graph becomes stale within weeks, and its critical path gives false precision.
- **No graph at all.** Rejected: in distillation the structure is known, and the graph is the roadmap that the task inventory lacked.

## Consequences

- A project record states its phase, and a transition is recorded at a cycle planning.
- The selection rule uses its unblocking key only where a graph exists. After the second review, the graph serves precedence, unblocking and external latencies, and not a longest path, as the note on [dependency](../kernel/objects/dependency.md#^graph-uses) states.
