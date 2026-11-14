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

The shares assume a plannable capacity of about 30 hours a week, the time left once the appointments and the reserves are removed. The shares and the reserves are defaults without a source. ^shares

| Stream and description | Yields | Triggered by | Allocation | Placement |
| --- | --- | --- | --- | --- |
| `inquiry`: advances the results of the research projects | results | `selection` | an exact share of 45% | the longest blocks, at the hours of highest energy |
| `tools`: builds the tools and frameworks that the projects consume | means | `demand` | a share of at most 15% | dedicated blocks |
| `training`: derives the mathematics that the projects will need | competence | `calendar` | a share of at least 20% | a daily slot at a fixed hour, plus one longer block |
| `bibliography`: surveys the literature of the field | knowledge | `calendar` | a share of at least 10% | two fixed sessions a week |
| `meetings`: prepares and holds the supervision and lab meetings | coordination | `appointment` | a reserve of at most `PT3H` per event, for each meeting that a task prepares | the appointments, recurring or placed each week |
| `upkeep`: repairs the vault and its defects | integrity | `accumulation` | none | positions of low energy |
| `requests`: answers the correspondence and the requests of others | coordination | `arrival` | an exact reserve of `PT1H30M` per week, a prior that the logged load replaces | one request window a day |
| `planning`: plans the work and reviews its course | organization | `calendar` | a reserve of at most `PT1H45M` per week | the blocks of the weekly review and of the daily plannings |

The reserves of `meetings`, `requests` and `planning` are removed before the shares, and the shares leave 10% of the plannable capacity unallocated, in which `upkeep` takes its time. The values are [policies](../kernel/foundations/parameters.md#^parameter-kinds): the logs report deviations from them, and only the strategic review changes them.

A framework intended for publication is a [means that is a result](../kernel/objects/stream.md#^means-as-result), and belongs to `inquiry`.

## Types of deliverable

| Type | Description | Predictability | Starting phase | Review latency | Stages, by the phase from which they exist |
| --- | --- | --- | --- | --- | --- |
| `abstract` | summarizes results for the selection committee of a conference | `routine` | delivery | about two months, the latency of the committee | delivery: argument plan · draft · submission |
| `article` | reports established results to the field | `exploratory` | exploration | about three months, the latency of the reviewers | validation: argument plan; delivery: draft · internal review · submission · revision |
| `poster` | presents established results at a conference | `routine`, with a prior margin of 1.5 | delivery | — | delivery: argument plan · layout · print |
| `talk` | presents results to an audience | `routine` | delivery | — | delivery: argument plan · slides · rehearsal |
| `chapter` | states published results as a chapter of the thesis | `routine` | delivery | a few weeks, the latency of the supervisor | delivery: draft · review by the supervisor · revision |
| `software` | publishes a framework that the projects built | `exploratory` | exploration | — | validation: prototype; delivery: documentation · release |

Each stage becomes a milestone when its deliverable enters the phase of the stage. The argument plan establishes the messages and the arguments, and has them agreed, before any writing, which then projects them.

## Cadences

| Horizon | Research |
| --- | --- |
| Strategic horizon | quarter |
| Cycle | `cycle_length`, synchronized with the meetings with the supervisor |

## Enabled mechanisms

| Mechanism | Setting |
| --- | --- |
| Tooling control | on |
| Milestone graph | on, for the deliverables in the phase delivery |
| Calibration | on once `calibration_min_samples` entries exist in a class of calibration, a type of deliverable with a class of predictability |
| Reactive work | on, light: kinds correspondence and requests of the lab, classes `windowed` and `scheduled`, no `immediate` class |
| External parties | on: the supervisor is the party to whom the agent is accountable (`reviews`, `imposes`); co-authors (`supplies`, `reviews`); reviewers and editors (`reviews`, with a latency of months) |
| Delegation | on: automated agents (`delegates`), whose output is reviewed and the review logged |
| Imposed deadlines | on: submissions to conferences and journals (`hard`), revisions, the thesis (on the purpose) |
| Worth | ordinal |

## Modules

- [Bibliography](../modules/bibliography/_index.md), for the stream `bibliography`.
- [Mathematical mastery](../modules/mathematical-mastery/_index.md), for the stream `training`.
- Four further modules are proposed for this profile, as the [index of modules](../modules/_index.md) lists.

## Notes specific to the domain

- **Delegation to agents.** Automated agents are parties of the relation `delegates`: each delegated task has a brief with a test of acceptance, and the time spent verifying the output is [logged apart](../kernel/processes/feedback.md#^verification-time).
- **Margins before calibration.** The prior margin of exploratory work is raised to 4, after the range of 4 to 10 that the [time-management course](../references/time-management-course.md) gives for research.
- **Teaching.** Assigned teaching is a stream that yields obligation, triggered by appointment.
- **Review loops.** A submission and its revision are two milestones separated by the latency of the reviewers, as [external coordination](../kernel/processes/external-coordination.md) states. The latency is used for another article.
- **Choice of problems.** The kernel does not address the choice of a problem. The quarterly review of the ideas file is its place, with the sources that the [phases of research](../references/research-phases.md) cite.
