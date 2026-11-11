---
tags:
  - theory
index: "[Processes](docs/kernel/processes/_index.md)"
aliases:
  - Feedback
  - Metrics of the method
  - Evidence note
---
# Feedback

> [!QUESTION] Goal: from which observations are the estimates of the method revised and its policies questioned, without creating targets that can be gamed?

## Metrics

The weekly review reads two core metrics, computed from the [log records](../../specification/log-record.md). ^core-metrics

1. **Hours per stream against the allocation**, each compared in the manner that its [form of capacity](capacity-allocation.md#^forms) states, with the time spent verifying delegated output reported apart. ^verification-time
2. **Ratio of time consumed to budget**, by class of variance, with its median and its quantile.

Each option that a profile turns on adds one metric. ^extension-metrics

| Option | Metric |
| --- | --- |
| Reactive work | the load per window against its length, and the fraction of requests served within their class of service |
| External parties | the latency of each party, with its median and its quantile |
| Imposed deadlines | the buffer consumed of each deadline against its work done |

## Two kinds of revision

The observations are used differently according to the [kind of parameter](../foundations/parameters.md#^parameter-kinds) that they concern. ^two-revisions

- **Estimates are revised at each cycle,** without a decision: the ratios, the latencies, the reactive load and the availability are recomputed from the logs.
- **A deviation from a policy is a finding,** listed for the strategic review. It is never corrected by changing the policy to match the logs: an under-spent floor calls for its protection, or for a recorded decision to lower it. A deviation calls for no additional effort either.

## Evidence note

Each week ends with a written note that states, for each active deliverable, what was learned, ruled out or delivered. With one principal, the note is shown to it. With several, one note is written per principal, and covers only the deliverables of that principal. ^evidence-note

The note replaces a rule that required one milestone to advance each week. Such a rule can be met by slicing milestones, whereas a statement of what was ruled out is hard to produce without work, as the decision on the [weekly note](../../adr/weekly-note.md) records.

## Limits

- **Perceived speed is not evidence.** The speedup attributed to delegation is measured from the logs, since the perception of it is [unreliable](../../references/ai-delegation.md).
- **Few instruments.** The method starts with its [minimal core](../foundations/core-and-options.md#^core) and three [views](../../specification/views.md). An instrument is added only when a decision lacked the information that it would give.
