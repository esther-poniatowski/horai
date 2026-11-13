# horai

[![Conda](https://img.shields.io/badge/conda-eresthanaconda--channel-blue)](docs/guide/installation.md)
![Maintenance](https://img.shields.io/maintenance/yes/2026)
[![Last Commit](https://img.shields.io/github/last-commit/esther-poniatowski/horai)](https://github.com/esther-poniatowski/horai/commits/main)
[![Python](https://img.shields.io/badge/python-%E2%89%A53.12-blue)](https://www.python.org/)
[![License: GPL](https://img.shields.io/badge/License-GPL--3.0-yellow.svg)](https://opensource.org/licenses/GPL-3.0)

Organizes tasks, priorities and schedules across the time scales of complex projects.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Overview

Horai records the tasks of complex projects, their priorities and their organization, and plans them across nested time horizons, by the method stated in [docs/](docs/_index.md). A plan is a folder of YAML records, which remain editable by hand and may be kept under version control.

> [!NOTE]
> The first increment reads and checks a plan, selects the next task, prints the view of the week, and records the time spent through start and stop marks.

---

## Features

- [x] **Checked records:** each file of a plan is validated against its schema, and the references between records are checked.
- [x] **Selection of the next task:** the selection rule orders the committed tasks, and reports ties.
- [x] **View of the week:** the calendar, the committed tasks with the remaining work of each item, and the follow-ups due.
- [x] **Time spent:** start and stop marks, from which the time spent and the remaining work are computed.
- [ ] **Planning sessions:** capture, weekly commitment, cycle planning and checkpoint decisions written by the tool.
- [ ] **Obsidian plugin:** live views and forms over the same records.

---

## Quick Start

### CLI

Run from the folder of a plan, the four commands below check the records, print the next task of the stream `P`, print the view of the week, and mark the start of work on a task:

```sh
horai check
horai next --stream P
horai view week
horai start fit-gating-model
```

The options and exit statuses of every command are listed in the [CLI reference](docs/guide/cli-reference.md).

### Application Programming Interface

```python
import horai

horai.info()
```

---

## Documentation

| Guide | Content |
| ----- | ------- |
| [Installation](docs/guide/installation.md) | Prerequisites, pip/conda/source setup |
| [Usage](docs/guide/usage.md) | Workflows and detailed examples |
| [CLI Reference](docs/guide/cli-reference.md) | Full command registry and options |
| [Configuration](docs/guide/configuration.md) | Configuration files, environment variables, precedence |
| [Architecture](docs/internals/architecture.md) | Design strategy, module organization, layers |

Full API documentation and rendered guides are also available at
[esther-poniatowski.github.io/horai](https://esther-poniatowski.github.io/horai/).

---

## Contributing

Contribution guidelines are described in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Acknowledgments

### Authors

**Author**: @esther-poniatowski

For academic use, the GitHub "Cite this repository" feature generates citations in
various formats. The [citation metadata](CITATION.cff) file is also available.

### Third-Party Dependencies

- **[Typer](https://typer.tiangolo.com/)** -- Command-line interface.

---

## License

This project is licensed under the terms of the
[GNU General Public License v3.0](LICENSE).
