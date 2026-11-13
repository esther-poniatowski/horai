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

The configuration file states four keys, each optional:

| Key | Value | Default |
| --- | --- | --- |
| `plan` | the central folder of the plan, relative to the root | the root |
| `roots` | the folders, relative to the root, under which the records of the hierarchy are found by their key `_schema`, beside what they concern | none |
| `exclude` | the patterns of paths, relative to a root, under which no record is sought; hidden folders are always skipped | none |
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

The check validates every file of the plan against the schema of its type, then the references between records: identifiers unique in the plan, references to existing records, at most one non-negotiable mark, the marks of each day, the budget and the rank of each item selected for the current cycle.

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

The week view prints the calendar of the current week, the committed tasks grouped by stream with the remaining work of each item and the marks of the day, the follow-ups due, and the task under way.

```sh
horai view week [--date DATE]
```

### `start`

The start mark records that work begins on a task, or on a parent for work without a task, such as attending an appointment. Starting a task stops the task under way; starting the task already under way changes nothing.

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

### `info`

The diagnostic line gives the version of the package and the platform.

```sh
horai info
```
