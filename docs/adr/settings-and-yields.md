---
tags:
  - decision
status: accepted
created: 2026-11-14
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Settings folder
  - Several yields
---
# Settings folder and yields

> [!QUESTION] Goal: where do the settings of a plan sit apart from its records, and which outcomes can a stream yield?

The tree of a plan mixed settings with records: `calendar/` held the typical week, which the rules read as a parameter, beside the cycles and the dates, which are records. While filling the profile of the pilot, the author found three defects in the yields. Upkeep and planning shared the yield `continuity`, although they give different outcomes. The follow-up of conferences gives both knowledge and a network, whereas a stream bore one yield. The name `continuity` did not say continuity of what.

## Decision

- **Settings folder.** The folder `settings/` holds the three settings of a plan: `profile.yml`, `parties.yml` and `typical-week.yml`. The other folders hold records: `plan/`, `calendar/` (cycles and dates), `capture/` and `log/`.
- **Several yields.** The field `yields` of a stream is a list of one or several outcomes. The rule of exclusivity is retired: a task still belongs to one stream, so its time is counted once.
- **Values.** Nine yields are distinguished: `results`, `means`, `knowledge`, `competence`, `network`, `coordination`, `organization`, `integrity` and `obligation`.
  - `network` builds the relations with the people of the field, for future collaboration; its payoff is deferred, like that of knowledge and competence.
  - `organization`, the yield of planning, organizes the work: it chooses what is worked on, and checks its course.
  - `integrity`, the yield of upkeep, in place of `continuity`, keeps the working system whole and correct: it repairs its defects and updates its parts.

## Constraints that decide the formats

- **A setting and a record have different lifetimes.** A setting is rewritten when the situation changes, whereas a record accumulates.
- **A yield names what the work gives the agent,** read without the glossary, in every profile of the method.
- **A field reads the same in every case.** `yields` is a list even for one value.

## Options weighed

- **Settings at the root of the plan.** Rejected: the boundary would be a convention that the reader must know.
- **The cycles and the dates in `plan/`.** Rejected: `calendar/` names the records of time well enough once the typical week leaves it.
- **One yield per stream, with the rule of exclusivity.** Rejected by the author: a stream may give several outcomes, and the allocation is per stream in any case.
- **`direction`, `plan` or `control` for planning; `consistency` or `maintenance` for upkeep.** Rejected: `plan` leaves out the review of the course, `control` collides with the control questions of the kernel, `consistency` is narrow outside a vault, and `maintenance` names the act.

## Consequences

- The loader reads the settings in `settings/`; the paths of the issues follow.
- The profile schema takes `yields` as a list of the nine values.
- The kernel note on streams, the usual pairings, the dimensions and the profiles state the nine yields.
- This decision replaces the single yield and the values of the decision on [explicit names](explicit-names.md).
