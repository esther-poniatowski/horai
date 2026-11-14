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

> [!QUESTION] Goal: which fields do the purpose, the deliverable, the milestone and the question state, so that the roadmap, the budgets, the waits and the deadlines can be computed?

## Deadline, at any level

A purpose, a deliverable and a milestone may each bear one deadline, with the same fields. A deadline is recorded only here, on the level that it concerns.

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `deadline.date` | option imposed deadlines | authored | a date | [deadline](../kernel/objects/deadline.md#^deadline) |
| `deadline.strictness` | with a deadline | authored | `hard` when missing the date loses the result, `soft` when its value only decays | [kinds](../kernel/objects/deadline.md) |
| `deadline.party` | with a deadline | authored | the party that relies on it: a declared party by its identifier, or an occasional one by `{name: ...}` | [promised dates](../kernel/objects/deadline.md#^promised-date) |
| `deadline.work`, `demand`, `buffer`, `slack` | with a deadline | computed | durations | [slack](../kernel/objects/deadline.md#^slack) |
| `deadline.buffer_consumed`, `work_done` | with a deadline | computed | fractions | [consumption](../kernel/objects/deadline.md#^buffer-consumption) |

## Purpose

| Field | When it is required | Kind | Values |
| --- | --- | --- | --- |
| `id` | always | authored | the slug of the title, fixed at creation and unique in the plan; it names the file of the record |
| `title` | always | authored | the title, from which the identifier is formed |
| `description` | optional | authored | a statement of the purpose for the reader, which no rule reads |
| `deadline` | when the purpose bears one | — | as above |

## Deliverable

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `id` | always | authored | the slug of the title, fixed at creation and unique in the plan; it names the file of the record | — |
| `title` | always | authored | the title, from which the identifier is formed | [file layout](file-layout.md) |
| `purpose` | always | authored | the identifier of one purpose | [levels](../kernel/objects/work-hierarchy.md#^levels) |
| `type` | always | authored | the identifier of a type of deliverable of the profile, which supplies the defaults below | [profile record](profile-record.md) |
| `phase` | when the deliverable has left its starting phase | authored | `exploration` · `validation` · `delivery`; the starting phase of the type when absent | [phases](../kernel/objects/phase.md#^phases) |
| `stages` | optional | authored | the stages of the deliverable, in place of those of its type, in the form of the profile | [profile record](profile-record.md) |
| `status` | always | authored | `active` · `awaiting-admission` · `stopped` · `done` | [admission](../kernel/processes/planning-horizons.md#^admission) |
| `accountable_to` | option external parties | authored | the identifier of the party to whom the agent answers for the deliverable | [accountability](../kernel/objects/external-party.md#^principal) |
| `derived_from` | for a deliverable that presents another | authored | the identifier of the deliverable that it presents, such as the article of a talk, itself derived from none; the two share one place under `active_deliverables_max` | [derived deliverables](../adr/parties-and-derived-deliverables.md) |
| `deadline` | when the deliverable bears one | — | as above | — |

## Milestone or question


| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `id` | always | authored | the slug of the title, fixed at creation and unique in the plan; it names the file of the record | — |
| `title` | always | authored | the title, from which the identifier is formed | [file layout](file-layout.md) |
| `deliverable` | unless the milestone serves its stream directly | authored | the identifier of one deliverable; a milestone without one, such as the follow-up of an event, serves its stream and closes by its `done_when` | [hierarchy of work](../kernel/objects/work-hierarchy.md) |
| `stream` | always | authored | a stream of the profile | [streams](../kernel/objects/stream.md#^streams) |
| `done_when` | for a milestone | authored | the test that judges completion, or the acceptance by a party | [definition of done](../kernel/objects/milestone.md#^definition-of-done) |
| `stage` | for the milestone of a stage | authored | the identifier of the stage of its deliverable that the milestone holds; the milestone is then named `<deliverable>-<stage>` | [request windows and stages](../adr/request-windows-and-stages.md) |
| `predictability` | when selected for a cycle | authored, or computed by threshold | `routine` · `exploratory` | [classes of predictability](../kernel/objects/appetite.md#^variance-classes) |
| `budget` | when selected for a cycle | authored, or computed from `estimate` | a duration: an estimate or an appetite | [appetite](../kernel/objects/appetite.md#^appetite) |
| `estimate` | optional, for a routine item without `budget` | authored | three durations, `optimistic`, `probable` and `pessimistic`; the budget is their PERT value, $(T_{opt} + 4\,T_{prob} + T_{pess})/6$ | [buffer](../kernel/objects/deadline.md#^buffer) |
| `consumed` | always | computed | a duration: the time spent on the item and on its tasks, computed from the clock entries | [log record](log-record.md) |
| `remaining` | with a budget | computed | a duration: the budget less the time consumed since the budget was set, and zero once the budget is consumed. The budget was set at the start of the cycle that the item records, or at the date of its last decision entry that renewed or reduced it. An item carried into a new cycle without such a decision keeps counting from its earlier budget, and `check` reports it | [worth key](../kernel/processes/task-selection.md#^valuation-key) |
| `overruns` | always | computed | the number of checkpoints passed | [checkpoint](../kernel/objects/appetite.md#^checkpoint) |
| `depends_on` | option milestone graph | authored | identifiers of milestones | [milestone graph](../kernel/objects/dependency.md#^milestone-graph) |
| `successor_work` | option milestone graph | computed | a duration | [unblocking](../kernel/objects/dependency.md#^graph-uses) |
| `supplied_by` | option external parties | authored | a party, for an external dependency | [external dependency](../kernel/objects/dependency.md#^external-dependency) |
| `consumed_by` | for a stream that yields means | authored | identifiers of the milestones, or kinds of request, that consume the output | [pull rule](../kernel/processes/tooling.md#^pull-rule) |
| `non_negotiable` | optional | authored | the date at which the agent set the mark; at most one item of the plan bears it; `check` reports a second mark, and a mark left on a closed item or a completed task | [non-negotiable key](../kernel/processes/task-selection.md#^non-negotiable-key) |
| `rank` | ordinal worth, when selected | authored | an integer within the stream and the cycle | [scales](../kernel/objects/value.md#^scales) |
| `value`, `cost_of_delay` | cardinal worth | authored | amounts in the unit of the profile, each with its basis | [quantities](../kernel/objects/value.md#^quantities) |
| `deadline` | when the milestone bears one | — | as above | — |
| `status` | always | authored | `open` · `done` · `reduced` · `stopped` | [checkpoint decision](../procedures/checkpoint-decision.md) |
| `cycle` | when selected | authored | the identifier of the cycle | [calendar record](calendar-record.md) |
| `origin` | when the milestone enters the plan as an imposed commitment or a converted request | authored | `chosen` · `imposed` · `request`; `chosen` when absent | [origin](../kernel/objects/commitment-state.md#^origin) |
