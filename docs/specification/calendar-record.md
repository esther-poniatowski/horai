---
tags:
  - specification
  - wip
index: "[Specification](docs/specification/_index.md)"
aliases:
  - Calendar record
  - Cycle record
---
# Calendar record

> [!QUESTION] Goal: which fields state the cycles and the placement of the capacity in time, so that the allocation can be checked and the views computed?

## Cycle

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `id` | always | authored | an identifier, which names the file of the cycle | [file layout](file-layout.md) |
| `start`, `end` | always | authored | dates | [cycle](../kernel/objects/horizon.md#^cycle) |
| `cool_down` | always | authored | the dates of the cool-down | [cycle](../kernel/objects/horizon.md#^cycle) |
| `capacity` | always | computed | the plannable capacity of the cycle, per stream, at the low quantile of the availability | [plannable capacity](../kernel/objects/availability.md#^plannable-capacity) |

## Week

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `opened` | always | authored | the date of the weekly review that opens the week | [state rule](../kernel/objects/commitment-state.md#^state-rule) |
| `blocks`, `windows` | when the week departs from the template | authored | the blocks and the windows of the week, in place of those of the template | [weekly review](../procedures/weekly-review.md) |

## Appointment

An appointment is a dated block of the regime [`appointed`](../kernel/objects/regime.md#^regimes), recorded as soon as it is known. A block that recurs every week is placed in the week template instead.

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `title` | always | authored | the title of the appointment | — |
| `id` | always | authored | the slug of the title, fixed at creation and unique in the plan; it names the file of the record | [file layout](file-layout.md) |
| `date`, `start`, `length` | always | authored | a date, an hour and a duration | [block](../kernel/objects/horizon.md#^block) |
| `stream` | always | authored | a stream of the regime `appointed` | [regime](../kernel/objects/regime.md#^regimes) |
| `party` | always | authored | the party that fixed the block: a name, or the identifier of a party under the option of external parties | [external party](../kernel/objects/external-party.md#^party) |
| `cap` | optional | authored | a duration: the maximum of preparation, in place of the cap of the stream | [forms of capacity](../kernel/processes/capacity-allocation.md#^forms) |

## Week template

The week template places the capacity. A week may depart from it, and the departure is recorded on the week.

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `blocks` | always | authored | per block, a day, a start, a length and one stream | [block](../kernel/objects/horizon.md#^block) |
| `windows` | option reactive work | authored | per window, a day, a start and a length | [window](../kernel/objects/horizon.md#^window) |
| `appointed` | with a stream of the regime `appointed` | authored | per recurring appointed block, a day, a start, a length, the stream and the party | [regime](../kernel/objects/regime.md#^regimes) |
| `window_length` | option reactive work | computed | the quantile `window_quantile` of the logged load per window | [reserve](../kernel/processes/reactive-work.md#^reserve) |
