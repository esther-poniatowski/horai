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

**A log never revises a policy.** A floor that is under-spent over a cycle is a finding, which the strategic review answers by protecting the floor or by deciding to lower it, and never by an automatic adjustment. Otherwise the logs would ratify the drift that the policy exists to prevent. ^policy-not-from-logs

## Policies

All values are defaults without a source, unless a reference is named. A profile overrides any of them in its record. ^parameter-table

| Parameter | Default | Used in |
| --- | --- | --- |
| `discretion_min` | one third of the weekly capacity | [conditions](problem-class.md#^discretion) |
| allocation of each stream | set by the profile | [allocation](../processes/capacity-allocation.md#^forms) |
| `active_deliverables_max` | 3 | [admission](../processes/planning-horizons.md#^admission) |
| `stall_cycles` | 2 | [admission](../processes/planning-horizons.md#^admission) |
| `milestones_open` | 5 to 10 per deliverable in a structured phase | [milestone](../objects/milestone.md) |
| `milestones_per_cycle` | 1 to 3 per active deliverable | [cycle planning](../../procedures/cycle-planning.md) |
| `cycle_length` | 4 to 6 weeks, the last being the cool-down | [horizon](../objects/horizon.md#^cycle) |
| `theme_length` | a half-day, bounded by the minimum block of the [availability](../objects/availability.md) | [theme](../objects/horizon.md#^theme) |
| `daily_marks` | 3 | [commitment states](../objects/commitment-state.md) |
| `orphan_cycles` | 2 | [orphan rule](../objects/work-hierarchy.md#^orphan-rule) |
| `recurrence_threshold` | 3 | [manual first](../processes/enablement.md#^manual-first), [recurrence of requests](../processes/reactive-work.md) |
| `stop_overruns` | 2 | [stop by default](../processes/uncertainty-control.md#^stop-default) |
| `variance_threshold` | $\hat\sigma = 0.7$ | [classes of variance](../objects/appetite.md#^variance-classes) |
| `calibration_quantile` | 0.8 | [calibration](../processes/uncertainty-control.md#^calibration), [buffer](../objects/deadline.md#^buffer) |
| `window_quantile` | 0.9 | [windows](../processes/reactive-work.md#^reserve) |
| `calibration_min_samples` | 8 entries per class | [calibration](../processes/uncertainty-control.md#^calibration) |
| `latency_min_samples` | 5 | [latency](../objects/external-party.md#^latency) |
| durations of the rituals | strategic 120 min a quarter, cycle 60 min, weekly 45 min, daily 5 min | [planning](../processes/planning-horizons.md) |
| `overhead_budget` | 105 min a week for the core | [core and options](core-and-options.md#^overhead) |
| `bootstrap_appetite` | 4 h | [bootstrap](../../procedures/bootstrap.md) |

## Estimates

| Estimate | Computed from | Used in |
| --- | --- | --- |
| median ratio $r_{50}$, quantile ratio $r_q$ and $\hat\sigma$, per class of variance | checkpoint and completion entries, with censoring | [calibration](../processes/uncertainty-control.md#^calibration) |
| latency of each party | wait records | [latency](../objects/external-party.md#^latency) |
| reactive load per window | request entries | [windows](../processes/reactive-work.md#^reserve) |
| weekly capacity, as a distribution | time entries | [availability](../objects/availability.md) |

## Authored quantities

The budget of an item, the appetite, the value $V$, the cost of delay $\gamma$, the cost of capacity $\kappa$, the ordinal rank of a milestone, and the mark of risk are authored judgments, stated with their basis. No log revises them, although a log can show that one of them was misjudged.
