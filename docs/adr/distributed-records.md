---
tags:
  - decision
status: accepted
created: 2026-11-13
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Distributed records
  - Integration with Geonexus
---
# Distributed records

> [!QUESTION] Goal: how do the records of a plan sit beside the projects, artifacts and folders that they concern, so that each one ships its own open tasks?

The research workspace Geonexus holds 39 lists of open actions, one per folder: 858 lines, of which 500 are open. Its lines carry subtasks, dependencies across lists, importance markers set by hand, and due dates, which the records of horai did not admit.

## Decision

- **Placement.** A record of the hierarchy may sit in any folder under the roots that the configuration declares, and horai finds it by its key `_schema`. The records that describe the agent stay in one central folder: the configuration, the profile, the availability, the calendar, the capture files and the logs.
- **Loose actions.** A folder ships its loose actions, such as housekeeping, fixes and one-off steps, in a [standing parent](../kernel/objects/work-hierarchy.md#^standing-parent) of its own, whose file declares its stream and is named by the slug of its title.
- **Steps.** A task may list steps, which record its decomposition. The task stays the unit of selection, of time and of commitment.
- **Dependencies across parents.** A task may depend on any task of the plan, and it is a candidate only once its predecessors are done.
- **Importance and urgency within a parent.** A task may carry an importance. Within its parent, the tasks that the order of dependencies leaves free are ordered by quadrant, after the matrix of Eisenhower: a task is *important* at the levels highest and high, and *urgent* once its scheduled date is reached. Across parents, the keys of the [selection rule](../kernel/processes/task-selection.md#^selection-rule) still decide.
- **Due dates.** An outside term on an action is a deadline on its parent, and an action that alone bears such a term becomes a milestone of its own.

## Constraints that decide the integration

- **A project must remain standalone.** A folder moved elsewhere keeps its own records.
- **A parent of a record is a field, never a path,** as the [record formats](record-formats.md) state, so a record can move without changing its parent.
- **Priority is computed across milestones** by the selection rule, whose deadline key acts as urgency against an outside term, and whose rank acts as importance. An importance set by hand therefore acts only within one parent.

## Options weighed

- **One central folder for every record.** Rejected for the first constraint.
- **Reading the lines of the Tasks plugin.** Rejected: the lines carry no parent, no stream and no budget, and the records of horai are YAML.
- **An Eisenhower matrix across a stream.** Rejected: ordering tasks across milestones interleaves them and delays the completion of each, as the decision on [valuation at the milestone](milestone-level-valuation.md) states.
- **Due dates on tasks.** Rejected: a date that a party relies on is recorded on the level that it concerns.

## Consequences

- The configuration declares the roots under which the records are found, beside the central folder.
- The decision on [record formats](record-formats.md) keeps folders by record type for the central records only.
- The lists of Geonexus migrate area by area, under an amended rule on task tracking of Geonexus, beginning with `lexicon/`.
