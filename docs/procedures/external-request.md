---
tags:
  - procedure
index: "[Procedures](docs/procedures/_index.md)"
aliases:
  - External request
  - Handoff
  - Delegation brief
---
# External request

> [!QUESTION] Goal: how is a request to an external party stated, so that the wait is visible and bounded?

The procedure applies the rules of [external coordination](../kernel/processes/external-coordination.md). It serves equally for a delegation and for a handoff that awaits an acceptance or a review.

1. **Content.** State what is asked, in a form that the party can answer without a further exchange: the artifact expected, its form, and the date at which it is needed. For a delegation, state the test of acceptance.
2. **Expected date.** Read the latency of the party at `calibration_quantile`. Below `latency_min_samples` responses, ask the party for a date, or judge one, and mark it as authored.
3. **Latest date.** Under a deadline, compute the latest date of the request and of the response, as the [three acts](../kernel/processes/external-coordination.md#^three-acts) state.
4. **Fallback.** Under a deadline, or for the milestone of largest successor work, state the fallback.
5. **Send.** Send the request as soon as its content is stated, in the next window if need be.
6. **Mark.** Create the wait record, attached to the tasks that need the artifact.
7. **Close.** At the response, record its date, and create the tasks of revision if work was done on an assumption. For a delegation, review the output against its test, and log the time of review as verification.
