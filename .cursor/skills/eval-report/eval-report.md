# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `legion-qa-ai-assisted-program-ann`  
**Window:** `e2e.yml` runs 2026-10-30 → 2026-11-10 (18 daily backlog-scan runs, all failed at Playwright install) + related draft PRs  
**Generated:** 2026-11-10  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**This refresh trigger:** scheduled backlog batch (cron `0 10 * * *`, 2026-11-10 UTC). **0 / 5** tickets processed — **Atlassian MCP `needsAuth`**; unauthenticated Jira JQL returned `issues: []` (untrusted). `workflow_dispatch` for `test-generation.yml` returned **403** (integration token). Metrics below **unchanged** from prior evidence window; CI slice remains scan-only failures (`Playwright does not support chromium on ubuntu26.04-x64`), not suite execution.

---

## Flake rate

| | |
|---|---|
| **Number** | **0** flaky outcomes across **14** `e2e.yml` runs (2026-07-10 → 2026-07-22). Local DS-4 re-verify: **20 passed, 0 flaky, 0 retries**. → **0%** flake in the last window where tests actually executed. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 30`, then `gh run view <id> --log` grepped for `flaky`, `Retry #`, `passed`. Sampled runs 2026-07-16→07-22 (smoke slice **40 tests → 39 passed** + 1 skip; sanity slice **54 tests → 49 passed** + 5 skips) — none reported `flaky`. Since 2026-10-30, all sampled runs fail at browser install (no test output). CI uses `retries: 2` (`playwright.config.ts`). |
| **What it tells us** | Flake signal is **stale** — recent CI never reaches Playwright execution, so flake rate cannot be refreshed from automation scans. |

---

## Heal success rate

| | |
|---|---|
| **Number** | **Unchanged: 1 / 2 (50%)** — no new locator-heal PRs this window. **Masked-regression count: 0** (required target: **0**). |
| **How measured** | `gh pr list --state all` — no `heal/*` or "Heal:" PRs since the last measured window; latest heal-related PRs remain [#10](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/10) (first CI failed) / [#11](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/11) (first CI passed). No red run this session, so no heal was invoked. |
| **What it tells us** | Metric is stale by design (no drift to repair). Masked-regression discipline holds at 0. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **Unchanged: first-PR CI green 2 / 2 (100%)** ([#7](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/7) DS-4, [#8](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/8) DS-1). **Full gate (green + conforming + maps-to-AC): still incomplete / unknown.** |
| **How measured** | `gh pr list` — no new `test(DS-*)` generation PRs this window (recent PRs #67–#76 are `docs(eval)` empty-scan commits). Standing specs DS-1–DS-5 exist under `tests/` and `features/`. |
| **What it tells us** | Backlog automation has not produced new generation PRs since Jira auth blocked the queue; gate metrics are unrefreshed. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **This session (2026-11-10 backlog scan): 0 asks; 0 invented tickets or AC.** Did not process Jira queue without authenticated MCP — no silent ticket picks. |
| **How measured** | Session review. `GetDynamicTools` → Atlassian `needsAuth`; `mcp_auth` rejected in Cloud Agent; unauthenticated Jira REST treated as false-empty per automation memory; `gh workflow run` 403; `gh` for CI/PR window only. |
| **What it tells us** | Correct behavior under missing Jira auth is **stop**, not guess from cached snapshots or public API empty arrays. |

---

## Top reliability risk

**Backlog automation cannot enumerate Jira.** Atlassian MCP auth is unavailable in Cloud Agent; without credentials the queue is unknowable and **no ticket generation runs**. Secondary: **E2E workflow fails before tests** on `ubuntu26.04-x64` Playwright/chromium install, so even doc-scan PRs do not exercise the suite in CI.

## Next action

1. Reconnect **Atlassian** MCP for automation `1e8b0ec6-3214-47ed-ad52-fe5e53731673` under Cursor **Integrations** (or bind `ATLASSIAN_*` secrets on the Cloud Agent environment).
2. Grant integration token **`workflow_dispatch`** on `test-generation.yml` if using the GitHub Actions fallback path.
3. Fix E2E workflow Playwright install on the current GitHub-hosted runner image (`ubuntu26.04-x64`).
4. Queue work: move a DS ticket to **In Progress** without **`tests-generated`** once Jira is readable.
5. On the **next real generation or heal PR**, capture first-PR-green + conformance + AC-map in the PR body so generation-gate and heal metrics leave the stale state.
