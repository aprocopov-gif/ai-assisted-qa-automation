# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `ai-assisted-qa-automation`  
**Window:** `e2e.yml` runs 2026-10-30 → 2026-11-08 (15 daily backlog-scan runs, all failed at Playwright install) + related draft PRs  
**Generated:** 2026-11-08  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**This refresh trigger:** scheduled backlog batch (cron `0 10 * * *`, 2026-11-08 UTC). **0 / 5** tickets processed — **Atlassian MCP `needsAuth`**; unauthenticated Jira JQL returned `issues: []` (untrusted). Metrics below **unchanged** from prior evidence window; CI slice is now scan-only failures (`Playwright does not support chromium on ubuntu26.04-x64`), not suite execution.

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
| **Number** | **This session (2026-11-08 backlog scan): 0 asks; 0 invented tickets or AC.** Did not process Jira queue without authenticated MCP — no silent ticket picks. |
| **How measured** | Session review. `GetDynamicTools` → Atlassian `needsAuth`; `mcp_auth` rejected in Cloud Agent; unauthenticated Jira REST treated as false-empty per automation memory; `gh` for CI/PR window only. |
| **What it tells us** | Correct behavior under missing Jira auth is **stop**, not guess from cached snapshots or public API empty arrays. |

---

## Top reliability risk

**Backlog automation cannot enumerate Jira.** Atlassian MCP auth is unavailable in Cloud Agent; without credentials the queue is unknowable and **no ticket generation runs**. Secondary: **E2E workflow fails before tests** on `ubuntu26.04-x64` Playwright/chromium install, so even doc-scan PRs do not exercise the suite in CI.

## Next action

1. Reconnect **Atlassian** MCP for automation `1e8b0ec6-3214-47ed-ad52-fe5e53731673` (Cursor Integrations) or bind `ATLASSIAN_*` / Jira API token to this Cloud Agent environment.
2. Fix **e2e.yml** runner image or Playwright browser install so PR CI can run smoke again.
3. Queue work: move a DS ticket to **In Progress** without **`tests-generated`** once Jira is readable.
4. On the **next real generation or heal PR**, refresh generation-gate and heal metrics from first-PR-green evidence.
