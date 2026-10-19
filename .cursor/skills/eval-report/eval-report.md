# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `legion-qa-ai-assisted-program-ann`  
**Window:** `e2e.yml` runs 2026-10-16 → 2026-10-18 (daily backlog-scan PR/push pairs) + this session’s queue probe  
**Generated:** 2026-10-19  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data** when evidence is missing.

**This refresh trigger:** **Backlog mode** cron (06:00 EST / 10:00 UTC). **0 / 5** tickets processed — Jira queue could not be read authentically; no specs generated.

---

## Flake rate

| | |
|---|---|
| **Number** | Run `39117665199` (2026-10-18 smoke): **2 failed / 38 passed**, **0 flaky** in summary. Prior: `39023356937` (2026-10-17) **2 failed / 37 passed**, **1 flaky** (DS-1 TC-002); `38884637019` (2026-10-16) **2 failed / 38 passed**, **0 flaky**. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 15`; `gh run view <id> --log` grepped for `flaky`, `Retry #`, `failed`, `passed (`. |
| **What it tells us** | Eval PR smoke remains **red** (~2 failures) on create/edit paths; flake count dropped to 0 on the latest run but retries still appear in logs. |

---

## Heal success rate

| | |
|---|---|
| **Number** | **Unchanged: 1 / 2 (50%)** — no new locator-heal PRs this window. **Masked-regression count: 0**. |
| **How measured** | `gh pr list --state open --limit 20` — recent PRs are `docs(eval)` backlog scans; no `heal/*` or “Heal:” titles since prior window. |
| **What it tells us** | Heal path idle; recurring red smoke on eval PRs was not triaged this window. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **0 new ticket generation PRs** this window → **insufficient data** for first-PR gate refresh. Historical first-PR CI green remains **2 / 2** on legacy PRs #7 (DS-4) and #8 (DS-1). |
| **How measured** | `gh pr list` — no `test(DS-*)` or `qa/DS-*` generation PRs; backlog automation blocked before analyze/implement. |
| **What it tells us** | Generation gate cannot improve until Jira auth unblocks queue fetch and spec work. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **This session: 0 asks (no human present), 0 invented tickets/AC/locators.** |
| **How measured** | Session review. Atlassian MCP `needsAuth` (interactive `mcp_auth` unavailable in Cloud Agent); unauthenticated Jira REST (`legionqaschool.atlassian.net/rest/api/3/search/jql`, JQL: In Progress DS without `tests-generated`) returned empty `issues[]` (HTTP 200 — false empty); did **not** pick tickets from stale memory snapshot. `gh workflow run test-generation.yml` → 403 (integration token). Agent run: https://cursor.com/agents/bc-9a046827-5875-497d-847d-3bac8f512402 |
| **What it tells us** | Guardrail held: empty/unauthenticated Jira ≠ “no work in Jira”; automation correctly no-oped rather than guessing DS keys. |

---

## Top reliability risk

**Jira authentication gap in Cloud Agent** blocks the entire backlog pipeline (queue → analyze → spec → `tests-generated` label). Secondary risk: **recurring red eval PR smoke** (`39117665199`: 2 failed on DS-1/DS-2 paths) without triage — likely edit/list drift, timing, or product regressions.

## Next action

1. **Authenticate Atlassian MCP** for the Cloud Agent environment (or inject `ATLASSIAN_EMAIL` + `ATLASSIAN_API_TOKEN` into the automation env) so queue fetch and labeling work.
2. Grant **`workflow_dispatch`** on `test-generation.yml` for the automation token as a fallback path with authenticated Jira in `dev1` secrets.
3. Triage **2026-10-18** eval PR smoke (`39117665199`); if classified as drift, open a `heal/*` PR with assertions unchanged.
