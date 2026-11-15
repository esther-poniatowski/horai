# CLI Reference

The commands of `horai` read the YAML records of one plan, check them, and print what the method computes from them. Only the commands `start` and `stop` write, and they write only clock entries. The plan is assumed to follow the [file layout](../specification/file-layout.md).

## Global Options

Every command is invoked on the plan that the configuration names:

```sh
horai [OPTIONS] COMMAND [ARGS]
```

| Option | Description |
| ------ | ----------- |
| `--version`, `-v` | Display the version and exit. |
| `--help` | Display the help message and exit. |

The commands that read a plan accept three common options:

| Option | Description | Default |
| ------ | ----------- | ------- |
| `--root`, `-r` | Folder from which the configuration file is searched, and against which its paths are resolved. | the environment variable `HORAI_ROOT`, then the nearest folder holding a configuration file, then the current folder |
| `--config`, `-c` | Configuration file at any path. | the environment variable `HORAI_CONFIG`, then `config/tools/horai.yml` or `horai.yml` under the root |
| `--date` | Day of the computation, in ISO 8601; `start` and `stop` take the moment `--at` instead. | today, in the time zone of the configuration |

The configuration file states five keys, each optional:

| Key | Value | Default |
| --- | --- | --- |
| `plan` | the central folder of the plan, relative to the root | the root |
| `roots` | the folders, relative to the root, under which the records of the hierarchy are found by their key `_schema`, beside what they concern | none |
| `exclude` | the patterns of paths, relative to a root, under which no record is sought; hidden folders are always skipped | none |
| `actions_file` | the name of the file in which every folder keeps its actions, the same in every folder | `TODO.yml` |
| `timezone` | the time zone of the agent, an IANA name | the local zone |

The configuration below serves a workspace whose central folder is `planning/`, and whose folders each ship their own records:

```yaml
_schema: horai:configuration@1
plan: planning
roots: [.]
exclude: [archive, templates]
timezone: Europe/Paris
```

## Exit Statuses

| Status | Meaning |
| ------ | ------- |
| 0 | The command succeeded. |
| 1 | `check` found at least one error. |
| 2 | The command line or the configuration is wrong, or a named task or stream does not exist. |

## Commands

### `check`

The check validates every file of the plan against the schema of its type, then the references between records: identifiers unique in the plan, references to existing records, at most one non-negotiable mark, the marks of each day, the budget and the rank of each item selected for the current cycle. It checks the calendar as well: the coherence of the allocations, the placement of the blocks and the appointments within the spans of the typical week, the time that the blocks give each stream against its allocation, the hours of high energy, the declared parties, the departures recorded for single dates, the absences, and, over the current week, the placement of the unplaced appointments and the blocks of the preparations. It reports a last weekly review older than seven days, a stream that holds committed work without an allocation, and a rule of recurrence that resolves to no period.

```sh
horai check [--format text|json] [--date DATE]
```

| Option | Description | Default |
| ------ | ----------- | ------- |
| `--format` | Format of the report. | `text` |

The text report gives one line per issue, with its severity, its rule, the file and the record concerned, and a final count. A file that fails its schema is excluded from every computation, and a reference to it is reported as excluded rather than missing.

### `next`

The command applies the selection rule to the tasks committed for the current week, and prints the candidates in tiers. Candidates of one tier are tied by the rule, and the choice among them is left to the agent.

```sh
horai next [--stream STREAM] [--date DATE]
```

| Option | Description | Default |
| ------ | ----------- | ------- |
| `--stream` | Stream of the current block. | the stream of the block of the week that holds the current moment |

While an item is marked non-negotiable, the candidates are its own tasks, and the stream is ignored. The notes under the tiers state why an item was excluded, such as a consumed budget awaiting its checkpoint decision.

### `view week`

The week view prints the calendar of the current week, which is the typical week changed by the departures of the week, then the committed tasks grouped by stream, with the remaining work of each item, the loose tasks and the marks of the day, the follow-ups due, the time spent against each reserve per week, and the task under way.

```sh
horai view week [--date DATE]
```

### `start`

The start mark records that work begins on a task, on a milestone or a question for work without a task, or on an appointment, for attending it. Starting a task stops the task under way; starting the task already under way changes nothing.

```sh
horai start TASK [--at MOMENT]
```

| Option | Description | Default |
| ------ | ----------- | ------- |
| `--at` | Moment of the mark, in ISO 8601; without an offset, the time zone of the configuration applies. | now |

The mark is appended to the clock file of its month, `log/clock/<month>.yml`, which is created when absent.

### `stop`

The stop mark records that work ends on the task under way. Without a task under way, the command changes nothing.

```sh
horai stop [--at MOMENT]
```

### `stages`

The command creates the milestone of each stage that an active deliverable has reached and that no milestone holds, as the [cycle planning](../procedures/cycle-planning.md) requires at a change of phase. Each milestone is named `<deliverable>-<stage>`, takes the predictability of its stage, or else that of the type, and is appended to the store of actions of the folder of its deliverable.

```sh
horai stages [--deliverable ID] [--stream STREAM] [--into FOLDER] [--dry-run]
```

| Option | Description | Default |
| ------ | ----------- | ------- |
| `--deliverable` | Identifier of the one deliverable to examine. | every active deliverable |
| `--stream` | Stream of the milestones whose deliverable has no stream shared by its milestones. | the stream shared by the milestones of the deliverable |
| `--into` | Folder whose store of actions receives the new milestones. | the folder of the deliverable; `plan/` for a deliverable of the central folder |
| `--dry-run` | List the missing stages without writing. | off |

The rest of the store is left as written. A deliverable whose milestones share no stream, without `--stream`, ends the command with the status 2.

### `info`

The diagnostic line gives the version of the package and the platform.

```sh
horai info
```
