---
tags:
  - definition
index: "[Objects](docs/kernel/objects/_index.md)"
aliases:
  - Deadline
  - Imposed deadline
  - Buffer
  - Slack
---
# Deadline

> [!QUESTION] Goal: what is a date that the agent cannot move alone, and which margin protects it?

A **deadline** is a date that the agent cannot move alone, because missing it imposes a cost on a party, closes an external opportunity, or exhausts a resource. It is the imposed counterpart of an [appetite](appetite.md): in both, time is fixed and scope varies, and they differ by who can move the time. ^deadline

## Kinds

| Kind | After the date | Moved by |
| --- | --- | --- |
| `hard` | the result loses its value, or incurs a penalty | nobody, or a party by exception; the date of exhaustion of a resource is re-estimated |
| `soft` | the value of the result decays with the delay | negotiation with the party |

A deadline attaches to the level that it concerns: a purpose, a deliverable or a milestone. Its **work** $w$ is the sum of the remaining budgets of the items below it.

## Self-set and promised dates

- **A date that the agent sets for itself is not a deadline.** It is a scheduled date, or an appetite. ^no-self-deadline
- **A date that the agent proposes to a party becomes a deadline once the party relies on it.** It is therefore proposed only after the [feasibility test](../processes/imposed-deadlines.md#^feasibility-test), so that a promise does not escape the test that an imposed date passes. ^promised-date

## Demand, buffer and slack

Let $r_{50}$ and $r_q$ be the median and the quantile `calibration_quantile` of the logged ratio of time consumed to budget, and $C(D)$ the capacity that the streams concerned receive until the date $D$, at the low quantile of the [availability](availability.md). For a deadline $j$: ^slack

- the **planned demand** is $W_j = r_{50}\, w_j$;
- the **buffer** is $B_j = (r_q - r_{50})\, w_j$, the margin pooled for the whole item, after the [critical chain](../../references/critical-path-and-constraints.md). An item that states three durations contributes its pessimistic duration less its PERT value, in place of its share of that product; ^buffer
- with the deadlines sorted by date, $D_1 \le \dots \le D_n$, the **slack** at the $k$-th deadline is

$$s_k = C(D_k) - \sum_{j \le k} \left( W_j + B_j \right).$$

The slack is cumulative: a deadline is charged with the demand of every earlier deadline that draws on the same capacity, which is the test of feasibility of earliest-deadline-first scheduling for one agent.

## Consumption of the buffer

For a deadline $j$, the **work done** $p_j$ is the fraction of $w_j$, as set at the last test, carried by completed items. The **overrun** $o_j$ is the time consumed on completed items in excess of $r_{50}$ times their budgets, plus the time consumed on open items in excess of $r_{50}$ times theirs. The buffer consumed is $\beta_j = \max(0, o_j) / B_j$. ^buffer-consumption

The buffer is **running ahead** when $\beta_j > p_j$: the margin is spent faster than the work advances. This raises the first key of the [selection rule](../processes/task-selection.md#^selection-rule).

## Retroplanning

The **retroplanning** of a deadline places its items backward from its date. The latest end of an item is the date $D$ of the deadline, or the latest start of the earliest item that must follow it; the items that follow one another are those of the milestone graph, and otherwise those of lower rank. Its **latest start** is the latest date from which the capacity of its stream covers its demand and its share of the buffer before its latest end. ^retroplanning

- **The latest starts are shown by default.** For each deadline, the roadmap shows the latest start of each milestone under it, and flags an open item whose latest start has passed.
- **The full retroplanning is shown on demand.** It adds the latest end of each milestone, and the latest start and end of each task that states a budget, within its milestone and in its local order.
- The method follows the retroplanning of the [time-management course](../../references/time-management-course.md), with the buffer as its margin of safety.

## Order of the adjustments

When a slack is negative, the variables are adjusted in a fixed order: ^adjustment-order

1. the scope of the result, except for a [non-negotiable](../foundations/commitments.md#^c-non-negotiable) item, whose scope is reduced only by an explicit decision of the agent;
2. the capacity, taken from the other streams of the regimes `planned` and `pulled`, as the exception of the second [commitment](../foundations/commitments.md#^c-capacity) admits;
3. the date, by negotiation with the party; for a deadline set by the exhaustion of a resource, the resource itself, by reducing its consumption or replenishing it, levers that lie outside the allocation of attention and are recorded as such;
4. the floors, suspended for a stated period, as a recorded exception.

The process that applies this order is the [test of imposed deadlines](../processes/imposed-deadlines.md).
