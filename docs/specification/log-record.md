---
tags:
  - specification
  - wip
index: "[Specification](docs/specification/_index.md)"
aliases:
  - Log record
---
# Log record

> [!QUESTION] Goal: which entries are logged, so that the estimates and the metrics can be computed?

The clock entries are written by the tool when the agent marks the start or the stop of its work, and the time spent is computed from them. The other entries are authored, and a tool writes their timestamps, as facts that it observes.

## Clock entry

The agent marks the start and the stop of its work, and the tool writes one entry for each mark. Starting a task stops the task under way.

| Field | When it is required | Values |
| --- | --- | --- |
| `at` | always | the date and the hour, recorded by the tool |
| `event` | always | `start` · `stop` |
| `task` | for `start` | the identifier of a task, or of a parent for work without a task, such as the standing parent of an appointed stream, for attending an appointment |
| `assigned` | for a span assigned at the close of the day | a mark: the agent stated the span, and the tool did not observe it |

## Time spent

The time spent on a task during a day is computed from the clock entries, and stored nowhere. It measures how long the agent worked on that task, and not what was done: the completion of the task records the work done.

At the close of the day, the tool lists the spans of the planned blocks that no clock entry covers, and the tasks still running. The agent assigns each span to a task, which writes a pair of clock entries marked `assigned`, or leaves it untracked.

The computed time spent has three fields:

| Field | When it is required | Values |
| --- | --- | --- |
| `date` | always | a date |
| `task` | always | the identifier of a task, or of a parent for work without a task |
| `duration` | always | the time spent |

The time spent on a task that bears the field `verifies` is time spent verifying delegated output, and is reported apart.

## Decision entry

One entry is written at each [checkpoint decision](../procedures/checkpoint-decision.md), and at the completion of each item.

| Field | Values |
| --- | --- |
| `date` | the date of the decision or of the completion |
| `milestone` | the identifier of the item |
| `decision` | `done` · `stop` · `reduce` · `renew` |
| `ratio` | the time consumed divided by the budget; censored for `stop` and `reduce` |
| `rationale` | required except for `done`. It states what was obtained, what remains unknown, and why this decision; for `renew`, it names the fact that was unknown when the first budget was set |

## Request entry

Where reactive work is on, one entry is written at each [request triage](../procedures/request-triage.md).

| Field | Values |
| --- | --- |
| `arrived` | the date and the hour of arrival, recorded by the tool |
| `party` | the requester |
| `kind` | the kind of the request, from the profile |
| `class` | `immediate` · `windowed` · `scheduled` |
| `outcome` | `respond` · `convert` · `redirect` · `decline` |
| `responded` | the date and the hour of the response, recorded by the tool |
| `duration` | the time spent |
| `interrupted` | a mark, when a block was interrupted |

## Adjustment entry

Where deadlines are on, one entry is written for each adjustment of a [deadline feasibility](../procedures/deadline-feasibility.md): the deadline, the adjustment, and what it displaces.

## Deviation entry

One entry is written when the weekly review finds a deviation from a [policy](../kernel/foundations/parameters.md#^parameter-kinds): the policy, the deviation, and the cycle. The strategic review closes each deviation entry, by protecting the policy or by changing it with a recorded reason.

The latency of a party is read from the dates of the [wait records](party-record.md), and needs no entry of its own.
