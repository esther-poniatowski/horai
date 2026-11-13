---
tags:
  - theory
index: "[Processes](docs/kernel/processes/_index.md)"
aliases:
  - Reactive work
  - Class of service
  - Reserve
  - Triage
---
# Reactive work

> [!QUESTION] Goal: how are unplanned requests served within their expected time of response, without displacing the planned work at the moment of their arrival?

A **request** is a demand that an [external party](../objects/external-party.md) sends at a time that the plan did not fix, with an expected time of response. Requests are the work of the streams under the [reactive regime](../objects/regime.md#^regimes). Each request has a **kind**, which the profile declares, such as a defect report or a question. ^request

## Classes of service

A profile declares the class of service of each kind of request, optionally per party, and the time of response of each class. Three classes are distinguished. ^classes-of-service

| Class | Served | Effect on the plan |
| --- | --- | --- |
| `immediate` | at once | interrupts the current block; the interruption is logged and counted in the reactive load |
| `windowed` | in the next [window](../objects/horizon.md#^window) | none on the blocks |
| `scheduled` | as planned work | enters the inbox, then a plan through the weekly review |

The class `immediate` is the one exception to the seventh [commitment](../foundations/commitments.md#^c-reserve). It is kept for the requests whose delay harms a party beyond repair within a day.

## Reserve

The reserve is the time of the windows. A person who serves requests only in windows is not a queue with continuous service: the time of response is dominated by the gap between two windows, and the question is how often the load of one window exceeds its length. ^reserve

- **Length of a window.** A window lasts the quantile `window_quantile` of the logged reactive load per window, so that the load of a window exceeds its length on a known fraction of days. *Example*: with five requests a day of ten minutes each, arriving at random, a daily window sized on the mean (50 minutes) overflows on about half of the days, and one sized on the 0.9 quantile (80 minutes) on about 7%.
- **Placement.** The windows are placed so that the gap between two windows is shorter than the time of response of the class `windowed`.
- **Stability.** The weekly reserve $r$ exceeds the mean weekly load $\ell$, so that $\rho = \ell / r < 1$. Above it, the backlog of requests grows without bound, as [queueing theory](../../references/queueing-and-reactive-work.md) shows. This is a necessary condition, not a rule of sizing.
- **An unused window returns to the plan.** The reserve is therefore a bound and not a cost. Its time also serves the tasks that [release a wait](task-selection.md#^release-key).
- **Discretion.** When the reserve and the appointed blocks leave less than `discretion_min` of the capacity, the method degrades as the [boundaries of the class](../foundations/problem-class.md) state.

## Triage

Each request receives exactly one of four outcomes. ^triage

1. **Respond**, within its class of service, when the response fits in a window.
2. **Convert**, when the response exceeds a window: the request becomes a task or a milestone of the stream that the profile declares for its kind, and enters a plan with the origin `request`. Its time is drawn from that stream. Conversions that persist over a cycle are a deviation for the strategic review, which may change the allocation.
3. **Redirect**, to the party that can serve it.
4. **Decline**, with the reason stated to the requester.

## Recurrence

A kind of request that reaches `recurrence_threshold` occurrences pulls [tooling](tooling.md#^pull-rule): a documented answer, a template or an automated response. Reactive load is thereby the one source of work that the method aims to reduce.

The steps are given in the [triage procedure](../../procedures/request-triage.md).
