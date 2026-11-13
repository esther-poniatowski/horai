---
tags:
  - handoff
index: "[horai documentation](docs/_index.md)"
aliases:
  - Handoff
---
# Handoff

The handoff carries the state of the development of horai from one agent session to the next. Each session reads it first, works on the open step of the [roadmap](../TODO.md), checks the steps that it completes there, and updates this note before ending.

## Task state

Increment 1 is implemented: the commands `check`, `next`, `view week`, `start` and `stop` run on a plan in the [file layout](specification/file-layout.md), as the [CLI reference](guide/cli-reference.md) states. Its exit criterion, one week of use on the plan of the author, is open.

The author decided to apply horai in the research workspace Geonexus, whose folders each ship their own list of open actions. The decisions are recorded in the decision on [distributed records](adr/distributed-records.md) and applied to the notes; their implementation is the open section of the roadmap. No plan of the author exists yet.

## Active constraints

- **Accepted decisions.** The records of status `accepted` in the [decision index](adr/_index.md) bind every change. A choice that departs from one of them is put to the author before it is applied.
- **Ratification first.** Each increment opens with the decisions that it needs, asked to the author one by one, and recorded before code is written.
- **Environment.** Python tools run through `conda run -n horai python -m …`; the bare command `pytest` resolves outside the environment.
- **Geonexus.** A change in Geonexus follows its own [instructions for agents](../../../research/geonexus/AGENTS.md), its rule on task tracking, and its commit gate `elenchos check`.

## Open questions

- **Roots.** The configuration key that declares the roots, and whether the central folder of Geonexus is `planning/` or another folder, are settled with the amendment of the rule on task tracking of Geonexus.
- **Migration.** The 51 dependencies of the Geonexus lists that name no identifier are repaired, or dropped, as each area migrates.

## Provenance

- The method: the notes of [docs/](_index.md), and the accepted decision records.
- The task lists of Geonexus, measured by a script of the ignored workspace `.agent-tmp/`, which also holds the proposals and the review sheet that preceded the ratification.
- The siblings consulted: Ekphrasis for forms built from schemas, Anagraphe for logical targets, Gnomon for the conventions of schemas.

## Decision log

The decisions of the author are recorded in the accepted records of the [decision index](adr/_index.md): scope, constraints of the software, architecture, commitments, ontology, record formats and core rules. Two later choices are recorded in the notes that they changed: weekends are planned as ordinary blocks, and the streams of the research profile are identified by slugs.
