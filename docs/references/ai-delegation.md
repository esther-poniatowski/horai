---
tags:
  - reference
index: "[References](docs/references/_index.md)"
aliases:
  - AI delegation
  - Perceived and measured speedup
---
# AI delegation

## Findings

- **Trial of early 2025.** METR ran a randomized trial with experienced open-source developers working on their own repositories. With AI tools the developers were 19% slower, while believing that they were 20% faster [metr2025].
- **Update of February 2026.** A later measurement gives estimates of −18% and −4%, each with an interval that spans zero. METR judges that the true speedup is now larger than in 2025 [metr2026].

The stable result across both reports is the gap between the perceived and the measured effect.

## Bearing on `horai`

- The time spent verifying the output of agents is [logged apart](../kernel/processes/feedback.md#^verification-time), so that the effect of delegation is measured and not perceived.
- Delegation lowers the cost of building a tool, and leaves the costs of verification and of maintenance, which the [recurrence test](../procedures/enablement-request.md) weighs.
- The trials concern software development. Their transfer to mathematical derivation and to the triage of literature is an assumption.

## Sources

- [metr2025] ✓ [METR, "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity", 2025](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
- [metr2026] ✓ [METR, uplift update, February 2026](https://metr.org/blog/2026-02-24-uplift-update/)
