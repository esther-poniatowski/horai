---
tags:
  - reference
index: "[References](docs/references/_index.md)"
aliases:
  - Kanban and Lean pull
  - Work-in-progress limit
---
# Kanban and Lean pull

Kanban is a method for managing the flow of knowledge work, adapted by Anderson from Lean manufacturing [anderson2010]. Benson and Barry adapted it to the work of one person [benson2011].

## Method

- **Pull.** A piece of work starts when a downstream stage has capacity for it or demands its output, and not when it becomes available upstream.
- **Commitment point.** A board separates the options that are recorded from the work that is committed. The promise starts at the commitment point.
- **Limit on work in progress.** Each stage holds a bounded number of items, so that work is finished before new work starts.

Two neighboring heuristics of software practice bear on the same question. The *rule of three* admits a duplication twice and calls for an abstraction at the third occurrence [fowler1999]. The *walking skeleton* is the smallest end-to-end implementation of a system, built before any part is completed [cockburn2004].

## Bearing on `horai`

- The [commitment states](../kernel/objects/commitment-state.md) apply the commitment point.
- The [pull rule](../kernel/processes/enablement.md#^pull-rule), the manual route and the thin slice apply pull, the rule of three and the walking skeleton to enablement.
- The limit of three papers in the [reading pipeline](../modules/bibliography/reading-pipeline.md#^pipeline) is a limit on work in progress. The review of 2026-11-11 found no controlled evidence on such limits for one person, so the value is a default.

## Sources

- [anderson2010] ○ Anderson, *Kanban: Successful Evolutionary Change for Your Technology Business*, Blue Hole Press, 2010
- [benson2011] ○ Benson and Barry, *Personal Kanban: Mapping Work, Navigating Life*, Modus Cooperandi Press, 2011
- [fowler1999] ○ Fowler, *Refactoring: Improving the Design of Existing Code*, Addison-Wesley, 1999
- [cockburn2004] ○ Cockburn, *Crystal Clear: A Human-Powered Methodology for Small Teams*, Addison-Wesley, 2004
