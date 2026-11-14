---
tags:
  - decision
status: accepted
created: 2026-11-13
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Explicit names
  - Naming criterion
---
# Explicit names

> [!QUESTION] Goal: which names do the fields of the records and their values take, so that an author reads a record without the glossary?

The terms "theme", "enablement", "capability", "cycle", "role" and "regime" were each questioned by the author, and the first four were corrected one at a time. The defect is one class: a name that states a category of the method instead of the question that the field answers, such as `role`, `regime`, `kind` or `options`, or an everyday word given a meaning of its own, such as `floor`, `standing`, `held` or `releases`.

> [!WARNING] Partly replaced
> The decision on [streams, allocation and loose tasks](streams-allocation-and-loose-tasks.md) replaces the names `worth: {by}` and `permanent-area`, and the forms of allocation. The decision on [properties apart from the trigger](properties-apart-from-the-trigger.md) replaces the placement of energy by trigger, which justified the removal of `slots`. The decision on [dates, reviews and recurring tasks](dates-reviews-and-recurring-tasks.md) retires the record of the week and its field `starts_on`. The decision on [settings and yields](settings-and-yields.md) makes `yields` a list, and replaces the value `continuity`.

## Decision

- **Criterion.** A field name, read with its value in a record, states what the value means without the glossary. The criterion binds the keys and the values alike. It complements the rule of terms of the [alignment with the time-management course](time-management-alignment.md), which takes a term of the references where one exists.
- **Renames.** The names of the tables below replace the current ones. A name absent from the tables is kept, such as `title`, `deadline`, `budget`, `importance`, `steps`, `scheduled`, `committed_week`, `depends_on`, `prepares`, `non_negotiable` and `overhead`.
- **Names kept after weighing.** The author kept `rank`, `appointed` and `predictable`, and the name of the procedure "weekly review", which is the term of Getting Things Done.

### Stream

| Current | New | Question answered |
| --- | --- | --- |
| `role: production` · `tooling` · `survey` · `training` · `exchange` · `upkeep` · `duty` | `yields: results` · `means` · `knowledge` · `competence` · `coordination` · `continuity` · `obligation` | what does the work give the agent? |
| `regime: planned` · `pulled` · `floor` · `batched` · `reactive` · `appointed` | `triggered_by: selection` · `demand` · `calendar` · `accumulation` · `arrival` · `appointment` | what prompts the work? |
| `capacity` | `allocation` | which part of the plannable time does the stream receive? |
| `ceiling: 0.15` · `floor: 0.2` | `at_most: 0.15` · `at_least: 0.2` | which bound holds on its share of time? |
| `slots: true` | removed: a stream triggered by accumulation always takes the low-energy slots | — |
| `share: 0.04, cap: PT3H` of a stream triggered by appointment | `preparation: {share: 0.04, cap_per_appointment: PT3H}` | how much time prepares the appointments? |

### Profile

| Current | New | Question answered |
| --- | --- | --- |
| `options` | `enabled_mechanisms` | which optional mechanisms run? |
| `valuation: {scale: ordinal}`, or `{scale: quantified, unit, cost_of_capacity}` | `worth: {by: rank}`, or `{by: amount, unit, worth_per_hour}` | how is the worth of a milestone stated, and what is one hour of the agent worth in that unit? |

### Items

| Current | New | Question answered |
| --- | --- | --- |
| record type `standing` | `permanent-area` | which permanent parent holds recurring and loose work? |
| `kind: milestone` · `question` | removed: the type of the record already states it | — |
| `done` | `done_when` | which test judges completion? |
| `variance: routine` · `exploratory` | `predictability: routine` · `exploratory` | how predictable is the duration of the work? |
| `consumers` | `consumed_by` | which milestones consume the output of a tooling item? |
| `principal` | `accountable_to` | to which party does the agent answer for the deliverable? |
| `status: waiting-admission` | `status: awaiting-admission` | is the deliverable waiting for the strategic review to admit it? |
| deadline `kind: hard` · `soft` | deadline `strictness: hard` · `soft` | does missing the date lose the result, or only decay its value? |

### Tasks

| Current | New | Question answered |
| --- | --- | --- |
| `today: 2026-11-16 main` | `marked_for: 2026-11-16`, and `main_objective: true` | for which day is the task marked, and is it the main objective? |
| `held` | `held_since` | since when has the task waited in the holding file? |
| `waiting` | `follow_up` for a date, and `awaits` for the identifier of a wait | when is the party reminded, or which wait blocks the task? |
| `releases: true` | `hands_off: true` | does completing the task start the delay of a party? |
| `risk: true` | `riskiest: true` | is it the riskiest task of its parent? |

### Calendar and logs

| Current | New | Question answered |
| --- | --- | --- |
| week `opened` | `starts_on` | on which day does the week start, the day of its weekly review? |
| `windows` | `request_windows` | which spans receive the requests of others? |
| clock entry `assigned: true` | `recalled: true` | was the span stated from memory instead of marked live? |
| decision entry `decision` | `checkpoint_decision` | what was decided when the budget was consumed? |

## Consequences

- The kernel notes, the specification and the procedures adopt the new names in the same change as the schemas. The terms of the method in prose follow the field values: a stream "triggered by the calendar" replaces a "floor stream".
- The format change of the [typical week and the types of deliverable](typical-week-and-deliverable-types.md) applies these renames in the same migration, so that every record is migrated once.
