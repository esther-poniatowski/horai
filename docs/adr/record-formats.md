---
tags:
  - decision
status: accepted
created: 2026-11-13
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Record formats
---
# Record formats

> [!QUESTION] Goal: in which files and notations are the records of a plan stored, so that they are read by the tool and filled through Ekphrasis?

## Decision

- **YAML only.** Every record is a YAML file, a mapping whose first key is `_schema`. It is viewed and edited through the plugin of `horai` or through [Ekphrasis](https://github.com/esther-poniatowski/ekphrasis), which builds a form from the schema of each type.
- **One file per object.** Each purpose, deliverable, milestone, question, standing parent, cycle, week, appointment, party and wait is its own file, named by its identifier. The tasks are a list in the file of their parent.
- **Folders by record type.** The parent of a record is a field, and never a path.
- **Logs.** One file per kind of entry and per month.
- **Capture.** One file each for the inbox, the holding file, the ideas file and the archive.
- **Notation.** Dates, timestamps and durations follow ISO 8601. References hold logical targets of Anagraphe, with the repository omitted inside one plan.
- **Kind.** A milestone or a question states its `kind`, which repeats its schema for the reader and is checked against it.
- **Views in the plugin only.** No view is written into the plan.

The paths are listed in the [file layout](../specification/file-layout.md).

## Constraints that decide the formats

- **A plain-text source in YAML,** as the [constraints of the software](software-constraints.md) require.
- **One form per file in Ekphrasis.** A file holds one record, and its type fixes its schema.
- **One machine.** The software is used on one machine. A plan may be kept under version control, which the plain files allow.

## Options weighed

- **Markdown notes with YAML frontmatter or blocks.** Rejected: the author prefers YAML, and the forms of Ekphrasis replace the editing of notes.
- **One file per deliverable or per purpose.** Rejected: a large form, which every edit of a task rewrites.
- **Durations as `4h` or in minutes.** Rejected in favor of a standard notation, at some cost in readability.
- **Views written as Markdown.** Not adopted: the views stay in the plugin, so that no generated file enters the plan.

## Consequences

- No view is readable on a mobile device until Ekphrasis or a plugin runs there.
- The JSON Schema of each record type is the contract shared by `horai`, its plugin, Ekphrasis and Anagraphe.
