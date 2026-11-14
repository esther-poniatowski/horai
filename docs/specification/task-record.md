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
| `parent` | for a task of a milestone or a question | authored | in a file, the milestone or the question that holds the task | [parent rule](../kernel/objects/work-hierarchy.md#^parent-rule) |
| `stream` | for a loose task | authored | the stream of a task that serves no milestone, held in a task list | [loose tasks](../adr/streams-allocation-and-loose-tasks.md) |
| `committed_week` | when the task is committed for a week | authored | the date of the weekly review that committed the task, as the [review log](log-record.md) records it; absent on a recurring task | [state rule](../kernel/objects/commitment-state.md#^state-rule) |
| `state` | always | computed | `backlog` · `cycle` · `week` | [state rule](../kernel/objects/commitment-state.md#^state-rule) |
| `origin` | when the task enters the plan as an imposed commitment or a converted request | authored | `chosen` · `imposed` · `request`; `chosen` when absent | [origin](../kernel/objects/commitment-state.md#^origin) |
| `budget` | optional | authored | a duration, by which the tasks of a week are fitted to the capacity of each stream | [weekly review](../procedures/weekly-review.md) |
| `marked_for` | set by the daily planning | authored | the date of the day for which the task is marked; at most `daily_marks` tasks bear the same date | [daily planning](../procedures/daily-planning.md) |
| `main_objective` | set by the daily planning | authored | a mark on the one task marked for a day that is its main objective | [daily planning](../procedures/daily-planning.md) |
| `completed` | when the task is done | authored | the date of completion; for a recurring task, the date of its last completion | — |
| `recurs` | for a recurring loose task | authored | its rule of recurrence: a default rule, `daily` · `weekly` · `cycle`, a rule named in the `recurrences` of the profile, or a period such as `P2W` or `P2C`, counting days (D), weeks of commitment (W), months (M) or cycles (C); the task is always in the state `week`, and is open again once that many periods have begun since its last completion | [recurrence rules](../adr/strategic-review-and-recurrence-rules.md) |
| `held_since` | in the holding file | authored | the date at which the task entered the holding file | [orphan rule](../kernel/objects/work-hierarchy.md#^orphan-rule) |
| `depends_on` | for an order | authored | identifiers of tasks of the plan, in any parent | [dependency](../kernel/objects/dependency.md) |
| `scheduled` | set by the weekly review | authored | a date within the week; once reached, it makes the task urgent within its parent | [weekly review](../procedures/weekly-review.md) |
| `follow_up` | when the task needs an awaited artifact | authored | the date at which the awaited party is reminded | [waiting](../kernel/objects/external-party.md#^waiting) |
| `awaits` | option external parties | authored | the identifier of the wait that blocks the task | [waiting](../kernel/objects/external-party.md#^waiting) |
| `hands_off` | option external parties | authored | a mark on a task whose completion starts the latency of a party | [key of the hand-off](../kernel/processes/task-selection.md#^release-key) |
| `prepares` | for the preparation of an appointment | authored | the identifier of the appointment that the task prepares, recurring or dated | [calendar record](calendar-record.md) |
| `verifies` | option delegation | authored | the identifier of the wait whose delegated output the task reviews | [delegation](../kernel/processes/external-coordination.md#^delegation-acts) |
| `non_negotiable` | optional | authored | the date at which the agent set the mark; at most one item of the plan bears it; `check` reports a second mark, and a mark left on a closed item or a completed task | [non-negotiable key](../kernel/processes/task-selection.md#^non-negotiable-key) |
| `importance` | optional | authored | `highest` · `high` · `medium` · `low` · `lowest`; the first two make the task important within its parent | [selection rule](../kernel/processes/task-selection.md#^selection-rule) |
| `steps` | optional | authored | the decomposition of the task: a list of steps, each with a title and a mark of completion | — |
| `riskiest` | optional | authored | a mark on the riskiest task of its parent | [selection rule](../kernel/processes/task-selection.md#^selection-rule) |
| `request_kind` | for a task converted from a request | authored | the kind of the request | [request](../kernel/processes/reactive-work.md#^request) |

The stream, the phase, the cycle, the predictability, the deadline, the rank and the worth of a task of a milestone or a question are read from its parent, and are not restated on the task. A loose task names only its stream; within a block of that stream, an important and urgent loose task precedes the milestones, and the other loose tasks follow them. A task bears no date of deadline: a date that a party relies on is recorded on the level that it concerns.
