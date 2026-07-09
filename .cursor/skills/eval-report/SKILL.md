---
name: eval-report
description: >-
  Refreshes the suite reliability report (flake, heal, generation-gate,
  ask-vs-guess). Use when the orchestrator reaches Done, after a backlog batch,
  heal, or generation PR, or when the user asks for eval-report / reliability
  metrics.
---

# Reliability eval

Update [eval-report.md](eval-report.md) — the living report lives next to this skill.

Cursor has no built-in telemetry. Measure from CI logs, PR history, and session review. End with top risk + next action. Masked-regression count must stay **0**.
