---
tags:
  - specification
  - wip
index: "[Specification](docs/specification/_index.md)"
aliases:
  - Task record
---
# Task record

> [!QUESTION] Goal: which fields does a task state, so that its commitment and its order follow from the plan?

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `id` | always | authored | the slug of the title, fixed at creation, and unique in the plan | — |
| `title` | always | authored | the title of the task | — |
| `parent` | always, except in the holding file | authored | the identifier of a milestone, a question or a standing parent; in a file, the record that holds the task | [parent rule](../kernel/objects/work-hierarchy.md#^parent-rule) |
| `committed_week` | when the task is committed for a week | authored | the week of its commitment, identified by the date of the weekly review that opened that week | [state rule](../kernel/objects/commitment-state.md#^state-rule) |
| `state` | always | computed | `backlog` · `cycle` · `week` | [state rule](../kernel/objects/commitment-state.md#^state-rule) |
| `origin` | when the task enters the plan as an imposed commitment or a converted request | authored | `chosen` · `imposed` · `request`; `chosen` when absent | [origin](../kernel/objects/commitment-state.md#^origin) |
| `budget` | optional | authored | a duration, by which the tasks of a week are fitted to the capacity of each stream | [weekly review](../procedures/weekly-review.md) |
| `today` | set by the daily planning | authored | the date of the day for which the task is marked, followed by `main` for the main objective; at most `daily_marks` tasks bear the same date | [daily planning](../procedures/daily-planning.md) |
| `completed` | when the task is done | authored | the date of completion | — |
| `held` | in the holding file | authored | the date at which the task entered the holding file | [orphan rule](../kernel/objects/work-hierarchy.md#^orphan-rule) |
| `depends_on` | for an order | authored | identifiers of tasks of the plan, in any parent | [dependency](../kernel/objects/dependency.md) |
| `scheduled` | set by the weekly review | authored | a date within the week; once reached, it makes the task urgent within its parent | [weekly review](../procedures/weekly-review.md) |
| `waiting` | when the task needs an awaited artifact | authored | the date of the follow-up in the core; the identifier of a wait under the option of external parties | [waiting](../kernel/objects/external-party.md#^waiting) |
| `releases` | option external parties | authored | a mark on a task that starts the latency of a party | [release key](../kernel/processes/task-selection.md#^release-key) |
| `prepares` | for a task of a stream of the regime `appointed` | authored | the identifier of the appointment that the task prepares | [appointment](calendar-record.md) |
| `verifies` | option delegation | authored | the identifier of the wait whose delegated output the task reviews | [delegation](../kernel/processes/external-coordination.md#^delegation-acts) |
| `non_negotiable` | optional | authored | the date at which the agent set the mark; at most one item of the plan bears it, and `check` reports a second mark | [non-negotiable key](../kernel/processes/task-selection.md#^non-negotiable-key) |
| `importance` | optional | authored | `highest` · `high` · `medium` · `low` · `lowest`; the first two make the task important within its parent | [selection rule](../kernel/processes/task-selection.md#^selection-rule) |
| `steps` | optional | authored | the decomposition of the task: a list of steps, each with a title and a mark of completion | — |
| `risk` | optional | authored | a mark on the riskiest task of its parent | [selection rule](../kernel/processes/task-selection.md#^selection-rule) |
| `request_kind` | for a task converted from a request | authored | the kind of the request | [request](../kernel/processes/reactive-work.md#^request) |

The stream, the phase, the cycle, the class of variance, the deadline, the rank and the value of a task are read from its parent, and are not restated on the task. A task bears no date of deadline: a date that a party relies on is recorded on the level that it concerns.
