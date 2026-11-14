---
tags:
  - definition
index: "[Objects](docs/kernel/objects/_index.md)"
aliases:
  - Stream
  - Yield of a stream
  - Role of work
  - Functional role
---
# Stream and yield

> [!QUESTION] Goal: by which type is a piece of work classified, so that its allocation is decided before its tasks are compared with others?

## Yield

The **yield** of a piece of work, what the work gives the agent, is its relation to the value that the agent produces. Nine yields are distinguished, each a value of the field `yields`; a stream may yield several of them. ^roles

| Yields | Relation to value | Delay of payoff |
| --- | --- | --- |
| `results` | delivers the results for which the agent is valued | short to medium |
| `means` | builds the means by which results are produced | medium, through the results that it serves |
| `knowledge` | acquires knowledge of the environment: prior work, markets, users | long, indirect |
| `competence` | raises the competence of the agent itself | long, indirect |
| `network` | builds the relations with the people of the field, for future collaboration | long, indirect |
| `coordination` | exchanges with the parties to whom the agent answers or with whom it works | immediate, by synchronization |
| `organization` | organizes the work: chooses what is worked on, and checks its course | immediate, through the other streams |
| `integrity` | keeps the working system whole and correct: repairs its defects and updates its parts | none when done, a cost when omitted |
| `obligation` | discharges an obligation owed to an affiliation, independent of the purposes of the agent | none for the purposes; a cost when omitted |

Knowledge, competence and network are the yields whose payoff is deferred. The work that yields them is the work that a single scale of priority starves. The work that yields an obligation is the work that a single scale of priority overfeeds, since its requests are urgent and its value to the purposes is nil.

**Several yields.** A stream may yield several outcomes, such as the follow-up of conferences, which yields knowledge and a network. Each task still belongs to one stream, so its time is counted once, against the allocation of that stream, whatever the outcomes that it yields. ^several-yields

## Stream

A **stream** is a class of work that a [profile](../../profiles/_index.md) declares, with one or several yields and one [trigger](regime.md). Every task belongs to exactly one stream. ^streams

- **A profile may declare several streams of one yield,** such as two streams that yield results, or none of a yield that its domain lacks.
- **A stream has one trigger.** Work of the yield of a stream that is triggered differently, such as reading demanded by one milestone in a domain where reading is triggered by the calendar, is charged to the consumer, like [blocking tooling](../processes/tooling.md#^constraint-rule).
- **A means that is itself a result belongs to a stream that yields results.** When the thing built is delivered and valued for itself, it has its own deliverable and milestones, and the rules of [tooling](../processes/tooling.md) do not apply to it. ^means-as-result

The allocation of each stream is stated in the [allocation of capacity](../processes/capacity-allocation.md).
