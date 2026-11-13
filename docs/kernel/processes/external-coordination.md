---
tags:
  - theory
index: "[Processes](docs/kernel/processes/_index.md)"
aliases:
  - External coordination
  - Request, follow-up and fallback
  - Handoff
---
# External coordination

> [!QUESTION] Goal: how does a plan that schedules one agent account for the persons on whom the work waits, for those who wait on it, and for those to whom it delegates?

An [external party](../objects/external-party.md) is never scheduled, by the eighth [commitment](../foundations/commitments.md#^c-own-acts). Each relation with a party is therefore reduced to acts of the agent.

## Outbound: the agent awaits a party

An [external dependency](../objects/dependency.md#^external-dependency) is managed by three acts, all fixed at the moment of the request. ^three-acts

| Act | Content | Date |
| --- | --- | --- |
| Request | what is asked, in a form that the party can answer without a further exchange | no later than the latest date below |
| Follow-up | a reminder, or a check of the state | the expected date of the response, read from the [latency](../objects/external-party.md#^latency) |
| Fallback | another supplier, a reduced scope, or work on a stated assumption | the latest date at which the milestone can still be met without the party |

- **Release the wait first.** The request is made as soon as its content can be stated, and before the work of the agent that could run in parallel, as the [release key](task-selection.md#^release-key) states. It may be made in the next window.
- **Latest date of a request.** For a milestone under a deadline $D$, the request is sent no later than $D$ minus the remaining work of the agent after the artifact arrives, minus the latency of the party at `calibration_quantile`.
- **A fallback is required under a deadline,** and for a milestone with the largest successor work of its deliverable.
- **Work on an assumption is marked.** A result produced on an assumed response is revised when the response arrives, and the revision is a [lateral entry](planning-horizons.md#^lateral-entries).

## Delegation

A delegated task adds two acts to the three above. ^delegation-acts

- **Brief.** The brief states the output expected and the test by which the agent will accept it, so that the review is a check against a stated test.
- **Review.** The review of the output is a task of the agent, whose time is logged as [verification](feedback.md#^verification-time). A delegated task is done when the review accepts it.

## Inbound: a party awaits the agent

- **A handoff has an acceptance.** A result that a party consumes is done when the party accepts it, as the [definition of done](../objects/milestone.md#^definition-of-done) states. The handoff states what is delivered, what remains, and what is expected in return.
- **A review is a loop with a latency.** A result that a party reviews counts two milestones: the submission, and the revision. The latency of the review lies between them, and is planned as an external dependency.
- **A promise to a party is tested before it is made,** as the rule on [promised dates](../objects/deadline.md#^promised-date) states.

## Synchronization

The recurring meetings with each [principal](../objects/external-party.md#^principal) are milestones of the exchange stream, and the meetings of a single principal bound the cycles, as the [planning process](planning-horizons.md) states. Between two meetings, the questions for a principal are batched, unless one of them releases a wait under a deadline.

The steps are given in the [procedure for an external request](../../procedures/external-request.md).
