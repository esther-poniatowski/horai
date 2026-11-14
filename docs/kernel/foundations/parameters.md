---
tags:
  - theory
index: "[Foundations](docs/kernel/foundations/_index.md)"
aliases:
  - Parameters
  - Policies and estimates
---
# Parameters

> [!QUESTION] Goal: which numerical constants does the kernel use, what is the default of each, and by which act is each revised?

## Kinds of parameter

Every parameter is of one of three kinds, which are revised by different acts. ^parameter-kinds

| Kind | Meaning | Revised by |
| --- | --- | --- |
| Policy | a rule of conduct that the agent sets for itself | a decision at the strategic review, recorded with its reason |
| Estimate | a quantity of the world, measured from the logs | the [feedback process](../processes/feedback.md), at each cycle |
| Authored | a judgment on one item | the agent, with its basis, when the item is planned |

**A log never revises a policy.** A minimum that is under-spent over a cycle is a deviation, which the strategic review answers by protecting the minimum or by deciding to lower it, and never by an automatic adjustment. Otherwise the logs would ratify the drift that the policy exists to prevent. ^policy-not-from-logs

## Policies

All values are defaults without a source, unless a reference is named. A profile overrides any of them in its record. The unit and the admissible values of each parameter are stated in the column *Values*. A default written as two bounds is an interval: a plan should keep the bounded quantity between them, and a departure is a deviation. ^parameter-table

| Parameter | Default | Values | Used in |
| --- | --- | --- | --- |
| `discretion_min` | 1/3 | a fraction of the weekly capacity, between 0 and 1 | [conditions](problem-class.md#^discretion) |
| `allocation` of each stream | none: the profile states it | a mode, a bound, an amount and a period, which the trigger of the stream suggests without fixing them | [allocation](../processes/capacity-allocation.md#^forms) |
| `active_deliverables_max` | 3 | an integer of at least 1; a derived deliverable shares the place of its source | [admission](../processes/planning-horizons.md#^admission) |
| `stall_cycles` | 2 | an integer of at least 1 | [admission](../processes/planning-horizons.md#^admission) |
| `milestones_open` | 5 to 10 | an interval of integers, per deliverable in a structured phase | [milestone](../objects/milestone.md) |
| `cycle_length` | 4 to 6 | an interval of weeks, the last week being the cool-down | [horizon](../objects/horizon.md#^cycle) |
| `block_length` | 0.5 | a fraction of a working day; when the minimum block of the [availability](../objects/availability.md) is shorter, slots replace the blocks | [block](../objects/horizon.md#^block) |
| `daily_marks` | 3 | an integer of at least 1 | [commitment states](../objects/commitment-state.md) |
| `orphan_cycles` | 2 | an integer of at least 1, in cycle plannings | [orphan rule](../objects/work-hierarchy.md#^orphan-rule) |
| `recurrence_threshold` | 3 | an integer of at least 1 | [recurrence of requests](../processes/reactive-work.md) |
| `stop_overruns` | 2 | an integer of at least 1 | [stop by default](../processes/uncertainty-control.md#^stop-default) |
| `variance_threshold` | 0.7 | a positive dispersion $\hat\sigma$ of the logarithm of the ratios | [classes of predictability](../objects/appetite.md#^variance-classes) |
| `calibration_quantile` | 0.8 | a probability above 0.5 | [calibration](../processes/uncertainty-control.md#^calibration), [buffer](../objects/deadline.md#^buffer) |
| `window_quantile` | 0.9 | a probability above 0.5 | [request windows](../processes/reactive-work.md#^reserve) |
| `prior_margin` | `routine` 2, `exploratory` 3 | a ratio of at least 1 per class of predictability, used as the quantile ratio before calibration | [calibration](../processes/uncertainty-control.md#^calibration) |
| `calibration_min_samples` | 8 | an integer of at least 1, in entries per class | [calibration](../processes/uncertainty-control.md#^calibration) |
| `latency_min_samples` | 5 | an integer of at least 1, in responses per party | [latency](../objects/external-party.md#^latency) |
| `ritual_durations` | `strategic_review` 120 min, `cycle_planning` 60 min, `weekly_review` 45 min, `daily_planning` 5 min | a duration per ritual: per strategic horizon, per cycle, per week and per day | [planning](../processes/planning-horizons.md) |
| `allocation_tolerance` | 0.02 | a fraction of the plannable time, by which the hours of a stream may depart from an exact allocation | [streams, allocation and loose tasks](../../adr/streams-allocation-and-loose-tasks.md) |
| `bootstrap_appetite` | 4 h | a duration | [bootstrap](../../procedures/bootstrap.md) |

## Estimates

| Estimate | Computed from | Used in |
| --- | --- | --- |
| median ratio $r_{50}$, quantile ratio $r_q$ and $\hat\sigma$, per class of predictability | decision entries, with censoring | [calibration](../processes/uncertainty-control.md#^calibration) |
| latency of each party | wait records | [latency](../objects/external-party.md#^latency) |
| reactive load per request window | request entries | [request windows](../processes/reactive-work.md#^reserve) |
| weekly capacity, as a distribution | clock entries | [availability](../objects/availability.md) |

## Authored quantities

The budget of an item, the appetite, the value $V$, the cost of delay $\gamma$, the worth per hour $\kappa$, the rank of a milestone, and the mark of the riskiest task are authored judgments, stated with their basis. No log revises them, although a log can show that one of them was misjudged.
