---
tags:
  - specification
  - wip
index: "[Specification](docs/specification/_index.md)"
aliases:
  - File layout
  - Record formats
---
# File layout

> [!QUESTION] Goal: in which file is each record of a plan stored, and which conventions does every file follow?

## Layout

A plan is a folder of YAML files. Each record type has one place, and the fields of each type are documented in its record note.

| Path | Record | Schema |
| --- | --- | --- |
| `horai.yml`, by default | configuration of the tool: the paths of the plan and the time zone | `horai:configuration@1` |
| `profile.yml` | [profile](profile-record.md) | `horai:profile@1` |
| `availability.yml` | [availability](availability-record.md) | `horai:availability@1` |
| `plan/purposes/<id>.yml` | a [purpose](milestone-record.md) | `horai:purpose@1` |
| `plan/deliverables/<id>.yml` | a [deliverable](milestone-record.md) | `horai:deliverable@1` |
| `plan/milestones/<id>.yml` | a [milestone](milestone-record.md), with its tasks | `horai:milestone@1` |
| `plan/questions/<id>.yml` | a question, with its tasks | `horai:question@1` |
| `plan/standing/<id>.yml` | a standing parent, with its tasks | `horai:standing@1` |
| `calendar/week-template.yml` | the [week template](calendar-record.md) | `horai:week-template@1` |
| `calendar/cycles/<id>.yml` | a cycle | `horai:cycle@1` |
| `calendar/weeks/<opened>.yml` | a week, named by the date of the review that opened it | `horai:week@1` |
| `calendar/appointments/<id>.yml` | an appointment | `horai:appointment@1` |
| `capture/inbox.yml` | the [inbox](capture-record.md) | `horai:inbox@1` |
| `capture/holding.yml` | the holding file | `horai:holding@1` |
| `capture/ideas.yml` | the ideas file | `horai:ideas@1` |
| `capture/archive.yml` | the archive | `horai:archive@1` |
| `log/clock/<month>.yml` | the [clock entries](log-record.md) of one month | `horai:clock-log@1` |
| `log/decisions/<month>.yml` | the decision entries | `horai:decision-log@1` |
| `log/deviations/<month>.yml` | the deviation entries | `horai:deviation-log@1` |
| `log/requests/<month>.yml` | the request entries, under the option of reactive work | `horai:request-log@1` |
| `log/adjustments/<month>.yml` | the adjustment entries, under the option of imposed deadlines | `horai:adjustment-log@1` |
| `parties/<id>.yml`, `waits/<id>.yml` | a [party and a wait](party-record.md), under the option of external parties | `horai:party@1`, `horai:wait@1` |

## Conventions

- **Configuration file.** The configuration of the tool is read from `horai.yml` at the root of the plan by default, or from `config/tools/horai.yml`, as the [conventions of the command line](../internals/cli-conventions.md) state; both at once is an error. Any other path is given by the option `--config`, or by the environment variable `HORAI_CONFIG`, which the plugin sets from its settings.
- **One record per file.** Each file is a mapping whose first key is `_schema`, and a list of entries is the value of a key of that mapping. The form of each file in Ekphrasis is generated from the schema of its type.
- **Identifiers.** The identifier of a record that has a title is the slug of that title, fixed at creation and unique in the plan. `check` reports a duplicate, which the agent resolves by changing one of the titles. A cycle bears an identifier of its own, and a week is identified by the date of the review that opened it. The identifier of a record of its own file names that file, and the identifier of a task is a field of the task.
- **References.** A field that refers to another record holds the identifier of that record, in the form of a logical target of [Anagraphe](https://github.com/esther-poniatowski/anagraphe), with the repository omitted inside one plan. Anagraphe checks these references and makes them navigable.
- **Dates and durations.** Dates follow ISO 8601 (`2026-11-13`), timestamps carry their offset (`2026-11-13T09:02+01:00`), and durations follow ISO 8601 (`PT4H`, `PT1H30M`).
- **Computed fields are not stored.** A field of the kind *computed* is derived on each read, and no file holds it. The time spent on each task is derived from the clock entries in this way.
- **Logs per month.** The entries of each kind are split by month, so that a log file stays short.
- **Kind of an item.** The field `kind` of a milestone or a question repeats what its schema states, so that a reader of the file sees it. `check` reports a `kind` that disagrees with the schema.
- **Views are not files.** The views are shown by the plugin, and printed by the command line on demand; no view is written into the plan.

## Example

A milestone with its tasks:

```yaml
_schema: horai:milestone@1
title: Fit of the gating model to the recorded population
deliverable: ctx-geometry
stream: inquiry
kind: milestone
done: the fitted model reproduces the three recorded geometries within the noise
status: open
variance: exploratory
budget: PT12H
cycle: 2026-c6
rank: 1
tasks:
  - id: fit-gating-model
    title: Fit the gating model to the recordings
    committed_week: 2026-11-09
    risk: true
  - id: compare-geometries
    title: Compare fitted and recorded geometries
    depends_on: [fit-gating-model]
```
