---
tags:
  - decision
status: accepted
created: 2026-11-12
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Ratified commitments
  - Non-negotiable mark
---
# Ratified commitments

> [!QUESTION] Goal: which commitments of the method does the author ratify, and how does the judgment of the agent protect an item that no rule would protect?

## Decision

- **The ten first [commitments](../kernel/foundations/commitments.md) are ratified as stated.**
- **An eleventh commitment is added: one item may claim all the capacity.** By its own judgment, the agent marks at most one task, milestone or question of the plan as [non-negotiable](../kernel/foundations/commitments.md#^c-non-negotiable). Until the item is completed or the mark is removed, it has three properties:
  - every block, floor and window serves it, and its tasks are the only [candidates](../kernel/processes/task-selection.md#^non-negotiable-key) of the selection;
  - it is never stopped by default at a checkpoint, never removed to fit a cycle, and never the first scope cut under a deadline;
  - only an explicit decision of the agent may stop it or reduce its scope.

  Appointed blocks and requests of the class `immediate` keep their time.

## Constraints that decide the mark

- **Some emergencies are known to the agent before any rule.** A submission due in two days may be discovered too late for the feasibility test to place it.
- **A mark on several items stops ranking them.** A single mark keeps its meaning: all the discretionary capacity goes to one result.
- **A party relies on appointed blocks and on immediate requests.** The agent cannot reassign that time alone.

## Options weighed

- **Protection from cuts only, with the order unchanged.** Rejected: the author requires that the marked item receive the resources.
- **First in its stream, on any number of items.** Rejected: the mark stops discriminating when several items bear it.
- **Suspension of appointed blocks as well.** Rejected for the third constraint.

## Consequences

- The mark is a second exception to the [second commitment](../kernel/foundations/commitments.md#^c-capacity), and suspends the floors that the ninth commitment protects from valuation.
- The mark is an authored field of the task record and of the level record, and bears the date at which it was set. The check of a plan reports a second mark as an error.
- The time logged during the mark departs from the shares. A departure that the mark explains is read as such at the weekly review.
- The other decisions of the method keep the status of proposals: ratifying a commitment does not ratify every rule derived from it.
