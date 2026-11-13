---
tags:
  - procedure
index: "[Procedures](docs/procedures/_index.md)"
aliases:
  - Request triage
---
# Request triage

> [!QUESTION] Goal: what is decided at the arrival of an unplanned request?

The triage applies the rules of [reactive work](../kernel/processes/reactive-work.md), and takes place in a window, or at once for a request of the class `immediate`.

1. **Kind and class.** Assign the kind of the request, and read its [class of service](../kernel/processes/reactive-work.md#^classes-of-service) from the profile, or from the party where it overrides the profile. A request does not choose its own class.
2. **Size.** Judge whether the response fits in a window.
3. **Decide.** Record exactly one [outcome](../kernel/processes/reactive-work.md#^triage):
   - **Respond**, now for `immediate`, in this or the next window for `windowed`.
   - **Convert**, when the response exceeds a window: create a task or a milestone in the stream that the profile declares for the kind, with the origin `request`. If the requester relies on a date, run the [deadline feasibility](deadline-feasibility.md) before promising it.
   - **Redirect**, and tell the requester to whom.
   - **Decline**, and tell the requester why.
4. **Acknowledge.** For a conversion, tell the requester the date at which the response will come.
5. **Count.** The request entry is logged. When the kind reaches `recurrence_threshold` occurrences, open a [tooling request](tooling-request.md).
