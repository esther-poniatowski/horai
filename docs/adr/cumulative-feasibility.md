---
tags:
  - decision
status: accepted
created: 2026-11-11
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Cumulative feasibility of deadlines
---
# Cumulative feasibility of deadlines

> [!QUESTION] Goal: how are several deadlines tested, so that each is not checked against capacity that the others also claim?

The first statement of the extension computed the slack of one deadline against the whole capacity of its stream. Three deadlines in one stream, each needing 60% of it, all passed, although the plan was infeasible.

## Decision

The deadlines are tested together. Sorted by date, the demand of every deadline up to the $k$-th, with its buffer, must fit in the capacity available until the $k$-th date, per stream and then over the plan, as the [slack](../kernel/objects/deadline.md#^slack) and the [feasibility test](../kernel/processes/imposed-deadlines.md#^feasibility-test) state. The demand is planned at the median ratio, and the buffer pools the margin up to the quantile.

## Constraints that decide the test

- **One agent serializes its work.** Its feasibility for a set of deadlines is that of a single resource, for which the cumulative test of earliest-deadline-first scheduling is the exact condition with known work.
- **The margin must be counted once.** The first statement planned at the quantile and added a buffer, which counted the margin twice.
- **A promise must pass the same test as an imposed date,** or the guard against self-set dates leaks through promises.

## Options weighed

- **Per-deadline slack.** Rejected for the first constraint.
- **A full schedule by simulation.** Not adopted: the work is estimated, so the precision of a schedule would be false, and the cumulative test gives the same verdict on feasibility.

## Consequences

- A deadline attaches to any level, and its work is the remaining work below it.
- The kind `resource` is added for a date that follows the consumption of a resource.
- The buffer has a defined consumption, which the selection rule reads.
