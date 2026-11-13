---
tags:
  - definition
index: "[Objects](docs/kernel/objects/_index.md)"
aliases:
  - Stream
  - Role of work
  - Functional role
---
# Stream and role

> [!QUESTION] Goal: by which type is a piece of work classified, so that its capacity is decided before its tasks are compared with others?

## Role

The **role** of a piece of work is its relation to the value that the agent produces. Seven roles are distinguished. ^roles

| Role | Relation to value | Delay of payoff |
| --- | --- | --- |
| Production | delivers the results for which the agent is valued | short to medium |
| Tooling | builds the means by which results are produced | medium, through the results that it serves |
| Survey | acquires knowledge of the environment: prior work, markets, users | long, indirect |
| Training | raises the competence of the agent itself | long, indirect |
| Exchange | exchanges with the parties to whom the agent answers or with whom it works | immediate, by synchronization |
| Upkeep | preserves the working system against decay | none when done, a cost when omitted |
| Duty | discharges an obligation owed to an affiliation, independent of the purposes of the agent | none for the purposes; a cost when omitted |

Survey and training are the roles whose payoff is deferred. They are the ones that a single scale of priority starves. Duty is the role that a single scale of priority overfeeds, since its requests are urgent and its value to the purposes is nil.

**Rule of exclusivity.** A piece of work that could bear two roles bears the role of the purpose for which it would be done if the other were absent. When both purposes would justify it alone, it is split into two items, or recorded under the role of the stream whose capacity it consumes, with the other noted. *Example*: a call with a customer requested as support is exchange, even when it also informs the market. ^role-exclusivity

## Stream

A **stream** is a class of work that a [profile](../../profiles/_index.md) declares, with one role and one [regime](regime.md). Every task belongs to exactly one stream. ^streams

- **A profile may declare several streams of one role,** such as two lines of production, or none of a role that its domain lacks.
- **A stream has one regime.** Work of the role of a stream that is triggered differently, such as reading pulled by one milestone in a domain where reading is a floor, is charged to the consumer, like [blocking tooling](../processes/tooling.md#^constraint-rule).
- **A means that is itself a result belongs to production.** When the thing built is delivered and valued for itself, it has its own deliverable and milestones, and the rules of [tooling](../processes/tooling.md) do not apply to it. ^means-as-result

The capacity of each stream is stated in the [allocation of capacity](../processes/capacity-allocation.md).
