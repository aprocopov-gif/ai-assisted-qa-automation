# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `ai-assisted-qa-automation`  
**Window:** `e2e.yml` runs 2026-07-10 → 2026-07-22 (14 daily backlog-scan runs) + related PRs, plus local DS-4 re-verify  
**Generated:** 2026-07-22  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**This refresh trigger:** scheduled **Backlog mode** cron run **2026-11-14 10:04 UTC** (`0 10 * * *`). **Processed 0 / 5 tickets** — Atlassian MCP `needsAuth` (desktop-only OAuth); unauthenticated Jira JQL returned HTTP 200 `issues: []` (known false-empty). `workflow_dispatch` for `test-generation.yml` returned **403**. No generation/heal/local-run evidence this session; metric numerators unchanged from 2026-07-22 window.

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
| **How measured** | `gh pr list` — no new `test(DS-*)` generation PRs this window (all recent PRs #16–#24 are `docs(eval-report)` empty-scan commits). DS-4 re-verified **CI-adjacent green locally** this session (20/20) and its 19 TCs **map to AC** (both AC scenarios — confirm-delete + cancel — plus negatives/edges); conformance to `playwright-conventions.mdc` holds (role/label locators, one tag/test, self-cleaning via cleanup fixture). |
| **What it tells us** | No fresh generation evidence; DS-4's existing spec still passes and maps to AC, but the full conforming+AC checklist remains only half-instrumented across the suite. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **This session (2026-11-14 backlog scan): 0 asks, 0 invented tickets/AC/locators.** |
| **How measured** | Session review. Did not treat unauthenticated Jira empty list as proof of empty queue; recorded auth block and cited automation memory snapshot instead. No Playwright run (DIDAXIS_* absent in env). |
| **What it tells us** | Automation correctly refuses to generate specs without verified ticket ACs; operational unblock is Jira auth + env secrets, not guessing backlog contents. |

---

## Top reliability risk

**Jira auth gap blocks the backlog automation.** Daily cron runs cannot enumerate `In Progress` tickets without Atlassian MCP auth or `ATLASSIAN_*` secrets in the Cloud Agent environment. Unauthenticated JQL false-empties mask real queue work; `test-generation.yml` dispatch is also blocked (integration token 403).

## Next action

1. **Reconnect Atlassian MCP** for automation `1e8b0ec6-3214-47ed-ad52-fe5e53731673` in Cursor **Integrations**, or add `ATLASSIAN_API_TOKEN` + `ATLASSIAN_EMAIL` + `ATLASSIAN_BASE_URL` to the Cloud Agent / `dev1` secrets.
2. Grant the GitHub app **`workflow_dispatch`** on `test-generation.yml` as a fallback when Cloud Agent Jira auth is unavailable.
3. To queue work manually: move a DS ticket to **In Progress** and remove **`tests-generated`** until auth is fixed.
