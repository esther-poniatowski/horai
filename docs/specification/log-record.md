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

All entries are authored, except the timestamps that a tool records.

## Time entry

One entry is written per item and per day, at the close of the day.

| Field | When it is required | Values |
| --- | --- | --- |
| `date` | always | a date |
| `parent` | always | the identifier of a milestone, a question or a standing parent |
| `duration` | always | the time spent |
| `verification` | when work was delegated | the part of the duration spent verifying the delegated output |

## Outcome entry

One entry is written at each [checkpoint decision](../procedures/checkpoint-decision.md), and at the completion of each item.

| Field | Values |
| --- | --- |
| `milestone` | the identifier of the item |
| `outcome` | `done` · `stop` · `reduce` · `renew` |
| `ratio` | the time consumed divided by the budget; censored for `stop` and `reduce` |
| `justification` | required for `renew` |

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
| `interrupted` | a mark, when a theme was interrupted |

## Adjustment entry

Where deadlines are on, one entry is written for each adjustment of a [deadline feasibility](../procedures/deadline-feasibility.md): the deadline, the adjustment, and what it displaces.

## Finding entry

One entry is written when the weekly review finds a deviation from a [policy](../kernel/foundations/parameters.md#^parameter-kinds): the policy, the deviation, and the cycle. The strategic review closes each finding with a decision.

## Evidence note

One note per week, and per principal where there are several, states for each deliverable concerned what was learned, ruled out or delivered, as the [feedback process](../kernel/processes/feedback.md#^evidence-note) requires.

The latency of a party is read from the dates of the [wait records](party-record.md), and needs no entry of its own.
