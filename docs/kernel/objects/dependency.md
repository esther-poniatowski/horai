---
tags:
  - definition
index: "[Objects](docs/kernel/objects/_index.md)"
aliases:
  - Dependency
  - Milestone graph
  - Artifact dependency
---
# Dependency

> [!QUESTION] Goal: on what does a milestone depend, at which grain are dependencies declared, and what does their graph compute for one agent?

## Dependencies between milestones

A dependency is declared between two [milestones](milestone.md). The **milestone graph** is the directed acyclic graph of these dependencies over the deliverables in a structured [phase](phase.md). ^milestone-graph

- The graph is small enough to be drawn on one canvas.
- A dependency between two tasks is kept only as a local order within one milestone.

## What the graph computes for one agent

The critical path method gives the duration of a project whose activities run in parallel. One agent performs its own work in sequence, so the duration of its work is close to the sum of the budgets, plus the external latencies that its own work does not overlap. The graph therefore serves three computations, and not the longest path. ^graph-uses

1. **Precedence.** A milestone is a candidate only when the milestones on which it depends are done.
2. **Unblocking.** The **successor work** of a milestone is the sum of the budgets of the milestones that depend on it, directly or not. Doing first the milestone with the largest successor work keeps the most work available, which is the [unblocking key](../processes/task-selection.md#^selection-rule).
3. **Latest dates of external requests.** An external dependency must be requested early enough for its latency to elapse before the work that needs it, as the [feasibility test](../processes/imposed-deadlines.md#^feasibility-test) computes.

## A milestone depends on an artifact

A milestone depends on an **artifact**, and not on the means that generates it. ^artifact-dependency

The statement "the work is blocked by the missing means" therefore names the wrong dependency. The artifact can be produced by hand, by a means made for the occasion, or obtained from outside, which unblocks the work and reveals what a durable means must do. The rules that follow are stated in the process of [tooling](../processes/tooling.md).

## A milestone can depend on an external party

A dependency whose artifact is supplied by an [external party](external-party.md) is an **external dependency**. It differs from the others on one point: its duration is a latency that the agent does not control. ^external-dependency

In the milestone graph, an external dependency is an edge that bears the expected latency of the party. The rules that follow are stated in the process of [external coordination](../processes/external-coordination.md).
