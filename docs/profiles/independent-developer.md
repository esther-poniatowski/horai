---
tags:
  - profile
  - wip
index: "[Profiles](docs/profiles/_index.md)"
aliases:
  - Independent developer profile
---
# Independent developer

> [!QUESTION] Goal: which values configure the kernel for the developer or maintainer of software, whose users and contributors send a continuous flow of requests?

> [!WARNING] Sketch
> This profile tests the generality of the kernel. No use has validated its values.

## Streams

| Stream | Yields | Triggered by | Allocation |
| --- | --- | --- | --- |
| Features | results | `selection` | an exact share |
| Build and infrastructure | means | `demand` | a share at most |
| Ecosystem watch | knowledge | `calendar` | a share at least |
| Techniques | competence | `calendar` | a share at least |
| Releases and community | coordination | `appointment` | a reserve per event, at most, for each release that a task prepares |
| Dependencies and debt | integrity | `accumulation` | none: the positions of low energy, and the cool-down |
| Issues and contributions | integrity | `arrival` | a reserve, the largest of the profiles |
| Planning | organization | `calendar` | a reserve per week, of at most `PT1H45M` by default |

## Types of deliverable

| Type | Description | Predictability | Starting phase | Review latency | Stages |
| --- | --- | --- | --- | --- | --- |
| `prototype` | tests a design before it enters a release | `exploratory` | exploration | — | spike · decision |
| `release` | delivers a version of the software to its users | `routine` | validation | — | feature freeze · release candidate · release |

## Cadences

| Horizon | Independent developer |
| --- | --- |
| Cycle | the release cycle |

## Enabled mechanisms

| Mechanism | Setting |
| --- | --- |
| Reactive work | on, heavy: kinds security report (`immediate`), defect and review of a contribution (`windowed`), feature request (`scheduled`, converted to the stream Features) |
| External parties | on: users (`requests`), contributors (`supplies`, and await a review), upstream projects (`supplies`, with a latency) |
| Imposed deadlines | rare: the disclosure date of a vulnerability |
| Worth | ordinal, unless a sponsor or a client pays for a result |

## Notes specific to the domain

- **The queue is not the roadmap.** A feature request is of the class `scheduled`: it enters the backlog, and the [commitment states](../kernel/objects/commitment-state.md) keep it out of sight until a planning selects it.
- **A release date set by the maintainer is not a deadline,** by the [guard on self-set dates](../kernel/objects/deadline.md#^no-self-deadline), unless users rely on it once announced.
- **A contribution inverts the wait.** The contributor awaits a review by the agent, so the review is a request under a class of service, and its delay is a latency that the agent imposes on a party.
- **Recurrent issues pull tooling:** documentation, a template of issue, an automated check.
- **Degraded mode.** When the reserve leaves less than `discretion_min` of the week, the profile runs in the [degraded mode](../kernel/foundations/problem-class.md): minimums and request windows are kept, features are suspended, and the deviation goes to the strategic review, which may restrict what is accepted or seek co-maintainers.
