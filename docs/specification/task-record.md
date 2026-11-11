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
| `id` | always | authored | an identifier unique in the plan | — |
| `parent` | always, except in the holding file | authored | the identifier of a milestone, a question or a standing parent | [parent rule](../kernel/objects/work-hierarchy.md#^parent-rule) |
| `state` | always | authored | `backlog` · `cycle` · `week` | [commitment states](../kernel/objects/commitment-state.md#^states) |
| `origin` | always | authored | `chosen` · `imposed` · `request` | [origin](../kernel/objects/commitment-state.md#^origin) |
| `budget` | when the parent is selected | authored | a duration; the budgets of the open tasks give the remaining work of the parent | [selection rule](../kernel/processes/task-selection.md#^valuation-key) |
| `today` | set by the daily planning | authored | a mark, on at most `daily_marks` tasks | [daily planning](../procedures/daily-planning.md) |
| `depends_on` | for a local order | authored | identifiers of tasks of the same parent | [dependency](../kernel/objects/dependency.md) |
| `scheduled` | set by the weekly review | authored | a date within the week | [weekly review](../procedures/weekly-review.md) |
| `waiting` | when the task needs an awaited artifact | authored | a reference to a wait | [waiting](../kernel/objects/external-party.md#^waiting) |
| `releases` | option external parties | authored | a mark on a task that starts the latency of a party | [release key](../kernel/processes/task-selection.md#^release-key) |
| `risk` | optional | authored | a mark on the riskiest task of its parent | [selection rule](../kernel/processes/task-selection.md#^selection-rule) |
| `kind` | for a task converted from a request | authored | the kind of the request | [request](../kernel/processes/reactive-work.md#^request) |

The stream, the phase, the class of variance, the deadline, the rank and the value of a task are read from its parent, and are not restated on the task. A task bears no date of deadline: a date that a party relies on is recorded on the level that it concerns.
