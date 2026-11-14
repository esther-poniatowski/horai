---
tags:
  - definition
index: "[Objects](docs/kernel/objects/_index.md)"
aliases:
  - External party
  - Principal
  - Party to whom the agent is accountable
  - Waiting condition
  - Relations with external parties
  - Delegation
---
# External party

> [!QUESTION] Goal: how do the persons outside the agent enter a plan, given that the plan schedules the agent alone?

An **external party** is a person, an organization or an automated system, other than the agent, whose action the work awaits, who awaits a result of the work, or to whom the agent hands part of its own work. A party is never scheduled: a plan states only the acts of the agent toward it. ^party

A party is declared once, with an identifier and a name, in the file of the parties, `settings/parties.yml`. A record names a declared party by its identifier, in a field such as `party` or `accountable_to`, and names an occasional party by a mapping `{name: ...}`. An identifier that no declaration bears is an error, so that a misspelled name does not create a party.

## Relations

A party bears one or several relations to the work. ^relations

| Relation | The party | Acts of the agent | Object concerned |
| --- | --- | --- | --- |
| `supplies` | provides an artifact that a milestone needs | request, follow-up | [external dependency](dependency.md#^external-dependency) |
| `delegates` | performs a part of the work of the agent, on its instruction | brief, follow-up, review of the output | an external dependency whose output the agent verifies |
| `consumes` | receives a result | handoff | [definition of done](milestone.md#^definition-of-done) by acceptance |
| `reviews` | judges or approves a result before it counts | submission, revision | a milestone of review |
| `imposes` | fixes a date or a requirement | negotiation | [deadline](deadline.md) |
| `requests` | sends unplanned demands | triage, response | [trigger by arrival](regime.md#^regimes) |

- **Delegation differs from supply by its verification.** The output of a delegated task is the agent's responsibility, so its review is a task of the agent, and its time is [logged apart](../processes/feedback.md#^verification-time). An automated agent to which work is handed is a party of this relation.
- **Direction is outside the kernel.** Allocating the work of a team is a different problem, as the [boundaries of the class](../foundations/problem-class.md) state.

## Party to whom the agent is accountable

The **party to whom the agent is accountable** for a deliverable, its principal, is the party that the field `accountable_to` of the deliverable names: it usually reviews, imposes, and fixes dates of synchronization. Each deliverable names at most one such party, and the agent may be accountable to several parties across its deliverables. ^principal

- **With one party to whom the agent is accountable,** the dates of synchronization of that party bound the [cycle](horizon.md#^cycle).
- **With several such parties,** the cycle follows the cadence of the agent, and the meetings of each party enter the plan as appointments of a stream triggered by appointment. The [weekly report](../processes/feedback.md#^weekly-report) can be restricted to the deliverables for which the agent is accountable to one party.

## Waiting

An item is **waiting** when its next act belongs to a party. In the core, the waiting task records the date of the follow-up in its field `follow_up`. Under the option of external parties, the task also names in its field `awaits` the wait that blocks it, which records the party, the date of the request, and the date at which a response is expected. ^waiting

- **The wait attaches to the tasks that need the artifact.** These tasks leave the candidates of the selection until the response arrives. The other tasks of the same milestone remain candidates. A milestone is shown as waiting when it holds an open waiting task, and each of its open tasks waits or follows a waiting task in its local order.
- **The follow-up is a task of the agent.** It is dated at the moment of the request, and appears in the week in which it falls.
- **Waiting is a condition, not a commitment state.** An item keeps its [commitment state](commitment-state.md) while it waits.

## Latency

The **latency** of a party is the time between a request and its response. It is logged per party, and its median and its quantile `calibration_quantile` set the expected dates, as for the [calibration](../processes/uncertainty-control.md#^calibration) of budgets. ^latency

- **Cold start.** Below `latency_min_samples` responses, the expected date is the one that the party states, or the one that the agent judges, and it is marked as authored.
- **Paths are conservative.** Summing the quantiles of the latencies along a path overstates the quantile of the path. The overstatement is accepted, since a late external dependency costs more than an early request.
