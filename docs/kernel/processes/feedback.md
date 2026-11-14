---
tags:
  - theory
index: "[Processes](docs/kernel/processes/_index.md)"
aliases:
  - Feedback
  - Metrics of the method
  - Weekly report
---
# Feedback

> [!QUESTION] Goal: from which observations are the estimates of the method revised and its policies questioned, without creating targets that can be gamed?

## Metrics

The weekly review reads three core metrics, computed from the [log records](../../specification/log-record.md). ^core-metrics

1. **Hours per stream against the allocation**, each compared with its amount according to its bound, as the [allocation of a stream](capacity-allocation.md#^forms) states, with the time spent verifying delegated output reported apart. ^verification-time
2. **Ratio of time consumed to budget**, by class of predictability, with its median and its quantile.
3. **Overhead of the method**, the time spent on the planning acts over the week, the hours of the stream `planning`, against its reserve.

Each option that a profile turns on adds one metric. ^extension-metrics

| Option | Metric |
| --- | --- |
| Reactive work | the load per request window against its length, and the fraction of requests served within their class of service |
| External parties | the latency of each party, with its median and its quantile |
| Imposed deadlines | the buffer consumed of each deadline against its work done |

## Two kinds of revision

The observations are used differently according to the [kind of parameter](../foundations/parameters.md#^parameter-kinds) that they concern. ^two-revisions

- **Estimates are revised at each cycle,** without a decision: the ratios, the latencies, the reactive load and the availability are recomputed from the logs.
- **A deviation from a policy is recorded as a deviation entry,** listed for the strategic review. It is never corrected by changing the policy to match the logs: an under-spent minimum calls for its protection, or for a recorded decision to lower it. A deviation calls for no additional effort either.

## Weekly report

Each week, a report is computed from the decision entries and the completed tasks of the week. For each active deliverable, it states what was decided, with the rationale of each decision, and what was completed. The report serves the agent, and any reader to whom the agent shows it, such as a party to whom the agent is accountable; it can be restricted to the deliverables for which the agent is accountable to one party. ^weekly-report

The report replaces a written evidence note, which the [ratified ontology](../../adr/ratified-ontology.md) judged redundant with the decision entries. A week without a decision shows only its completed tasks.

## Limits

- **Perceived speed is not evidence.** The speedup attributed to delegation is measured from the logs, since the perception of it is [unreliable](../../references/ai-delegation.md).
- **Few instruments.** The method starts with its [minimal core](../foundations/core-and-options.md#^core) and four [views](../../specification/views.md). An instrument is added only when a decision lacked the information that it would give.
