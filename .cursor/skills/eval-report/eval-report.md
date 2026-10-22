# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `legion-qa-ai-assisted-program-ann`  
**Window:** `e2e.yml` runs 2026-10-18 → 2026-10-21 (daily backlog-scan PR/push pairs) + this session’s queue probe  
**Generated:** 2026-10-22  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**This refresh trigger:** **Backlog mode** cron (06:00 EST / 10:00 UTC). **0 / 5** tickets processed — Jira queue could not be read authentically; no specs generated.

---

## Flake rate

| | |
|---|---|
| **Number** | Run `39581605540` (2026-10-21 smoke): **2 failed / 37 passed**, **1 flaky** in summary. Prior: `39405166574` (2026-10-20) **5 failed / 32 passed**, **2 flaky**; `39234677033` (2026-10-19) **5 failed / 31 passed**, **4 flaky**; `39117665199` (2026-10-18) **2 failed / 38 passed**, **0 flaky**. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 15`; `gh run view <id> --log` grepped for `flaky`, `Retry #`, `failed`, `passed (`. |
| **What it tells us** | Eval PR smoke improved on 2026-10-21 (2 hard failures vs 5 on 10-20) but remains red with at least one flaky create/edit path. |

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
| **How measured** | Session review. Atlassian MCP `needsAuth` (`mcp_auth_error` on run start); unauthenticated Jira REST (`legionqaschool.atlassian.net/rest/api/3/search/jql`, JQL: In Progress DS without `tests-generated`) returned empty `issues[]` (HTTP 200 — false empty); did **not** pick tickets from stale memory snapshot. `gh workflow run test-generation.yml` → 403 (integration token). Agent run: https://cursor.com/agents/bc-d065a718-c656-435b-a562-1d7561619770 |
| **What it tells us** | Guardrail held: empty/unauthenticated Jira ≠ “no work in Jira”; automation correctly no-oped rather than guessing DS keys. |

---

## Top reliability risk

**Jira authentication gap in Cloud Agent** blocks the entire backlog pipeline (queue → analyze → spec → `tests-generated` label). Secondary risk: **persistent eval PR smoke failures** (latest `39581605540`: 2 failed, 1 flaky) without triage — likely edit/list drift, timing, or product regressions on DS-1/DS-2 paths.

## Next action

1. **Authenticate Atlassian MCP** for this automation (Cursor Integrations dashboard) **or** add `ATLASSIAN_*` + `DIDAXIS_*` to the Cloud Agent environment / run `test-generation.yml` via `workflow_dispatch` with a token that has `actions:write`.
2. After auth works, re-run backlog mode on DS tickets in **In Progress** without **`tests-generated`** (budget 5).
3. Triage red smoke on the latest eval PR (`39581605540`) — classify drift vs app bug before the next generation PR adds more surface area.
