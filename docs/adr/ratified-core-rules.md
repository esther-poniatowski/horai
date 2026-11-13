---
tags:
  - decision
status: accepted
created: 2026-11-13
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Ratified core rules
---
# Ratified core rules

> [!QUESTION] Goal: which rules of the core does the author fix before the first increment of the software, including the amendments of its documentation gate?

## Decision

- **A checkpoint follows any consumed budget.** The [checkpoint](../kernel/objects/appetite.md#^checkpoint) applies to the estimate of a `routine` item as to the appetite of an `exploratory` one, and a renewal of a routine item is a new estimate. Until the decision, the tasks of the item are not candidates of the [selection](../kernel/processes/task-selection.md#^selection-rule).
- **Standing parents are ranked.** The cycle planning ranks each standing parent among the milestones of its stream, and the [worth key](../kernel/processes/task-selection.md#^valuation-key) orders them by that rank.
- **`milestones_per_cycle` is a maximum,** of 3 per active deliverable, as the cycle planning reads it.
- **The ritual durations form one parameter,** `ritual_durations`, keyed by ritual.
- **A task records its week in the field `committed_week`,** whose value identifies the week by the date of the review that opened it.

The amendments drafted for the documentation gate of the first increment are ratified as the notes now state them:

- **Remaining work** is the milestone budget less the time spent since that budget was set, and a task budget is optional ([level records](../specification/milestone-record.md)). The decision entry bears a date for this computation.
- **Selection:** the keys apply lexicographically, a question and a standing parent count as milestones, the task that releases a wait leads within its milestone, and the successor work is zero outside the graph ([selection rule](../kernel/processes/task-selection.md#^selection-rule)).
- **Waiting:** a milestone is shown as waiting when it holds an open waiting task and none of its open tasks can be taken ([waiting](../kernel/objects/external-party.md#^waiting)).
- **Waits:** the task holds the reference, and the tasks of a wait are computed. In the core, `waiting` holds a date of follow-up, and the weekly review always schedules the follow-ups ([party record](../specification/party-record.md)).
- **Task record:** the fields `completed`, `held` and `today` with `main`, and `origin` written only when it is not `chosen` ([task record](../specification/task-record.md)).
- **Commitment state** is computed, and the weekly review re-decides the undone tasks of the ending week ([state rule](../kernel/objects/commitment-state.md#^state-rule)).
- **Orphan rule:** a task of the holding file is archived at the `orphan_cycles`-th cycle planning held since its entry ([orphan rule](../kernel/objects/work-hierarchy.md#^orphan-rule)).
- **Authored fields:** a tool writes one only to transcribe a stated value, to record an observed fact, or to assign a new identifier ([specification](../specification/_index.md#^authored-computed)).
- **Parameters** state their unit and admissible values, and a default of two bounds is an interval ([parameters](../kernel/foundations/parameters.md#^parameter-table)).
- **Bootstrap** installs the core and the options turned on at its second step ([bootstrap](../procedures/bootstrap.md)).

The question of the two documentation entry points is deferred: the Sphinx documentation is left as the template states until the package documentation is written.

## Constraints that decide the rules

- **A remaining work of zero breaks the worth key.** A routine item past its estimate had no remaining work while its work continued, so the ratio of the cost of delay to the remaining work divided by zero.
- **Every candidate must be ordered.** A standing parent bore neither a rank nor a value.

## Options weighed

- **A remainder computed from the calibration.** Rejected: it is undefined until the class holds enough logged items.
- **Standing parents placed after the ranked milestones.** Rejected: the author keeps their order under control, at the cost of one rank per standing parent and per cycle.
- **Four parameters for the rituals, and the field names `week` or `committed_on`.** Rejected in favor of one grouped parameter and an explicit name.

## Consequences

- The weekly review lists the items whose budget, and not only whose appetite, is consumed within the week.
- Under quantified valuation, the standing parents follow the valued milestones, in the order of their ranks.
