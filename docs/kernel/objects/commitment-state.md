---
tags:
  - definition
index: "[Objects](docs/kernel/objects/_index.md)"
aliases:
  - Commitment state
  - Backlog
  - Origin of a commitment
---
# Commitment state

> [!QUESTION] Goal: how is a recorded task told from a task committed for a horizon, and a promise chosen by the agent from a promise fixed from outside?

## States

Each task bears one of three **commitment states**. ^states

| State | Meaning | Entered at |
| --- | --- | --- |
| `backlog` | recorded, with no promise | capture |
| `cycle` | serves a milestone or a question selected for the current cycle, or a standing parent | [cycle planning](../../procedures/cycle-planning.md) |
| `week` | committed for the current week | [weekly review](../../procedures/weekly-review.md), or one of the [lateral entries](../processes/planning-horizons.md#^lateral-entries) |

The state of a task is computed from its parent and from the week of its commitment. The task records that week by the date of the weekly review that opened it. ^state-rule

1. A task is in the state `week` when its field `committed_week` bears the date of the review that opened the current week, the latest week of the [calendar record](../../specification/calendar-record.md). A lateral entry bears the same date.
2. Otherwise, a task is in the state `cycle` when its parent is selected for the current cycle, or is a standing parent.
3. Any other task is in the state `backlog`.

- **A week ends at the next review.** A task left undone in the state `week` returns to the state `cycle` or `backlog` when the next weekly review is held, unless that review commits it again.
- **The backlog is hidden by default.** No view displays it outside a planning session, which removes the permanent competition among recorded tasks.
- **Priority is derived.** The order of the tasks of a week follows from the [selection rule](../processes/task-selection.md#^selection-rule), so a priority assigned by hand has meaning only within its parent, as the importance of a task.
- **The task of the day is a mark, not a state.** The [daily planning](../../procedures/daily-planning.md) marks at most `daily_marks` tasks of the week.

## Origin

Each commitment has one of three **origins**. ^origin

| Origin | Fixed by | Enters through |
| --- | --- | --- |
| `chosen` | the agent, at a planning session | the downward planning |
| `imposed` | an [external party](external-party.md), with a result and a date | the [feasibility test](../processes/imposed-deadlines.md) |
| `request` | the conversion of a reactive request that exceeds a window | the [triage](../processes/reactive-work.md#^triage), then the feasibility test when the requester fixes a date |

- **A date is not a commitment, unless a party relies on it.** A date is recorded only as a [deadline](deadline.md), on the level that it concerns. A scheduled date is assigned at the weekly review and nowhere else.
- **An accepted request is a commitment,** with the date that its class of service fixes or that the agent promised.
