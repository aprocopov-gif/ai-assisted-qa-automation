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
Update the **Current report** section below in this file; do not invent numbers —
measure or mark **insufficient data**.

## When (mandatory for orchestrator)

The QA orchestrator **must** run this skill before claiming **Done** when any
of the following occurred in the session:

- A heal PR was opened or a red CI run was triaged
- A generation PR was opened for a ticket
- The **Current report** section is missing or older than **14 days**

Otherwise: skip with a one-line note in the session summary (`eval: skipped —
no trigger`).

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
3. Overwrite the **Current report** section below (keep section order; update
   **Generated** date and **Window**).
4. End with **top reliability risk** and **next action** — human judgment
   allowed here; metrics above must be evidence-based.

## Metrics

### 1. Flake rate

Tests that passed **only on retry** / total tests in passing runs.

- Scan green-run logs for `retry #`, `passed on retry`, `flaky`
- `playwright.config.ts` sets `retries: 2` in CI
- **What it tells us:** one line — retries hiding timing bugs vs hard failures

### 2. Heal success rate

Drift heals that proved **green on first PR CI** with **assertions unchanged**
/ total locator heal PRs (`heal/*` or “Heal:” title).

- `gh pr diff` — count **masked-regression** = `expect()` removed/weakened (**must be 0**)
- **What it tells us:** one line on one-shot heal vs cascade

### 3. Generation-gate pass rate

Ticket **first** agent PRs where spec is **CI green** + **conforming** (POM
rules) + **maps to AC** / total ticket-first generation PRs.

- Counterexamples (e.g. “static review only”, red first CI) go in the table
- **What it tells us:** one line on first-time generation vs follow-up drift

### 4. Ask vs guess

Explicit asks for human input vs invented values (locators, credentials, AC)
without MCP re-discovery or `npx playwright test`.

- Qualitative ratio is OK — state **how measured** (transcript + PR review)
- **What it tells us:** one line on agent discipline

## Rules

- Every metric: **number**, **how measured**, **one-line interpretation**
- If data is missing, write `insufficient data` — do not guess
- Cleanup 404s in CI logs are noise, not flakes
- Do **not** file Jira tickets or change tests in this skill — report only

---

## Current report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `legion-qa-ai-assisted-program-ann`  
**Window:** last **30** `e2e.yml` runs + related PRs (through 2026-07-09)  
**Generated:** 2026-07-09  
**Note:** Cursor has **no built-in telemetry** for flake, heal, generation-gate, or ask-vs-guess. Every number below was measured from CI logs (`gh`), PR history, and session review.

### Flake rate

| | |
|---|---|
| **Number** | **3** flaky test outcomes in **27** passing E2E runs → **3/27 runs (11%)** showed any flaky result; **~0.7%** of test executions in runs that reported counts (`1 flaky` / `143 passed + 1 flaky` each). Post–Block-15 runs ([28992695571](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/28992695571) sanity, [28992482239](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/28992482239) smoke) reported **0** flaky. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 30`, then `gh run view <id> --log` grepped for `flaky`, `Retry #`, `passed on retry`. CI uses `retries: 2` (`playwright.config.ts`). Flaky tests: `ds4-delete-program` **TC-004** ([28762948379](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/28762948379)), `ds2-edit-program` **TC-002** ([27931236042](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/27931236042)), `ds4-delete-program` **TC-017** ([27931166465](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/27931166465)). Auth-setup `Retry #` lines on failed runs were **hard fails**, not flakes. Cleanup 404s treated as noise. |
| **What it tells us** | Retries keep CI green, but DS-2 TC-002 and DS-4 TC-004/TC-017 are recurring timing/race candidates. Block-15 smoke/sanity slices are currently clean. |

### Heal success rate

| | |
|---|---|
| **Number** | **Clean heals: 1 / 2 (50%)** in the recent locator-repair window. **Masked-regression count: 0** (required target: **0**). |
| **How measured** | PR history (`gh pr list`, `gh pr checks`, `gh pr diff`): [#10](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/10) (POM locator guess — first CI **failed**) vs [#11](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/11) (restored role/label locators + self-heal skill — first CI **passed**). [#12](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/12) (DS-3 unique-name stabilization) is a **test-data fix**, not counted as a heal. No formal `heal/*` repair PRs under the post-skill orchestrator path yet. No `expect()` removals/weakenings in heal PR diffs. |
| **What it tells us** | Locator heals without triage + Playwright MCP rediscovery can ship wrong selectors (PR #10). Masked-regression discipline holds at 0; self-heal gate is doing its job. |

### Generation-gate pass rate

| | |
|---|---|
| **Number** | **First-PR CI green: 2 / 2 (100%)** for ticket-shaped generation PRs ([#7](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/7) DS-4, [#8](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/8) DS-1). **Full gate (green + conforming + maps-to-AC): incomplete / unknown** — not re-audited against Jira AC this refresh. Scheduled `test-generation.yml` runs (10 recent, all green) do not by themselves prove a spec gate. |
| **How measured** | `gh pr list` filtered for `test(DS-*)` titles; `gh pr checks` on #7/#8. Generation workflow: `gh run list --workflow=test-generation.yml --limit 10`. PRs reference `features/DS-*.feature.md` + `tests/ds*.spec.ts`; neither #7 nor #8 carries the `tests-generated` GitHub label (Jira label may differ). |
| **What it tells us** | Early agent-generated specs can land green on first PR, but without a recorded conforming+AC checklist the gate is only half-instrumented. |

### Ask-vs-guess

| | |
|---|---|
| **Number** | **This refresh session: ~0 asks vs 0 invented product values** (explored repo + `gh` before writing). **Prior Block-15 framework session (sample): ~2 asks vs ~5 invented defaults** (ask:guess ≈ 0.4). Broader suite history: **not measurable** from git alone. |
| **How measured** | Manual session review of agent transcripts + PR bodies. Examples of prior **guessing**: `@high→@smoke` tag mapping, `DIDAXIS_NONADMIN_*` env aliases, branch naming — without explicit human confirmation. |
| **What it tells us** | Repo exploration + `gh` evidence beats silent defaults for CI workflow names and report paths. Still prefer one explicit ask when tag semantics or credentials are under-specified. |

### CI snapshot (window context)

| Metric | Value |
|---|---|
| E2E runs scanned | 30 (`e2e.yml`) |
| Passing | 27 |
| Failing | 3 (bloc14-1 locator drift on `main` merge + two pre-fix pushes) |
| Suite mapping | PR → `test:smoke` (~19 tests); push → `test:sanity` (~144 tests); manual → `test:regression` |
| Block-15 change | DS specs now carry exactly one tag each (`@smoke` / `@sanity` / `@regression`) |

### Top reliability risk

**Retries masking DS-4 and DS-2 flakes** — three distinct tests passed only on retry in the last 30 runs; Block-15 tag coverage now puts DS specs into smoke/sanity slices, so flakes may surface more often in PR/push CI instead of staying hidden in full local runs.

### Next action

1. **Stabilize DS-4 TC-004 and TC-017** and **DS-2 TC-002** (fix races with web-first waits; do not raise timeouts as the fix).  
2. On the next generation PR, add an explicit **generation-gate checklist** (green + `playwright-conventions.mdc` + AC map) in the PR body and apply label **`tests-generated`**.  
3. When opening a heal repair PR, use branch `heal/<spec-slug>` and prove green with **assertions unchanged** so heal success rate becomes measurable under the orchestrator path.
