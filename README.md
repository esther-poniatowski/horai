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

Horai is intended to record the tasks of complex projects, their priorities and their organization, and to schedule them across nested time horizons. Tasks and schedules are stored as plain-text files in the project folder, so they remain editable by hand and versioned with git.

> [!NOTE]
> The repository is initialized from the Keystone template. No feature is implemented yet: the package exposes only the `info` command and the `--version` option.

---

## Features

- [ ] **Task records:** plain-text records of tasks, read and validated by the tool.
- [ ] **Priorities:** ordering of tasks by importance and urgency.
- [ ] **Organization:** grouping of tasks by project and decomposition into subtasks.
- [ ] **Multi-scale scheduling:** plans at several time horizons, kept consistent with one another.

---

## Quick Start

### CLI

```sh
horai --help
```

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
