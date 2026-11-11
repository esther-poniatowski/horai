---
tags:
  - reference
index: "[References](docs/references/_index.md)"
aliases:
  - Critical path and theory of constraints
  - Critical path method
  - Theory of constraints
  - Critical chain
---
# Critical path and theory of constraints

## Critical path method

The critical path method represents a project as a network of activities with durations and precedence relations. The **critical path** is the longest path through the network: it fixes the minimal duration of the project, and a delay on it delays the whole. The method presupposes that the activities and their relations are known before the work.

## One resource

The critical path gives the duration of a project whose activities run in parallel, with unlimited resources. When all activities use one resource, the duration is the sum of their durations, and the problem becomes one of sequencing. For deadlines on one resource, scheduling by earliest deadline first meets every deadline whenever any order does, and the condition is that the cumulative work due by each deadline fit in the time available until it [liu1973].

## Theory of constraints

The theory of constraints of Goldratt holds that the output of a system is limited by one constraint at a time [goldratt1984]. It prescribes five steps: identify the constraint, exploit it, subordinate everything else to it, elevate it, and repeat. *Critical chain* applies the theory to projects: the tasks are estimated without their safety margins, near the median, the margins are pooled into one buffer at the end of the project, and the consumption of the buffer is the signal of its health [goldratt1997].

## Bearing on `horai`

- The [milestone graph](../kernel/objects/dependency.md#^graph-uses) serves precedence, unblocking and external latencies, and not the longest path, since one agent is one resource.
- The [cumulative test](../kernel/processes/imposed-deadlines.md#^feasibility-test) applies the condition of earliest deadline first.
- The [constraint rule](../kernel/processes/enablement.md#^constraint-rule) applies the steps of exploitation and subordination to a blocking tool.
- The [buffer](../kernel/objects/deadline.md#^buffer) of an imposed deadline applies the critical chain: one margin per deliverable, whose consumption is the signal of its health.

## Sources

- [goldratt1984] ○ Goldratt and Cox, *The Goal: A Process of Ongoing Improvement*, North River Press, 1984
- [goldratt1997] ○ Goldratt, *Critical Chain*, North River Press, 1997
- [liu1973] ○ Liu and Layland, "Scheduling algorithms for multiprogramming in a hard-real-time environment", *Journal of the ACM*, 20(1), 1973, pp. 46–61
