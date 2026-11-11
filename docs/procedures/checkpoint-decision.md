---
tags:
  - procedure
index: "[Procedures](docs/procedures/_index.md)"
aliases:
  - Checkpoint decision
---
# Checkpoint decision

> [!QUESTION] Goal: what is decided when the appetite of a piece of work is consumed?

The decision applies the rules of [uncertainty control](../kernel/processes/uncertainty-control.md).

1. **State.** Write in two sentences what was obtained and what remains unknown.
2. **Count.** Read the number of earlier overruns of the same item.
3. **Value.** Where the valuation is quantified, compute $G(\Delta)$ for the renewals considered, as the [stop by value](../kernel/processes/uncertainty-control.md#^stop-by-value) states.
4. **Decide.** Record exactly one outcome:
   - **Stop.** The item is closed as not obtained, and what was ruled out enters the evidence note. This is the default at the overrun `stop_overruns`, and whenever no renewal has $G(\Delta) > 0$.
   - **Reduce.** The definition of done is narrowed to what the evidence now supports, with a budget for the reduced scope.
   - **Renew.** A new budget is given, with a written statement of what has changed since the first budget.
5. **Deadline.** If the item lies under a hard deadline and the outcome is a stop or a reduction, open the [deadline feasibility](deadline-feasibility.md) at its adjustment of scope, instead of closing the item silently. A renewal under a deadline is admissible only if the feasibility test still passes.
6. **Propagate.** For a stop or a reduction, review the milestones that depended on the item, the [phase](../kernel/objects/phase.md) of the deliverable, and the parties that await the result.
7. **Log.** Record the outcome entry, whose ratio is censored for a stop or a reduction, for the [calibration](../kernel/processes/uncertainty-control.md#^calibration).

> [!WARNING]
> Renewal is the easy outcome. Its justification must name a fact that was unknown when the first budget was set.
