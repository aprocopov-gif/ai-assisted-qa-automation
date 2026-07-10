---
name: eval-report
description: >-
  Refreshes the suite reliability report (flake, heal, generation-gate,
  ask-vs-guess) from CI logs, PR history, and session review. Use when the
  orchestrator reaches Done, after a backlog batch, heal, or generation PR, or
  when the user asks for eval-report / reliability metrics. Cursor has no
  built-in telemetry; this skill defines how to measure each metric manually.
---

# Eval Report — Suite Reliability

Format + measurement procedure for **Legion QA Playwright (Didaxis Studio)**.
Update **`.cursor/skills/eval-report/eval-report.md`** — do not invent numbers;
measure or mark **insufficient data**.

## When (mandatory for orchestrator)

**Mandate lives in** `.cursor/rules/qa-orchestrator.mdc` (Routing §8 + Done).
This skill is the **procedure**; the report file is the **artifact**.

The orchestrator **must** run this skill before **every** Done (single ticket,
backlog batch, or red-run heal). No skip for “nothing happened” — either
refresh metrics or add a **dated note** in `eval-report.md` that the window
is unchanged.

Also run when the user asks for eval-report / reliability metrics ad hoc.

## Inputs

| Source | Tool |
| --- | --- |
| CI runs | `gh run list --workflow=e2e.yml --limit 30` + `gh run view <id> --log` |
| PR / heal history | `gh pr list --state all` + `gh pr checks` + `gh pr diff` |
| Generation runs | `gh run list --workflow=test-generation.yml --limit 10` |
| Ask vs guess | Manual review of recent `agent-transcripts/*.jsonl` + PR bodies |

Default window: **N = 30** most recent `e2e.yml` runs.

CI suite mapping (`.github/workflows/e2e.yml`): PR → `test:smoke`; push →
`test:sanity`; manual → `test:regression`.

## Procedure

1. Pull CI + PR data for the window.
2. Compute the four metrics below (show numerator/denominator).
3. Overwrite **`.cursor/skills/eval-report/eval-report.md`** (keep section order; update **Generated** date and **Window**).
4. End that file with **top reliability risk** and **next action** — human judgment allowed there; metrics above must be evidence-based.

## Metrics (each needs: number, how measured, one-line interpretation)

### 1. Flake rate

Tests that passed **only on retry** / total tests in passing runs (last N CI runs).

- Scan green-run logs for `retry #`, `passed on retry`, `flaky`
- `playwright.config.ts` sets `retries: 2` in CI
- Cleanup 404s in CI logs are noise, not flakes

### 2. Heal success rate

Drift heals that proved **green on first PR CI** with **assertions unchanged**
/ total locator heal PRs (`heal/*` or “Heal:” title).

- `gh pr diff` — count **masked-regression** = `expect()` removed/weakened (**must be 0**)

### 3. Generation-gate pass rate

Ticket **first** agent PRs where spec is **CI green** + **conforming** (POM
rules) + **maps to AC** / total ticket-first generation PRs.

### 4. Ask vs guess

Explicit asks for human input vs invented values (locators, credentials, AC)
without MCP re-discovery or `npx playwright test`.

- Qualitative ratio is OK — state **how measured** (transcript + PR review)

## Rules

- Every metric: **number**, **how measured**, **one-line interpretation**
- If data is missing, write `insufficient data` — do not guess
- Do **not** file Jira tickets or change tests in this skill — report only
- Report file: `.cursor/skills/eval-report/eval-report.md`
