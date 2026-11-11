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
| `cycle` | serves a milestone or a question selected for the current cycle | [cycle planning](../../procedures/cycle-planning.md) |
| `week` | committed for the current week | [weekly review](../../procedures/weekly-review.md), or one of the [lateral entries](../processes/planning-horizons.md#^lateral-entries) |

- **The backlog is hidden by default.** No view displays it outside a planning session, which removes the permanent competition among recorded tasks.
- **Priority is derived.** The order of the tasks of a week follows from the [selection rule](../processes/task-selection.md#^selection-rule), so a priority assigned by hand has meaning only within the committed week.
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
