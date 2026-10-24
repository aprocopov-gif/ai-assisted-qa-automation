# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `legion-qa-ai-assisted-program-ann`  
**Window:** Daily backlog-scan `e2e.yml` runs 2026-10-21 → 2026-10-23 (smoke slice on eval PRs) + this session (2026-10-24)  
**Generated:** 2026-10-24  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**This refresh trigger:** Backlog batch (cron 2026-10-24) — **0 / 5 tickets processed**. Atlassian MCP auth unavailable in Cloud Agent; unauthenticated Jira REST returned empty queue (`issues: []`, HTTP 200); `workflow_dispatch` for `test-generation.yml` returned HTTP 403 on integration token.

---

## Flake rate

| | |
|---|---|
| **Number** | **5 flaky test outcomes** across **2** completed Playwright E2E runs in window (runs `39760054581`, `39581605540`). Totals: **71 passed**, **4 failed**, **5 flaky** (smoke slice ~40 tests). Run `39936328868` (2026-10-23) failed at **browser install** — excluded from flake math. → **~7%** flaky among executed tests in those two runs (5 / 71). |
| **How measured** | `gh run list --workflow=e2e.yml --limit 5`, then `gh run view <id> --log` grepped for summary lines `failed`, `flaky`, `passed`. |
| **What it tells us** | Flake pressure persists on the standing suite during daily eval PRs (4 flaky on 2026-10-22 vs 1 on 2026-10-21). No new generation specs this window — flakes are on existing coverage, not fresh AC maps. |

---

## Heal success rate

| | |
|---|---|
| **Number** | **Unchanged: 1 / 2 (50%)** — no new locator-heal PRs this window. **Masked-regression count: 0**. |
| **How measured** | `gh pr list --state all` — no new `heal/*` PRs since prior window; no heal invoked this session (no ticket work started). |
| **What it tells us** | Red CI on eval PRs was not triaged/healed this run; metric stale but masked-regression discipline unchanged at 0. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **Unchanged: first-PR CI green 2 / 2 (100%)** on historical DS-1/DS-4 generation PRs. **0 new generation PRs** in this window (backlog blocked). |
| **How measured** | Session outcome: 0 tickets analyzed → 0 specs written. `gh pr list` — recent PRs remain `docs(eval-report)` backlog-scan commits only. |
| **What it tells us** | Automation cannot score fresh generation-gate evidence until Jira credentials work in Cloud Agent or GitHub Actions `test-generation.yml` is dispatchable. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **0 clarifying asks; 0 invented ticket/AC/locator values.** |
| **How measured** | Session review. Did not fabricate a ticket queue from empty unauthenticated Jira response; recorded auth failures explicitly; did not write specs without AC. |
| **What it tells us** | Correct stop when MCP auth and REST credentials are missing — avoids guessing which DS tickets are In Progress. |

---

## Top reliability risk

**Backlog automation blocked on Jira + CI infra.** Without Atlassian MCP auth (or `ATLASSIAN_*` in the agent environment), the orchestrator cannot reliably fetch the In Progress queue or apply `tests-generated`. The 2026-10-23 eval PR CI run failed before tests (`Failed to install browsers`), adding noise atop existing suite flakes (2 failed / 4 flaky on 2026-10-22).

## Next action

1. **Authenticate Atlassian MCP** for the Cloud Agent environment (or inject `ATLASSIAN_BASE_URL`, `ATLASSIAN_EMAIL`, `ATLASSIAN_API_TOKEN`, `JIRA_PROJECT_KEY`) so backlog JQL and labeling work.
2. **Grant `workflow_dispatch`** on `test-generation.yml` to the automation/integration token as a fallback runner with secrets.
3. **Fix E2E workflow browser install** on eval PR branches so daily scans produce test signal (not setup failures).
4. On the next successful generation PR, capture first-PR-green + conformance + AC-map in the PR body.
