---
tags:
  - specification
  - wip
index: "[Specification](docs/specification/_index.md)"
aliases:
  - Party record
  - Wait record
---
# Party record

> [!QUESTION] Goal: which fields do an external party and a wait state, so that the waits are visible and the latencies can be calibrated?

Both records are required only when the profile turns the option of external parties on.

## Party

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `title` | always | authored | the name of the party, or the title of the wait | — |
| `id` | always | authored | the slug of the title, fixed at creation and unique in the plan; it names the file of the record | — |
| `relations` | always | authored | one or several of `supplies` · `delegates` · `consumes` · `reviews` · `imposes` · `requests` | [relations](../kernel/objects/external-party.md#^relations) |
| `class_of_service` | for the relation `requests`, optional | authored | per kind of request, a class that overrides the class of the profile for this party | [classes of service](../kernel/processes/reactive-work.md#^classes-of-service) |
| `latency` | computed | computed | the median and the quantile of the logged latencies, with the number of samples | [latency](../kernel/objects/external-party.md#^latency) |

## Wait

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `title` | always | authored | the name of the party, or the title of the wait | — |
| `id` | always | authored | the slug of the title, fixed at creation and unique in the plan; it names the file of the record | — |
| `tasks` | always | computed | the tasks whose field `waiting` cites the wait | [waiting](../kernel/objects/external-party.md#^waiting) |
| `party` | always | authored | the identifier of the party | — |
| `relation` | always | authored | `supplies` · `delegates` · `reviews`, among the relations of the party | [relations](../kernel/objects/external-party.md#^relations) |
| `requested` | always | authored | the date of the request | [external request](../procedures/external-request.md) |
| `expected` | always | computed, or authored below `latency_min_samples` | the date at which the response is expected | [latency](../kernel/objects/external-party.md#^latency) |
| `follow_up` | always | computed | the date of the follow-up | — |
| `latest` | under a deadline, or for the milestone of largest successor work | computed | the latest date at which the milestone can be met without the response | [three acts](../kernel/processes/external-coordination.md#^three-acts) |
| `fallback` | with `latest` | authored | what the agent does after that date | [three acts](../kernel/processes/external-coordination.md#^three-acts) |
| `acceptance` | relation `delegates` | authored | the test by which the agent accepts the output | [delegation](../kernel/processes/external-coordination.md#^delegation-acts) |
| `closed` | at the response | authored | the date of the response | — |
