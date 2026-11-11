---
tags:
  - procedure
index: "[Procedures](docs/procedures/_index.md)"
aliases:
  - Bootstrap
  - Installing the method
---
# Bootstrap

> [!QUESTION] Goal: how is the method installed on an existing inventory of tasks, without the installation becoming enablement work of its own?

The installation is enablement, and receives the appetite `bootstrap_appetite`. It installs the [minimal core](../kernel/foundations/core-and-options.md#^core) only.

1. **Membership.** Check the situation against the [conditions of the class](../kernel/foundations/problem-class.md#^conditions). If discretion is below `discretion_min`, install the degraded mode.
2. **Profile.** Take the [profile](../profiles/_index.md) of the domain, or write one by filling the [profile record](../specification/profile-record.md). Turn on only the options whose modulator is clearly present.
3. **Availability.** State the weekly capacity, its low quantile, the minimum block and the energy profile. Place the committed blocks, if any.
4. **Deliverables.** List the deliverables, admit at most `active_deliverables_max`, and tag each with its [phase](../kernel/objects/phase.md). Record each date that a party relies on as a [deadline](../kernel/objects/deadline.md) on the level that it concerns.
5. **Milestones.** For each active deliverable in validation or in delivery, state its milestones with their definitions of done. For each one in exploration, state the open questions.
6. **Attachment.** Attach each existing task to a milestone, a question or a standing parent. Send the others to the holding file without reviewing them one by one, move ideas to the ideas file, and mark the tasks that await a party as [waiting](../kernel/objects/external-party.md#^waiting), each with a follow-up.
7. **Calendar.** Fill the [calendar record](../specification/calendar-record.md): the floors first, then the windows, then the themes of the other streams.
8. **First cycle.** Run a [cycle planning](cycle-planning.md), with the end of the cycle set on the next date of the principal, or on the cadence of the agent.

> [!WARNING] Trial
> The first cycle is a trial of the core. An option is turned on afterwards only when a decision of the cycle lacked it.
