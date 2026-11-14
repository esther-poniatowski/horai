---
tags:
  - procedure
index: "[Procedures](docs/procedures/_index.md)"
aliases:
  - Weekly review
---
# Weekly review

> [!QUESTION] Goal: how is a week closed and the next one committed, within `ritual_durations.weekly_review`?

1. **Inbox.** Process the inbox: attach each item to a parent, record it as a loose task of its stream, send it to the holding file or to the ideas file, or discard it. A request of the class `scheduled` is processed here.
2. **Metrics.** Read the [metrics](../kernel/processes/feedback.md#^core-metrics), and the metric of each option turned on.
3. **Deviations.** Record each deviation from a policy as a deviation entry, for the strategic review. A departure from the shares that a non-negotiable mark explains is not a deviation. Change no policy here.
4. **Report.** Read the [weekly report](../kernel/processes/feedback.md#^weekly-report) of the ending week. The checkpoint decisions of step 6 enter the next report.
5. **Waits.** Schedule the follow-ups that fall within the week, and apply the fallback of each wait whose latest date has passed.
6. **Checkpoints.** List the items whose budget is consumed or will be within the week, and run a [checkpoint decision](checkpoint-decision.md) for each.
7. **Buffers.** For each deadline whose buffer is running ahead, note it: the selection rule will raise it.
8. **Commit.** List the tasks of the ending week left undone, including those entered laterally, and decide for each one whether it is committed again. Then log this review in the [review log](../specification/log-record.md), which starts the new week. Mark with its date each task committed for the week, within the allocation of each stream. Each committed task must serve a milestone or a question of the cycle, or be a [loose task](../kernel/objects/work-hierarchy.md#^standing-parent) of its stream; a recurring task needs no mark.
9. **Calendar.** Confirm the blocks, the request windows and the appointments of the week. Enter in the [calendar of dates](../specification/calendar-record.md) each departure from the typical week that is not recorded yet: an appointment of one date, a recurring appointment cancelled or moved, an absence, the blocks of a date replaced, or one block added or removed on a date. Place on a date each appointment that the typical week lists as unplaced, as often as its number per week, by an appointment whose field `places` names it. For each appointment of the week that calls for a preparation, record a loose task of its stream that names it in `prepares`, with a budget, and mark it with the date of this review; a preparation task without a budget takes the reserve per event of its stream. Add before the appointment, in `added_blocks`, a block of that stream as long as the budget, since only a block offers the task to the selection. Keep the blocks of the streams triggered by the calendar at their positions.

> [!NOTE]
> Step 7 is skipped when the option of imposed deadlines is off. Without the option of external parties, step 5 schedules the follow-ups only, since the core records no latest date.
