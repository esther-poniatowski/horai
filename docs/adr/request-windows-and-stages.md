---
tags:
  - decision
status: accepted
created: 2026-11-14
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Request windows as blocks
  - Stage milestones
---
# Request windows and stages

> [!QUESTION] Goal: how are the request windows placed, and how does a stage of a deliverable become a milestone, so that each object has one form and one identity?

A review of the framework found two objects without a form of their own. A request window was an entry of the typical week apart from the blocks, and named no stream. Every stream triggered by arrival was measured against the whole time of the windows, so two such streams counted it twice, and the command `next` stopped inside a window. The stages of a type of deliverable were named by generic titles, such as `draft`, whereas the identifier of a milestone is unique in the plan. No milestone recorded its stage, the type gave one predictability to all its stages, and no procedure or command created the milestones of the stages.

## Decision

- **Request windows.** A request window is a block of a stream triggered by arrival. The entry `request_windows` is retired from the typical week and from the dates. In such a block, the selection offers the tasks of its stream, then the tasks of any other stream that hand off to a party.
- **Identity of a stage.** A stage has an identifier, `id`, in place of its `title`. The milestone of a stage is named `<deliverable>-<stage>`, and names the stage in its field `stage`. The check reports a stage that the deliverable lacks, and a milestone of a stage that bears another name.
- **Defaults of a stage.** A stage may state its `predictability` and its `prior_margin`, which replace those of its type. The class of calibration stays the type of deliverable and the predictability of the milestone.
- **Creation.** The command `horai stages` creates the milestone of each stage that an active deliverable has reached and that no milestone holds. The milestone takes the stream shared by the other milestones of its deliverable, or the stream named by `--stream`, and a placeholder test of completion. The cycle planning runs it when a deliverable enters a phase.

## Constraints that decide the formats

- **One form per object.** A slot of time given to one stream is a block, whatever triggers the stream.
- **An identifier unique in the plan.** A name shared by every deliverable of a type cannot name a milestone.
- **A class of calibration holds enough ratios.** With a few deliverables of a type each year, a class per stage would hold too few ratios to be estimated.

## Options weighed

- **A request window that names its stream.** Rejected: two kinds of entry would state a start, a length and a stream.
- **Stream-less windows with one stream triggered by arrival.** Rejected: it forbids the usual pairing of requests and incidents.
- **A free name for the milestone of a stage.** Rejected: the name would be a choice with no function, and collisions would be solved by hand.
- **Calibration per stage.** Rejected for the constraint on the size of a class.
- **A procedure step with a check, without a command.** Rejected by the author in favour of a command, at the cost of writing files before the rest of the write side. The command only creates new files, and never edits one.

## Consequences

- The schemas of the typical week, of the dates and of the profile change in place; the milestone gains the field `stage`.
- The calendar, its checks, the selection and the week view no longer know a kind `request-window`.
- The fixture plan and the plan of the author move their windows into blocks of the stream `requests`, and their stages to identifiers.
