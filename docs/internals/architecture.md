# Architecture

The package `horai` reads the YAML records of a plan, validates them against their schemas, and computes from them what the method defines: the state of each task, the time spent, the remaining work, the selection of the next task, and the views. This note states how the package is divided, so that a change finds its single place.

## Layers

The package is divided into five layers. Each layer imports only the layers listed before it, so that the rules of the method never depend on files, on the clock or on the command line.

| Layer | Modules | Responsibility |
| --- | --- | --- |
| Domain | `domain/time.py`, `domain/records.py`, `issues.py` | the ISO 8601 notations, the typed records of a plan, and the issue reported by a check |
| Input and output | `io/yaml_loader.py`, `io/schemas.py`, `io/config.py`, `io/loader.py`, `io/clock_writer.py` | the reading of YAML, the validation against the schemas, the resolution of the configuration, the loading of a plan, and the appending of clock entries |
| Rules | `rules/state.py`, `rules/time_spent.py`, `rules/budgets.py`, `rules/selection.py`, `rules/checks.py` | pure computations on a loaded plan, given an explicit day or moment |
| Rendering | `render/text.py` | the text of the reports and of the views |
| Command line | `cli.py` | the commands, their options and their exit statuses |

## Schemas

The JSON Schema of each record type is a YAML file of `src/horai/data/schemas/`, shipped as package data. The definitions shared by several types, such as the identifier, the duration and the task, are written once in `common.schema.yml`, which the other schemas reference by its identifier. The schemas are the contract of the record formats: Ekphrasis builds its forms from the same files.

## Loading

A plan is loaded in three steps, and a file that fails one of them is excluded:

1. the YAML reader keeps dates, hours and durations as strings, and resolves only the scalar types of the YAML 1.2 core schema;
2. the key `_schema` must name the type that the folder of the file expects, and the content must satisfy that schema;
3. the name of the file must agree with the layout: a slug for a titled record, the opening date for a week, the month for a log.

The central folder is read at the paths of the layout. Under the roots that the configuration declares, a file is read only when its first lines name a schema of `horai`, so that the other YAML records of a workspace are not parsed. A record of the hierarchy found there is loaded as if it sat in its default folder; a central record found there is reported as misplaced.

The identifier of an excluded file joins the set `Plan.excluded`. A check reports a reference to it as excluded rather than missing, and a computation that needs it reports itself undefined.

## Rules

Each rule receives the plan and an explicit day, or the spans of work computed from the clock entries. No rule reads the clock, the environment or a file, so each rule is tested on a constructed plan. The commitment state, the remaining work and the selection follow the kernel notes cited in the docstrings of their modules. The selection returns tiers of tied candidates and never breaks a tie.

## Writing

The only writer of this version is `io/clock_writer.py`. It appends one line to the list `entries` of the clock file of the month, parses the result back, and replaces the file through a temporary file in the same folder. It refuses a file whose list `entries` is not the last key, so that a file edited by hand is never rewritten.
