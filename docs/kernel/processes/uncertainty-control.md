---
tags:
  - theory
index: "[Processes](docs/kernel/processes/_index.md)"
aliases:
  - Control of uncertainty
  - Mean residual life of a task
  - Calibration
---
# Control of uncertainty

> [!QUESTION] Goal: on which grounds is exploratory work controlled by budgets and checkpoints rather than by estimates, and how are the estimates of routine work calibrated?

## Expected remaining time

Let $T$ be the duration of a piece of work, in units of its budget. The **mean residual life** $m(t) = \mathbb{E}[T - t \mid T > t]$ is the time expected to remain once $t$ has elapsed. Within one kind of work, the ratios of actual to estimated duration are modelled as log-normal, after the [distributions of duration](../../references/duration-distributions.md). For $\ln T \sim \mathcal{N}(\mu, \sigma^2)$ and $z = (\ln t - \mu)/\sigma$: ^mrl

$$m(t) = e^{\mu + \sigma^2/2}\,\frac{\Phi(\sigma - z)}{1 - \Phi(z)} - t, \qquad m(t) \sim \frac{\sigma^2\, t}{\ln t - \mu} \quad (t \to \infty).$$

With the budget at the median ($\mu = 0$), the expected remainder is:

| $\sigma$ | at $t = 1$ | at $t = 2$ | at $t = 4$ |
| --- | --- | --- | --- |
| 0.5 | 0.57 | 0.57 | 0.70 |
| 1.0 | 1.77 | 2.19 | 2.96 |

## Consequences

- **Low variance admits estimates.** At $\sigma = 0.5$ the remainder stays near half a budget: an overrun does not announce a larger one. Routine work is therefore estimated.
- **High variance requires checkpoints.** At $\sigma = 1$ the remainder exceeds the budget and grows with the time elapsed, while its ratio to the elapsed time falls from 1.77 to 0.74 over $t \in [1, 4]$. Exploratory work receives an [appetite](../objects/appetite.md) and a [checkpoint](../objects/appetite.md#^checkpoint).
- **No proportional law.** The remainder is not proportional to the elapsed time. The asymptotic form is reached slowly, so the table, and not the asymptote, describes the range in which checkpoints occur. The decision on [variance classes](../../adr/variance-classes.md) records why the Pareto assumption was dropped.
- **Pooling hides the classes.** Ratios pooled over kinds of work of different dispersion have a heavier tail than any one kind, as the source reports. Calibration is therefore done per class, and never on the pooled log.

## Rules

- **Stop by default.** At the `stop_overruns`-th consecutive overrun of the same work, the outcome of the checkpoint is the stop, unless a written rationale states what has changed. A [non-negotiable](../foundations/commitments.md#^c-non-negotiable) item has no default outcome: its checkpoint requires an explicit decision. ^stop-default
- **Stop by value.** Under a cardinal [worth](../objects/value.md), the checkpoint at elapsed time $t$, for an item of budget $b$ hours, compares renewals of length $\Delta$, in budget units, by their expected net worth ^stop-by-value

$$G(\Delta) = \Pr(T \le t + \Delta \mid T > t)\, V - \kappa\, b\, \mathbb{E}\left[\min(T - t, \Delta) \mid T > t\right].$$

  The default outcome is the stop when $G(\Delta) \le 0$ for every renewal considered, and otherwise the renewal of largest $G$. The rule looks one interval ahead: it counts the option of stopping at the next checkpoint, which a comparison of the whole remainder with $V$ ignores. *Example*: at $\sigma = 1$, $t = 1$ and $V = 1.5\,\kappa b$, the whole remainder costs $1.77\,\kappa b > V$, yet a renewal of one budget has $G(1) \approx 0.06\,\kappa b > 0$. The rule is myopic, and is not proven optimal.
- **Calibration.** Each completed item gives a ratio of time consumed to budget, and each stopped or reduced item gives a ratio censored at its value. The ratios are grouped by class of calibration: the stream of the item, the type of its deliverable, and its class of predictability. An item without a deliverable shares its class with the items of its stream that have none. Per class of calibration, the distribution of the logarithm of the ratio is estimated with the censoring taken into account, by a product-limit estimate or a log-normal fit by maximum likelihood. It yields $r_{50}$, $r_q$ at `calibration_quantile`, and $\hat\sigma$. ^calibration
  - The estimates correct the budgets of routine work, set the [buffers](../objects/deadline.md#^buffer), and assign the [predictability](../objects/appetite.md#^variance-classes) by `variance_threshold`.
  - They never set an appetite, which remains a judgment of worth.
  - Below `calibration_min_samples` entries in a class of calibration, prior ratios stand in for the logged ones: a median of 1, and a quantile equal to the `prior_margin` of the type of deliverable where the profile states one, and otherwise to the policy `prior_margin` of the class of predictability, after the margins of estimation of the [time-management course](../../references/time-management-course.md).
- **Padding is visible.** A median ratio well below 1 shows padded budgets, which the [feedback process](feedback.md) reports.
