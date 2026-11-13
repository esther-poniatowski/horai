---
tags:
  - decision
status: accepted
created: 2026-11-12
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Constraints of the software
  - Plain-text source of truth
---
# Constraints of the software

> [!QUESTION] Goal: which constraints does every part of `horai` respect, whatever its function?

## Decision

1. **Plain text.** A plan is held in plain-text files that the agent can read and edit by hand, and these files are its only source of truth. A cache may be derived from them, and is never authoritative. Among plain-text formats, YAML is preferred to Markdown wherever the record allows it.
2. **No dependency on a synchronization tool.** The software reads and writes plain files only. The agent synchronizes them between machines by any means, such as git or a file-synchronization service, and the software never requires git.
3. **No inference at run time.** Every output follows from a rule stated in the notes, and is reproducible from the files. No language model or learned model takes part at run time.
4. **One agent, local.** The software serves one person on that person's own machines, with no server, no accounts, and no database as source of truth. Collaborators enter a plan only as [external parties](../kernel/objects/external-party.md).

## Constraints that decide them

- **The plan must outlive the tool.** A plan in plain text remains readable and editable without `horai`.
- **A researcher's tools differ across machines.** Requiring git would exclude a plan synchronized otherwise.
- **The method separates judgments from computations.** A run-time model would produce results that no stated rule fixes, contrary to the [authored and computed boundary](../specification/_index.md#^authored-computed).

## Options weighed

- **Git as a requirement.** Rejected for the second constraint. A plan kept under git remains supported.
- **A model that proposes without deciding.** Rejected for the third constraint.

## Consequences

- No feature may rely on the history of a version-control system.
- The software is used on one machine for now. Use across several machines is out of scope until a need arises.
- The record formats take YAML as the default, and each record kept in Markdown must state the reason.
