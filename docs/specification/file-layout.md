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

A plan is a set of YAML files, whose fields are documented in the record notes. The records that describe the agent sit in one central folder, at the paths below. The records of the hierarchy may also sit beside what they concern, in any folder under the roots that the configuration declares, and are found by their key `_schema`, as the decision on [distributed records](../adr/distributed-records.md) states. The paths below are then their default places. The folder `settings/` holds the settings that the rules read as parameters; every other folder holds records, as the decision on [settings and yields](../adr/settings-and-yields.md) states.

| Path | Record | Schema |
| --- | --- | --- |
| `horai.yml`, by default | configuration of the tool: the central folder of the plan, the roots under which records are found, and the time zone | `horai:configuration@1` |
| `settings/profile.yml` | [profile](profile-record.md) | `horai:profile@1` |
| `settings/parties.yml` | the [parties](party-record.md): each declared party, with an identifier, a name, and optionally its relations and classes of service | `horai:parties@1` |
| `plan/purposes/<id>.yml` | a [purpose](milestone-record.md) | `horai:purpose@1` |
| `plan/deliverables/<id>.yml` | a [deliverable](milestone-record.md) | `horai:deliverable@1` |
| `plan/TODO.yml` | the store of actions of the central folder: [milestones and questions](milestone-record.md) with their tasks, and [loose tasks](task-record.md), each with its `id` | `horai:actions@1` |
| `settings/typical-week.yml` | the [typical week](typical-week-record.md) | `horai:typical-week@1` |
| `calendar/cycles/<id>.yml` | a [cycle](calendar-record.md) | `horai:cycle@1` |
| `calendar/dates/<month>.yml` | the [dates](calendar-record.md) of a month: the departures of single dates from the typical week, and the absences that start in the month | `horai:dates@1` |
| `capture/inbox.yml` | the [inbox](capture-record.md) | `horai:inbox@1` |
| `capture/holding.yml` | the holding file | `horai:holding@1` |
| `capture/ideas.yml` | the ideas file | `horai:ideas@1` |
| `capture/archive.yml` | the archive | `horai:archive@1` |
| `log/clock/<month>.yml` | the [clock entries](log-record.md) of one month | `horai:clock-log@1` |
| `log/reviews/<month>.yml` | the [weekly reviews](log-record.md) held in one month | `horai:review-log@1` |
| `log/decisions/<month>.yml` | the decision entries | `horai:decision-log@1` |
| `log/deviations/<month>.yml` | the deviation entries | `horai:deviation-log@1` |
| `log/requests/<month>.yml` | the request entries, under the option of reactive work | `horai:request-log@1` |
| `log/adjustments/<month>.yml` | the adjustment entries, under the option of imposed deadlines | `horai:adjustment-log@1` |
| `waits/<id>.yml` | a [wait](party-record.md), under the option of external parties | `horai:wait@1` |

## Conventions

- **Configuration file.** The configuration of the tool is read from `horai.yml` at the root of the plan by default, or from `config/tools/horai.yml`, as the [conventions of the command line](../internals/cli-conventions.md) state; both at once is an error. Any other path is given by the option `--config`, or by the environment variable `HORAI_CONFIG`, which the plugin sets from its settings.
- **One record per file, one store per folder.** Each file is a mapping whose first key is `_schema`, and a list of entries is the value of a key of that mapping. The form of each file in Ekphrasis is generated from the schema of its type. A folder keeps all its actions in one store, a file named by the configuration key `actions_file`, `TODO.yml` by default, the same in every folder; `check` reports a store under another name.
- **Identifiers.** An identifier is a slug, fixed at creation and unique in the plan; `check` reports a duplicate. A purpose, a deliverable and a cycle are named by their file. An item and a task of a store state their identifier in their field `id`, so that the name of the store says nothing of its content.
- **References.** A field that refers to another record holds the identifier of that record, in the form of a logical target of [Anagraphe](https://github.com/esther-poniatowski/anagraphe), with the repository omitted inside one plan. Anagraphe checks these references and makes them navigable.
- **Dates and durations.** Dates follow ISO 8601 (`2026-11-13`), timestamps carry their offset (`2026-11-13T09:02+01:00`), and durations follow ISO 8601 (`PT4H`, `PT1H30M`).
- **Computed fields are not stored.** A field of the kind *computed* is derived on each read, and no file holds it. The time spent on each task is derived from the clock entries in this way.
- **Logs per month.** The entries of each kind are split by month, so that a log file stays short.
- **Unknown record types.** A file under a root whose key `_schema` names a type of horai that the tool does not know is reported by `check`, and is not read.
- **Views are not files.** The views are shown by the plugin, and printed by the command line on demand; no view is written into the plan.

## Example

A store of actions with one milestone and one loose task:

```yaml
_schema: horai:actions@1
milestones:
  - id: ctx-population-fit
    title: Fit of the gating model to the recorded population
    deliverable: ctx-geometry
    stream: inquiry
    success_criteria:
      - the fitted model reproduces the three recorded geometries within the noise
    status: open
    cycle: 2026-c6
    predictability: exploratory
    budget: PT12H
    rank: 1
    tasks:
      - id: fit-gating-model
        action: Fit the gating model to the recordings
        riskiest: true
        committed_week: 2026-11-09
        started: 2026-11-12
      - id: compare-geometries
        action: Compare fitted and recorded geometries
        depends_on: [fit-gating-model]
tasks:
  - id: chapter-3-exercises
    action: Work the exercises of chapter 3
    stream: training
```
