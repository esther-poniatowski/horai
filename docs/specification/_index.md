---
tags:
  - index
index: "[horai documentation](docs/_index.md)"
aliases:
  - Specification
---
# Specification

Documents the fields of each record of a plan and the views computed from them.

> [!WARNING] Status
> The records below state what the method requires of any implementation, including a set of notes kept by hand. The file formats of `horai` are not yet decided. A field marked with an option is required only when the profile turns that option on.

> [!IMPORTANT] Authored and computed fields
> Each field is either **authored**, a judgment or a fact that the agent records, or **computed**, a value that the tool derives from authored fields by a rule stated in the kernel. A computed field is never edited by hand, and a tool never writes an authored field. The column *Kind* of each table states which. ^authored-computed

## Configuration

- [Profile record](profile-record.md): documents the fields by which a profile configures the kernel

## Plan

- [Level records](milestone-record.md): documents the fields of a purpose, a deliverable, a milestone and a standing parent
- [Task record](task-record.md): documents the fields that a task adds to its identifier and its dependencies
- [Party record](party-record.md): documents the fields of an external party and of a wait
- [Calendar record](calendar-record.md): documents the cycles, the themes, the windows and the committed blocks

## Observation

- [Log record](log-record.md): documents the entries from which the estimates and the metrics are computed
- [Views](views.md): documents the three views of a plan and the question that each answers
