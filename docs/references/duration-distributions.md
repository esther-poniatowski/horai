---
tags:
  - reference
index: "[References](docs/references/_index.md)"
aliases:
  - Distributions of duration
  - Planning fallacy
---
# Distributions of duration

## Findings

- **Tasks.** Bernhardsson analyses a public dataset of estimated and actual durations of software tasks. He models the ratio of actual to estimated duration of each task as log-normal, with a dispersion that differs between tasks. The pooled logarithms of the ratios are fitted by a Student-$t$ law, whose implied mean ratio is infinite. The median ratio is near 1 and the sample mean 1.81 [bernhardsson2019]. Read through a single log-normal law, a mean of 1.81 at a median of 1 implies $\sigma = \sqrt{2 \ln 1.81} \approx 1.09$.
- **Projects.** Flyvbjerg and co-authors find that the cost overruns of 5,392 IT projects follow a power law [flyvbjerg2022]. The finding concerns the costs of projects, and not the durations of tasks.
- **Flow systems.** Sources on Kanban describe the lead times of activities by a Weibull law with a shape between 1.3 and 2, without a public dataset [anderson-duration].
- **Bias.** The *planning fallacy* is the tendency to underestimate the duration of one's own work, and reference-class forecasting corrects it by the outcomes of comparable past work [kahneman1979].

## Mean residual life

For a duration $T$, the mean residual life is $m(t) = \mathbb{E}[T - t \mid T > t]$.

- **Pareto**, shape $\alpha > 1$: $m(t) = t/(\alpha - 1)$, proportional to the time elapsed.
- **Log-normal**, $\ln T \sim \mathcal{N}(\mu, \sigma^2)$: $m(t)$ grows as $\sigma^2 t/(\ln t - \mu)$, more slowly than $t$.

The values of the log-normal case at $\sigma = 0.5$ and $\sigma = 1$ are tabulated in the note on [uncertainty control](../kernel/processes/uncertainty-control.md#^mrl).

## Bearing on `horai`

- The two values of the [predictability](../kernel/objects/appetite.md#^variance-classes) follow from the dependence of $m(t)$ on $\sigma$.
- The log-normal law holds per kind of work, not for the pooled log, whose tail is heavier. The [calibration](../kernel/processes/uncertainty-control.md#^calibration) is therefore made per type of deliverable, and separately for routine and for exploratory work.
- At $\sigma \approx 1.09$, ordinary software tasks of the dataset would fall in the predictability `exploratory` under the default `variance_threshold`. The threshold is a policy, to be judged against the logs of each agent.
- [Calibration](../kernel/processes/uncertainty-control.md#^calibration) from logged ratios is a form of reference-class forecasting, with the past work of the researcher as the class.
- The log-normal law was observed on software tasks. Its transfer to mathematical research is an assumption, which the logs can test.

## Sources

- [bernhardsson2019] ✓ [Bernhardsson, "Why software projects take longer than you think: a statistical model", 2019](https://erikbern.com/2019/04/15/why-software-projects-take-longer-than-you-think-a-statistical-model)
- [flyvbjerg2022] ✓ [Flyvbjerg et al., "The Empirical Reality of IT Project Cost Overruns: Discovering A Power-Law Distribution", 2022](https://arxiv.org/abs/2210.01573)
- [anderson-duration] ✓ [Anderson, "What We Know About Duration: Individual Activities"](https://djaa.com/what-we-know-about-duration-individual-activities/)
- [kahneman1979] ○ Kahneman and Tversky, "Intuitive prediction: biases and corrective procedures", *TIMS Studies in Management Science*, 12, 1979, pp. 313–327
