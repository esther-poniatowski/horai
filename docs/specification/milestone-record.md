---
tags:
  - specification
  - wip
index: "[Specification](docs/specification/_index.md)"
aliases:
  - Milestone record
  - Deliverable record
  - Level records
---
# Level records

> [!QUESTION] Goal: which fields do the purpose, the deliverable, the milestone and the standing parent state, so that the roadmap, the budgets, the waits and the deadlines can be computed?

## Deadline, at any level

A purpose, a deliverable and a milestone may each bear one deadline, with the same fields. A deadline is recorded only here, on the level that it concerns.

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `deadline.date` | option imposed deadlines | authored, or computed for `resource` | a date | [deadline](../kernel/objects/deadline.md#^deadline) |
| `deadline.kind` | with a deadline | authored | `hard` · `soft` · `resource` | [kinds](../kernel/objects/deadline.md) |
| `deadline.party` | with a deadline | authored | the party that relies on it | [promised dates](../kernel/objects/deadline.md#^promised-date) |
| `deadline.resource` | kind `resource` | authored | the quantity left and its rate of consumption | [particular cases](../kernel/processes/imposed-deadlines.md) |
| `deadline.work`, `demand`, `buffer`, `slack` | with a deadline | computed | durations | [slack](../kernel/objects/deadline.md#^slack) |
| `deadline.buffer_consumed`, `work_done` | with a deadline | computed | fractions | [consumption](../kernel/objects/deadline.md#^buffer-consumption) |

## Purpose

| Field | When it is required | Kind | Values |
| --- | --- | --- | --- |
| `id` | always | authored | an identifier unique in the plan |
| `deadline` | when the purpose bears one | — | as above |

## Deliverable

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `id` | always | authored | an identifier unique in the plan | — |
| `purpose` | always | authored | the identifier of one purpose | [levels](../kernel/objects/work-hierarchy.md#^levels) |
| `phase` | always | authored | `exploration` · `validation` · `delivery` | [phases](../kernel/objects/phase.md#^phases) |
| `status` | always | authored | `active` · `waiting-admission` · `stopped` · `done` | [admission](../kernel/processes/planning-horizons.md#^admission) |
| `principal` | option external parties | authored | the identifier of one party | [principal](../kernel/objects/external-party.md#^principal) |
| `deadline` | when the deliverable bears one | — | as above | — |

## Milestone or question

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `id` | always | authored | an identifier unique in the plan | — |
| `deliverable` | always | authored | the identifier of one deliverable | [hierarchy of work](../kernel/objects/work-hierarchy.md) |
| `stream` | always | authored | a stream of the profile | [streams](../kernel/objects/stream.md#^streams) |
| `kind` | always | authored | `milestone` · `question` | [phases](../kernel/objects/phase.md#^phases) |
| `done` | for a `milestone` | authored | the test that judges completion, or the acceptance by a party | [definition of done](../kernel/objects/milestone.md#^definition-of-done) |
| `variance` | when selected for a cycle | authored, or computed by threshold | `routine` · `exploratory` | [classes of variance](../kernel/objects/appetite.md#^variance-classes) |
| `budget` | when selected for a cycle | authored | a duration: an estimate or an appetite | [appetite](../kernel/objects/appetite.md#^appetite) |
| `consumed`, `remaining` | always | computed | durations, from the logs and the budgets of open tasks | [log record](log-record.md) |
| `overruns` | always | computed | the number of checkpoints passed | [checkpoint](../kernel/objects/appetite.md#^checkpoint) |
| `depends_on` | option milestone graph | authored | identifiers of milestones | [milestone graph](../kernel/objects/dependency.md#^milestone-graph) |
| `successor_work` | option milestone graph | computed | a duration | [unblocking](../kernel/objects/dependency.md#^graph-uses) |
| `supplied_by` | option external parties | authored | a party, for an external dependency | [external dependency](../kernel/objects/dependency.md#^external-dependency) |
| `consumers` | for the role enablement | authored | identifiers of the milestones, or kinds of request, that consume the output | [pull rule](../kernel/processes/enablement.md#^pull-rule) |
| `rank` | valuation ordinal, when selected | authored | an integer within the stream and the cycle | [scales](../kernel/objects/value.md#^scales) |
| `value`, `cost_of_delay` | valuation quantified | authored | amounts in the unit of the profile, each with its basis | [quantities](../kernel/objects/value.md#^quantities) |
| `deadline` | when the milestone bears one | — | as above | — |
| `status` | always | authored | `open` · `done` · `reduced` · `stopped` | [checkpoint decision](../procedures/checkpoint-decision.md) |
| `cycle` | when selected | authored | the identifier of the cycle | [calendar record](calendar-record.md) |

## Standing parent

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `id` | always | authored | an identifier unique in the plan | — |
| `stream` | always | authored | one stream of the regimes `floor`, `calendar`, `batched`, `reactive` or `committed`, or the register of debt of an enablement stream | [standing parent](../kernel/objects/work-hierarchy.md#^standing-parent) |
