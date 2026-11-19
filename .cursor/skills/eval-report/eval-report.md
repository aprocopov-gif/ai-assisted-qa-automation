# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `ai-assisted-qa-automation`  
**Window:** `e2e.yml` runs 2026-07-10 → 2026-07-22 (14 daily backlog-scan runs) + related PRs, plus local DS-4 re-verify  
**Generated:** 2026-11-19  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**This refresh trigger:** Backlog mode cron (2026-11-19, automation `1e8b0ec6-3214-47ed-ad52-fe5e53731673`).

**2026-11-19 backlog scan (cron automation `1e8b0ec6-3214-47ed-ad52-fe5e53731673`, budget 5):** **0 tickets processed.** Atlassian MCP `needsAuth` (`mcp_auth_error` on run `bc-795a96fc-ac3d-4f40-9ae5-88bd9fd6d796`; interactive auth unavailable in Cloud Agent). No `ATLASSIAN_*` / `DIDAXIS_*` in Cloud Agent env. `gh workflow run test-generation.yml` → 403. Did not treat missing Jira as an empty queue. No `tests-generated` labels added. Core metrics below unchanged.

**2026-11-18 backlog scan (cron automation `1e8b0ec6-3214-47ed-ad52-fe5e53731673`, budget 5):** **0 tickets processed.** Atlassian MCP `needsAuth` (interactive auth unavailable in Cloud Agent). Unauthenticated Jira REST (`legionqaschool.atlassian.net`) → HTTP 401; no `ATLASSIAN_*` / `DIDAXIS_*` in Cloud Agent env. `gh workflow run test-generation.yml` → 403. Did not treat empty Jira responses as an empty queue. No `tests-generated` labels added. Core metrics below unchanged; recent `e2e.yml` on eval-doc pushes still fails at `playwright install` (`ubuntu26.04-x64` unsupported).

---

## Flake rate

| | |
|---|---|
| **Number** | **0** flaky outcomes across **14** `e2e.yml` runs (2026-07-10 → 2026-07-22). Local DS-4 re-verify: **20 passed, 0 flaky, 0 retries**. → **0%** flake in the current window. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 30`, then `gh run view <id> --log` grepped for `flaky`, `Retry #`, `passed`. Sampled runs 2026-07-16→07-22 (smoke slice **40 tests → 39 passed** + 1 skip; sanity slice **54 tests → 49 passed** + 5 skips) — none reported `flaky`. Local: `npx playwright test tests/ds4-delete-program.spec.ts` → 20 passed, no `Retry #`. CI uses `retries: 2` (`playwright.config.ts`); skips are the non-admin TC-007/TC-010 gates, not failures. |
| **What it tells us** | The prior window's flake candidates (**DS-4 TC-004/TC-017**, **DS-2 TC-002**) did **not** recur — DS-4 TC-004 and TC-017 passed first-try both in CI and locally. Note: recent CI runs are daily **empty-backlog** scans exercising the standing suite, not new-code runs. |

---

## Heal success rate

| | |
|---|---|
| **Number** | **Unchanged: 1 / 2 (50%)** — no new locator-heal PRs this window. **Masked-regression count: 0** (required target: **0**). |
| **How measured** | `gh pr list --state all` — no `heal/*` or "Heal:" PRs since the last window; latest heal-related PRs remain [#10](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/10) (first CI failed) / [#11](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/11) (first CI passed). No red run this session, so no heal was invoked. |
| **What it tells us** | Metric is stale by design (no drift to repair). Masked-regression discipline holds at 0. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **Unchanged: first-PR CI green 2 / 2 (100%)** ([#7](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/7) DS-4, [#8](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/8) DS-1). **Full gate (green + conforming + maps-to-AC): still incomplete / unknown.** |
| **How measured** | `gh pr list` — no new `test(DS-*)` generation PRs this window (recent PRs #69–#84 are `docs(eval)` empty-scan commits). DS-4 re-verified **CI-adjacent green locally** (20/20) and its 19 TCs **map to AC** (both AC scenarios — confirm-delete + cancel — plus negatives/edges); conformance to `playwright-conventions.mdc` holds (role/label locators, one tag/test, self-cleaning via cleanup fixture). |
| **What it tells us** | No fresh generation evidence; DS-4's existing spec still passes and maps to AC, but the full conforming+AC checklist remains only half-instrumented across the suite. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **This session (2026-11-19 backlog scan): 0 asks vs 0 invented product values.** |
| **How measured** | Session review. Queue JQL from orchestrator Backlog mode; did not invent ticket keys or AC. Atlassian MCP auth unavailable; Jira REST not called with guessed credentials; `gh workflow run` failed with 403 — reported as blocker, not workaround. Prior automation memory + `gh run list` for CI context only. |
| **What it tells us** | Repeated Jira-auth gaps block backlog execution; stopping at enumeration is correct — guessing an empty queue would inflate ask-vs-guess risk. |

---

## Top reliability risk

**Jira integration auth on Cloud Agent runs** — backlog automation cannot enumerate or label tickets without Atlassian MCP or `ATLASSIAN_*` secrets; daily cron runs produce doc-only PRs and **0 / 5** ticket throughput. Secondary: stale heal / full-generation-gate instrumentation (no new generation PRs since DS-1/DS-4 window).

## Next action

1. Reconnect **Atlassian** MCP for automation `1e8b0ec6-3214-47ed-ad52-fe5e53731673` (Cursor → Integrations) **or** grant Cloud Agent `ATLASSIAN_*` / `DIDAXIS_*` and `workflow_dispatch` on `test-generation.yml`.
2. Queue work by moving a DS ticket to **In Progress** without the `tests-generated` label.
3. Fix CI runner / `playwright install` on `ubuntu26.04-x64` so eval-doc PRs regain smoke signal.
4. On the **next real generation or heal PR**, capture first-PR-green + conformance + AC-map in the PR body.