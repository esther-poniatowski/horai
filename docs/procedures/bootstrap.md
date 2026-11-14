---
tags:
  - procedure
index: "[Procedures](docs/procedures/_index.md)"
aliases:
  - Bootstrap
  - Installing the method
---
# Bootstrap

> [!QUESTION] Goal: how is the method installed on an existing inventory of tasks, without the installation becoming tooling work of its own?

The installation is work that yields means, and receives the appetite `bootstrap_appetite`. It installs the [minimal core](../kernel/foundations/core-and-options.md#^core), and the options turned on at step 2.

1. **Membership.** Check the situation against the [conditions of the class](../kernel/foundations/problem-class.md#^conditions). If discretion is below `discretion_min`, install the degraded mode.
2. **Profile.** Take the [profile](../profiles/_index.md) of the domain, or write one by filling the [profile record](../specification/profile-record.md), and state in it the hours of high energy of the agent. Turn on only the options whose modulator is clearly present.
3. **Typical week.** Fill the [typical week](../specification/typical-week-record.md): the spans available on each weekday, the recurring appointments fixed by others, the appointments held every week without a fixed slot, the predictability of a week, and the working time of a poor week.
4. **Deliverables.** List the deliverables, admit at most `active_deliverables_max`, and tag each with its [phase](../kernel/objects/phase.md). Record each date that a party relies on as a [deadline](../kernel/objects/deadline.md) on the level that it concerns. Declare in the file of the parties each [party](../kernel/objects/external-party.md#^party) that a record names, unless it is occasional.
5. **Milestones.** For each active deliverable in validation or in delivery, state its milestones with their definitions of done. For each one in exploration, state the open questions.
6. **Attachment.** Attach each existing task to a milestone or a question, or give it its stream as a [loose task](../kernel/objects/work-hierarchy.md#^standing-parent), in the task list of the folder whose files it touches. Send the others to the holding file without reviewing them one by one, move ideas to the ideas file, and give each task that awaits a party the date of its [follow-up](../kernel/objects/external-party.md#^waiting), in the field `follow_up`.
7. **Calendar.** Place in the typical week the blocks of the streams triggered by the calendar first, then the request windows, then the blocks of the other streams. Record each departure already known, such as an appointment of one date or an absence, in the [calendar of dates](../specification/calendar-record.md).
8. **First cycle.** Run a [cycle planning](cycle-planning.md), with the end of the cycle set on the next date of the party to whom the agent is accountable, or on the cadence of the agent.

> [!WARNING] Trial
> The first cycle is a trial of the installation. Any other option is turned on afterwards only when a decision of the cycle lacked it.
