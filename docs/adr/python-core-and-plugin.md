---
tags:
  - decision
status: accepted
created: 2026-11-12
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Python core and Obsidian plugin
  - Architecture of the software
---
# Python core and Obsidian plugin

> [!QUESTION] Goal: where does a plan live, and how are its rules computed and its views shown, for one researcher working on desktop machines?

## Decision

- **Own vault.** A plan lives in a vault of its own, separate from the other notes of the agent.
- **Standalone.** The software depends on no Obsidian plugin for tasks, and provides its own Obsidian plugin.
- **Desktop only.** The plugin runs on desktop machines. On a mobile device, the records of the plan are read and edited through Ekphrasis, once Ekphrasis runs there. Until then, the plan is used on desktop only.
- **Python core, thin plugin.** All rules are computed by a Python package, which has a command line of its own. The plugin holds no rule: it shows the views and collects the inputs of the agent, and calls a local Python process for every computation.

## Constraints that decide the architecture

- **One home per rule.** A rule computed in two languages would be stated twice, and would drift.
- **The rules are numerical.** The calibration, the slacks and the selection rule are tested more easily in Python than in TypeScript.
- **A plugin for tasks fixes a task notation.** A standalone tool keeps the record formats under the control of the method.

## Options weighed

- **The Obsidian Tasks plugin as the notation.** Rejected for the third constraint.
- **All logic in TypeScript, in the plugin.** Rejected for the first two constraints, and because the command line would need a second implementation.
- **Mobile support.** Rejected: a desktop plugin can call a local process, whereas a mobile plugin cannot.

## Consequences

- The plugin must find the Python environment, restart the process after a failure, and refuse a version of the protocol that it does not know.
- The command line and the plugin share one application layer.
