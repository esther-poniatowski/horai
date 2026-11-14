---
tags:
  - definition
index: "[Objects](docs/kernel/objects/_index.md)"
aliases:
  - Appetite
  - Budget of a milestone
  - Variance class
  - Predictability
  - Checkpoint
---
# Appetite

> [!QUESTION] Goal: how much time does a piece of work receive when its duration cannot be estimated?

An **appetite** is the time that a result is judged to be worth, fixed by the agent before the work starts. Under an appetite, the scope is the adjustable variable. The notion comes from [Shape Up](../../references/shape-up.md). An appetite is an authored judgment of worth, and the logs do not set it. ^appetite

## Classes of predictability

Work is assigned to one of two classes of predictability, since the argument for an appetite holds only where variance is high, as the [distributions of duration](../../references/duration-distributions.md) show. ^variance-classes

| Class | Typical work | Time control |
| --- | --- | --- |
| `routine` | a kind of work already done several times | an estimate, corrected by the logged ratios of the class, and a checkpoint when it is consumed |
| `exploratory` | an attempt whose outcome is open, a new method, a question of an exploration | an appetite and a checkpoint |

- **Assignment by threshold.** Where the [calibration](../processes/uncertainty-control.md#^calibration) is on, a kind of work is `exploratory` when the estimated dispersion $\hat\sigma$ of the logarithm of its ratios exceeds `variance_threshold`. Otherwise, and for a kind of work never logged, the agent assigns the class, and a kind never done is `exploratory`.
- **Budget.** The budget of an item is its estimate in the class `routine`, and its appetite in the class `exploratory`.

## Checkpoint

A **checkpoint** is the decision taken when a budget is consumed: the appetite of an `exploratory` item, or the estimate of a `routine` one. Exactly one of three outcomes is recorded: a new budget with a written rationale, a reduction of scope, or a stop. For a `routine` item, the new budget is a new estimate. ^checkpoint

Continuation without a decision is excluded. At the `stop_overruns`-th consecutive overrun of the same work, the default outcome is the stop, as the process of [uncertainty control](../processes/uncertainty-control.md#^stop-default) states. The steps are given in the [checkpoint procedure](../../procedures/checkpoint-decision.md).

## Appetite, deadline and value

- **Under an imposed deadline,** an appetite is admissible when the [cumulative slack](deadline.md#^slack) stays non-negative with that appetite included in the work. The appetite is part of the demand that the test checks, so the bound is not circular.
- **A stop on the path of a hard deadline is an adjustment.** When a stop would leave a hard deadline unmet, the stop opens the [adjustments](deadline.md#^adjustment-order) of that deadline, beginning with its scope, and is not recorded silently.
- **Under a cardinal worth,** the checkpoint compares the expected worth of continuing with its expected cost, as the [stop by value](../processes/uncertainty-control.md#^stop-by-value) states.
