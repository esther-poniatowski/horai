---
tags:
  - profile
index: "[Profiles](docs/profiles/_index.md)"
aliases:
  - Research profile
  - Doctoral research
---
# Research

> [!QUESTION] Goal: which values configure the kernel for a doctoral researcher who conducts several projects toward publications, builds the tools that they need, and delegates part of the work to automated agents?

## Streams

The shares assume a plannable capacity of about 30 hours a week, and are defaults without a source. ^shares

| Stream | Role | Regime | Capacity | Placement |
| --- | --- | --- | --- | --- |
| `inquiry`: project results | production | `planned` | share of 45% | the longest blocks, at the hours of highest energy |
| `tools`: tools and frameworks | tooling | `pulled` | ceiling of 15% | dedicated blocks |
| `training`: mathematics | training | `floor` | floor of 20% | a daily slot at a fixed hour, plus one longer block |
| `bibliography`: bibliography | survey | `floor` | floor of 10% | two fixed sessions a week |
| `meetings`: supervision and lab meetings | exchange | `appointed` | a share of preparation, and a cap of about three hours per meeting | — |
| `upkeep`: vault and defects | upkeep | `batched` | slots of low energy | — |
| `requests`: correspondence and requests | exchange | `reactive` | reserve, one window a day | — |

The streams `meetings`, `upkeep` and `requests` share the remaining 10%. The values are [policies](../kernel/foundations/parameters.md#^parameter-kinds): the logs report deviations from them, and only the strategic review changes them.

A framework intended for publication is a [means that is a result](../kernel/objects/stream.md#^means-as-result), and belongs to P.

## Names

| Kernel | Research |
| --- | --- |
| Purpose · deliverable | thesis · paper |
| Exploration · validation · delivery | exploration · understanding · distillation |
| Strategic horizon | quarter |
| Cycle | `cycle_length`, synchronized with the meetings with the supervisor |

## Options

| Option | Setting |
| --- | --- |
| Tooling control | on |
| Milestone graph | on, for the deliverables in distillation |
| Calibration | on once `calibration_min_samples` entries exist per class |
| Reactive work | on, light: kinds correspondence and requests of the lab, classes `windowed` and `scheduled`, no `immediate` class |
| External parties | on: the supervisor is the principal (`reviews`, `imposes`); co-authors (`supplies`, `reviews`); reviewers and editors (`reviews`, with a latency of months) |
| Delegation | on: automated agents (`delegates`), whose output is reviewed and the review logged |
| Imposed deadlines | on: submissions to conferences and journals (`hard`), revisions, the thesis (on the purpose) |
| Valuation | ordinal |

## Modules

- [Bibliography](../modules/bibliography/_index.md), for the stream `bibliography`.
- [Mathematical mastery](../modules/mathematical-mastery/_index.md), for the stream `training`.
- Four further modules are proposed for this profile, as the [index of modules](../modules/_index.md) lists.

## Notes specific to the domain

- **Delegation to agents.** Automated agents are parties of the relation `delegates`: each delegated task has a brief with a test of acceptance, and the time spent verifying the output is [logged apart](../kernel/processes/feedback.md#^verification-time).
- **Margins before calibration.** The prior margin of exploratory work is raised to 4, after the range of 4 to 10 that the [time-management course](../references/time-management-course.md) gives for research.
- **Teaching.** Assigned teaching is a stream of the role duty under the regime `appointed`.
- **Review loops.** A submission and its revision are two milestones separated by the latency of the reviewers, as [external coordination](../kernel/processes/external-coordination.md) states. The latency is used for another paper.
- **Choice of problems.** The kernel does not address the choice of a problem. The quarterly review of the ideas file is its place, with the sources that the [phases of research](../references/research-phases.md) cite.
