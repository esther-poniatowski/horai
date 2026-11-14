---
tags:
  - reference
index: "[References](docs/references/_index.md)"
aliases:
  - Attention and switching
  - Attention residue
---
# Attention and switching

## Findings

- **Attention residue.** Leroy reports that, after a change of task, part of the attention stays on the previous task, and the performance on the next one decreases [leroy2009]. The experiments use short tasks in the laboratory.
- **Length of a session.** The prescription of sessions of 90 minutes appeals to a cycle of rest and activity during waking. The review of 2026-11-11 could not open the primary sources on that cycle, and found no good evidence for the prescription.
- **Deliberate practice.** A critical reading of the work of Ericsson on deliberate practice finds that the figures of about one hour per session and four hours per day rest on small studies [spotcheck2019].

## Bearing on `horai`

- The findings support fewer changes between kinds of work. They do not support a particular length of block.
- The decision on [day theming](../adr/day-theming.md) therefore assigns a stream to a half-day or a day, and fixes by the clock only the slots of the streams triggered by the calendar.

## Sources

- [leroy2009] ○ (bibliographic record only) [Leroy, "Why is it so hard to do my work? The challenge of attention residue when switching between work tasks", *Organizational Behavior and Human Decision Processes*, 109(2), 2009, pp. 168–181](https://econpapers.repec.org/RePEc:eee:jobhdp:v:109:y:2009:i:2:p:168-181)
- [spotcheck2019] ✓ ["Epistemic Spot Check: The Role of Deliberate Practice in the Acquisition of Expert Performance", 2019](https://acesounderglass.com/2019/06/21/epistemic-spot-check-the-role-of-deliberate-practice-in-the-acquisition-of-expert-performance/)
