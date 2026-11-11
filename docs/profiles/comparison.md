---
tags:
  - profile
index: "[Profiles](docs/profiles/_index.md)"
aliases:
  - Comparison of instances
---
# Comparison of instances

> [!QUESTION] Goal: what do the instances of the problem share, and on which dimensions do they differ?

The levels below are qualitative judgments, and none is measured.

## Streams by role

| Role | Research | Solo founder | Independent developer | Author | Consultant |
| --- | --- | --- | --- | --- | --- |
| Production | results of papers | product | features | manuscript | client deliverables |
| Enablement | research tools | internal tooling | build and infrastructure | note system, toolchain | templates, process |
| Sensing | bibliography | customer and market discovery | ecosystem watch | source reading | market watch |
| Capability | mathematics | new skills | new techniques | craft | upskilling |
| Interface | supervision, lab meetings | investors, partners | releases, community | editor, publicity | proposals, client meetings |
| Upkeep | vault, defects | administration | dependencies, debt | administration | accounting |
| Reactive stream | correspondence | customer support | issues, contributions | correspondence | client requests |
| Duty | teaching, if assigned | — | — | — | — |

## Modulators

| Modulator | Research | Solo founder | Independent developer | Author | Consultant |
| --- | --- | --- | --- | --- | --- |
| Reactive load | low | medium | high | low | medium to high |
| External dependence | medium: supervisor, co-authors, reviewers | medium: customers, contractors | medium: upstream projects, contributors | medium: editor, interviewees | high: clients, subcontractors |
| Imposed deadlines | few, hard: submissions | few: the runway, as a resource deadline on the purpose | rare | one, contractual, on the purpose | many, contractual |
| Committed capacity | none, or teaching | none | none | none | retainers, time sold |
| Delegation | automated agents | contractors | rare | rare | subcontractors |
| Principals | one | several investors, or none | none, or a sponsor | one | one per engagement |
| Quantifiable cost | no | yes: revenue and burn | rarely | no | yes: fees and penalties |

## Names of the dimensions

| Dimension | Research | Solo founder | Independent developer | Author | Consultant |
| --- | --- | --- | --- | --- | --- |
| Purpose | thesis | company goal | project vision | book | practice |
| Deliverable | paper | offer or release | release | part or chapter | engagement |
| Exploration | exploration | problem discovery | prototype | research | scoping |
| Validation | understanding | solution validation | stabilization | argument | proposal |
| Delivery | distillation | scaling | release | drafting and revision | delivery |
| Evidence note | read by the supervisor | investor update | changelog entry | note to the editor | status report to each client |

## Characteristic failure

Each instance has its form of the displacement of ends by means, and a second failure that its dominant modulator produces.

| Profile | Means displace ends | Second failure | Rule of the kernel that bears on it |
| --- | --- | --- | --- |
| Research | tools built for days without a result | learning and reading receive no time | [pull rule](../kernel/processes/enablement.md#^pull-rule), [floors](../kernel/processes/capacity-allocation.md#^floors) |
| Solo founder | a platform built before the product is wanted | discovery stops once building starts | [phase](../kernel/objects/phase.md), [stop by value](../kernel/processes/uncertainty-control.md#^stop-by-value) |
| Independent developer | an engine built instead of the application | the queue of issues becomes the roadmap | [reserve and triage](../kernel/processes/reactive-work.md) |
| Author | a note system refined instead of the text | reading without end before drafting | [manual first](../kernel/processes/enablement.md#^manual-first), [phase](../kernel/objects/phase.md) |
| Consultant | templates polished between engagements | all capacity is sold, and the floors vanish | [feasibility test](../kernel/processes/imposed-deadlines.md), [floors](../kernel/processes/capacity-allocation.md#^floors) |

## Domains at the boundary

The second review tested further domains against the kernel:

| Domain | Fit | What it required |
| --- | --- | --- |
| Doctoral researcher with teaching | fits | the role duty, under the regime `committed` |
| Clinician-scientist | fits, near the boundary | the regime `committed` for the rota, `immediate` requests for on-call, and the check of `discretion_min` |
| Parent-carer with a side project | fits | the [availability](../kernel/objects/availability.md) with a short minimum block, and slots in place of themes |
| Freelance designer | fits | several principals, review loops and dates set by clients |
| Principal investigator of a lab | partly | the relation `delegates` covers the work handed to members; the allocation of the work of the lab is outside the kernel |

## What the comparison shows

- **The six roles occur in every instance.** The differences lie in the regimes, the capacities and the modulators, which supports their separation in the [dimensions](../kernel/foundations/dimensions.md).
- **Each modulator dominates one instance.** Reactive load dominates the developer, deadlines and cost the consultant, cost and a single hard deadline the founder. Research and authorship are the instances closest to the [minimal core](../kernel/foundations/core-and-options.md#^core).
- **The floors are hardest to keep where cost is quantified.** A billable hour has an observed price and an hour of capability has none, which is the case that the ninth [commitment](../kernel/foundations/commitments.md#^c-valuation) addresses.
