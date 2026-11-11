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

| Stream | Role | Regime | Capacity |
| --- | --- | --- | --- |
| Features | production | `planned` | share |
| Build and infrastructure | enablement | `pulled` | ceiling |
| Ecosystem watch | sensing | `floor` | floor |
| Techniques | capability | `floor` | floor |
| Releases and community | interface | `calendar` | cap per release |
| Dependencies and debt | upkeep | `batched` | slots, and the cool-down |
| Issues and contributions | upkeep | `reactive` | reserve, the largest of the profiles |

## Names

| Kernel | Independent developer |
| --- | --- |
| Purpose · deliverable | project vision · release |
| Exploration · validation · delivery | prototype · stabilization · release |
| Cycle | the release cycle |
| Evidence note | the entry of the changelog, with what was tried and dropped |

## Options

| Option | Setting |
| --- | --- |
| Reactive work | on, heavy: kinds security report (`immediate`), defect and review of a contribution (`windowed`), feature request (`scheduled`, converted to the stream Features) |
| External parties | on: users (`requests`), contributors (`supplies`, and await a review), upstream projects (`supplies`, with a latency) |
| Imposed deadlines | rare: the disclosure date of a vulnerability |
| Valuation | ordinal, unless a sponsor or a client pays for a result |

## Notes specific to the domain

- **The queue is not the roadmap.** A feature request is of the class `scheduled`: it enters the backlog, and the [commitment states](../kernel/objects/commitment-state.md) keep it out of sight until a planning selects it.
- **A release date set by the maintainer is not a deadline,** by the [guard on self-set dates](../kernel/objects/deadline.md#^no-self-deadline), unless users rely on it once announced.
- **A contribution inverts the wait.** The contributor awaits a review by the agent, so the review is a request under a class of service, and its delay is a latency that the agent imposes on a party.
- **Recurrent issues pull enablement:** documentation, a template of issue, an automated check.
- **Degraded mode.** When the reserve leaves less than `discretion_min` of the week, the profile runs in the [degraded mode](../kernel/foundations/problem-class.md): floors and windows are kept, features are suspended, and the finding goes to the strategic review, which may restrict what is accepted or seek co-maintainers.
