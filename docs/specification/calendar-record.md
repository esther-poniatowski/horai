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
| `id` | always | authored | an identifier | — |
| `start`, `end` | always | authored | dates | [cycle](../kernel/objects/horizon.md#^cycle) |
| `cool_down` | always | authored | the dates of the cool-down | [cycle](../kernel/objects/horizon.md#^cycle) |
| `capacity` | always | computed | the plannable capacity of the cycle, per stream, at the low quantile of the availability | [plannable capacity](../kernel/objects/availability.md#^plannable-capacity) |

## Week template

The week template places the capacity. A week may depart from it, and the departure is recorded on the week.

| Field | When it is required | Kind | Values | Source |
| --- | --- | --- | --- | --- |
| `themes` | always | authored | per block, a day, a start, a length and one stream | [theme](../kernel/objects/horizon.md#^theme) |
| `windows` | option reactive work | authored | per window, a day, a start and a length | [window](../kernel/objects/horizon.md#^window) |
| `committed` | option committed capacity | authored | per block, a day, a start, a length, the stream and the party | [regime](../kernel/objects/regime.md#^regimes) |
| `window_length` | option reactive work | computed | the quantile `window_quantile` of the logged load per window | [reserve](../kernel/processes/reactive-work.md#^reserve) |
