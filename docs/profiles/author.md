---
tags:
  - profile
  - wip
index: "[Profiles](docs/profiles/_index.md)"
aliases:
  - Author profile
---
# Author

> [!QUESTION] Goal: which values configure the kernel for the author of a long work, who answers to an editor and to one contractual date?

> [!WARNING] Sketch
> This profile tests the generality of the kernel. No use has validated its values.

## Streams

| Stream | Yields | Triggered by | Allocation |
| --- | --- | --- | --- |
| Manuscript | results | `selection` | an exact share, the largest of the profiles |
| Note system and toolchain | means | `demand` | a share at most, low |
| Source reading | knowledge | `calendar` | a share at least |
| Craft | competence | `calendar` | a share at least |
| Editor and publicity | coordination | `appointment` | a reserve per event, at most, for each appointment that a task prepares |
| Administration | integrity | `accumulation` | none: the positions of low energy |
| Correspondence | coordination | `arrival` | a reserve, small |
| Planning | organization | `calendar` | a reserve per week, of at most `PT1H45M` by default |

## Types of deliverable

| Type | Description | Predictability | Starting phase | Review latency | Stages |
| --- | --- | --- | --- | --- | --- |
| `chapter` | advances one part of the book to the text delivered to the editor | `exploratory` | exploration | a few weeks, the latency of the editor | outline · draft · revision after the editor |
| `article` | publishes a piece drawn from the book | `routine` | delivery | the latency of the publication | draft · submission |

## Cadences

| Horizon | Author |
| --- | --- |
| Cycle | synchronized with the deliveries to the editor |

## Enabled mechanisms

| Mechanism | Setting |
| --- | --- |
| Reactive work | on, light |
| External parties | on: the editor is the party to whom the agent is accountable (`reviews`, `imposes`); interviewees and archives (`supplies`, with a latency) |
| Imposed deadlines | on: the delivery of the manuscript is a `hard` deadline on the purpose; the deliveries of parts agreed with the editor are deadlines on deliverables |
| Worth | ordinal |

## Notes specific to the domain

- **One buffer for the manuscript.** The deadline lies on the purpose, so its [buffer](../kernel/objects/deadline.md#^buffer) pools the margins of all chapters, and the deliveries of parts are tested with it in the [cumulative test](../kernel/processes/imposed-deadlines.md#^feasibility-test).
- **Reading has no natural end.** The passage from exploration to validation is a [transition of phase](../kernel/objects/phase.md) decided at a cycle planning. Afterwards, the reading that a chapter needs is charged to the chapter, in the stream Manuscript, and the minimum of the stream Source reading continues for reading not tied to a chapter.
- **Interviews are handed off first.** A request for an interview is made before the drafting that could run in parallel, by the [key of the hand-off](../kernel/processes/task-selection.md#^release-key).
