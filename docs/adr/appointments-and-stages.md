---
tags:
  - decision
status: accepted
created: 2026-11-13
index: "[Architecture decisions](docs/adr/_index.md)"
aliases:
  - Appointments and stages
  - Preparation of appointments
---
# Appointments and stages

> [!QUESTION] Goal: how are the preparation of appointments, the appointments without a fixed slot, the changes of one block, and the stages of a deliverable recorded, so that each follows the way the author actually works?

The first typical week of the author exposed four defects. A weekly share of preparation overstated the weeks in which the author presents nowhere, and understated the others. A weekly meeting whose slot varies could not be stated in the typical week, so the plannable time of a typical week was overstated. A week could replace the blocks of a date, but could not add or remove one block. The stages of a type of deliverable were created as milestones at the creation of the deliverable, although an exploration is planned by questions and not by milestones.

> [!WARNING] Partly replaced
> The decision on [streams, allocation and loose tasks](streams-allocation-and-loose-tasks.md) replaces the weekly share of preparation and the field `default_budget`. The decision on [request windows and stages](request-windows-and-stages.md) replaces the title of a stage by its identifier, and the decision on [uniform selection and recurrence](uniform-selection-and-recurrence.md) replaces the number `per_week` of an unplaced appointment.

## Decision

- **Preparation per appointment.** The preparation of an appointment exists only as a task that names the appointment in `prepares` and bears a budget. The budget is removed from the plannable time of the week of the appointment. A stream triggered by appointment states `preparation: {default_budget}`, the budget of a preparation task that states none. The weekly share of preparation is retired.
- **Unplaced appointments.** The typical week lists the appointments without a fixed slot under `unplaced`, each with an identifier, a title, a length, a number per week, a stream and a party. Their time is removed from the plannable time of a typical week. A week places each of them on a date by an appointment whose field `places` names it, and the check warns when a started week has not placed one.
- **One block added or removed.** A date of a week may list `added_blocks`, and `removed_blocks` by the start of the typical block. The field `blocks` still replaces every block of the date.
- **Stages with their phase.** Each stage of a type of deliverable states its title and the phase from which it exists. A stage is created as a milestone when its deliverable enters that phase.
- **Argument plan.** The first stage of delivery, and of validation for an article, is the `argument-plan`: the messages and the arguments are established and agreed before any writing, which projects them. The templates are:
  - `article`: `argument-plan` in validation; `draft`, `internal-review`, `submission`, `revision` in delivery;
  - `abstract`: `argument-plan`, `draft`, `submission` in delivery;
  - `poster`: `argument-plan`, `layout`, `print` in delivery;
  - `talk`: `argument-plan`, `slides`, `rehearsal` in delivery.

## Constraints that decide the formats

- **A share fits continuous demand only.** A fraction of each week is a meaningful policy for work whose demand spreads over the weeks: selection, demand, the calendar and arrival. The preparation of an appointment is tied to one event and exists only when that event requires it, so it receives a budget per event.
- **The typical week states every time that it removes.** Time that a party fixes every week, even without a slot, is not plannable.
- **A milestone exists only where its phase admits one,** as the [phase](../kernel/objects/phase.md#^phases) states.

## Options weighed

- **A weekly share with budgets per appointment.** Rejected: two mechanisms for one kind of work.
- **A default slot for the supervision, moved every week.** Rejected: the typical week would record a slot that is often wrong.
- **Blocks of a date merged by their start.** Rejected: a reader cannot tell an addition from a replacement.
- **Stages created on entering delivery, whatever their phase.** Rejected by the author in favour of a phase per stage, so that the argument plan of an article can belong to validation.

## Consequences

- The schemas of the profile, the typical week and the week change in place, and the field `cap` of an appointment is replaced by the budget of the preparation task.
- The plannable time of a week subtracts the appointments, the unplaced appointments and the budgets of the preparation tasks of the week.
- The calendar of a date applies the added and the removed blocks after a replacement.
- The specification, the research profile and the plan of the author in Geonexus follow.
