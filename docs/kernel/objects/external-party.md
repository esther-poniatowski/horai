---
tags:
  - definition
index: "[Objects](docs/kernel/objects/_index.md)"
aliases:
  - External party
  - Principal
  - Waiting condition
  - Relations with external parties
  - Delegation
---
# External party

> [!QUESTION] Goal: how do the persons outside the agent enter a plan, given that the plan schedules the agent alone?

An **external party** is a person, an organization or an automated system, other than the agent, whose action the work awaits, who awaits a result of the work, or to whom the agent hands part of its own work. A party is never scheduled: a plan states only the acts of the agent toward it. ^party

## Relations

A party bears one or several relations to the work. ^relations

| Relation | The party | Acts of the agent | Object concerned |
| --- | --- | --- | --- |
| `supplies` | provides an artifact that a milestone needs | request, follow-up | [external dependency](dependency.md#^external-dependency) |
| `delegates` | performs a part of the work of the agent, on its instruction | brief, follow-up, review of the output | an external dependency whose output the agent verifies |
| `consumes` | receives a result | handoff | [definition of done](milestone.md#^definition-of-done) by acceptance |
| `reviews` | judges or approves a result before it counts | submission, revision | a milestone of review |
| `imposes` | fixes a date or a requirement | negotiation | [deadline](deadline.md) |
| `requests` | sends unplanned demands | triage, response | [reactive regime](regime.md#^regimes) |

- **Delegation differs from supply by its verification.** The output of a delegated task is the agent's responsibility, so its review is a task of the agent, and its time is [logged apart](../processes/feedback.md#^verification-time). An automated agent to which work is handed is a party of this relation.
- **Direction is outside the kernel.** Allocating the work of a team is a different problem, as the [boundaries of the class](../foundations/problem-class.md) state.

## Principal

A **principal** is a party to whom the agent answers for a deliverable: it usually reviews, imposes, and fixes dates of synchronization. Each deliverable has at most one principal, and the agent may have several principals across its deliverables. ^principal

- **With one principal,** its dates of synchronization bound the [cycle](horizon.md#^cycle).
- **With several principals,** the cycle follows the cadence of the agent, and the dates of each principal enter the plan as milestones of the exchange stream. The [weekly report](../processes/feedback.md#^weekly-report) can be restricted to the deliverables of each principal.

## Waiting

An item is **waiting** when its next act belongs to a party. In the core, the condition records the date of the follow-up. Under the option of external parties, it also records the party, the date of the request, and the date at which a response is expected. ^waiting

- **The wait attaches to the tasks that need the artifact.** These tasks leave the candidates of the selection until the response arrives. The other tasks of the same milestone remain candidates. A milestone is shown as waiting when it holds an open waiting task, and each of its open tasks waits or follows a waiting task in its local order.
- **The follow-up is a task of the agent.** It is dated at the moment of the request, and appears in the week in which it falls.
- **Waiting is a condition, not a commitment state.** An item keeps its [commitment state](commitment-state.md) while it waits.

## Latency

The **latency** of a party is the time between a request and its response. It is logged per party, and its median and its quantile `calibration_quantile` set the expected dates, as for the [calibration](../processes/uncertainty-control.md#^calibration) of budgets. ^latency

- **Cold start.** Below `latency_min_samples` responses, the expected date is the one that the party states, or the one that the agent judges, and it is marked as authored.
- **Paths are conservative.** Summing the quantiles of the latencies along a path overstates the quantile of the path. The overstatement is accepted, since a late external dependency costs more than an early request.
