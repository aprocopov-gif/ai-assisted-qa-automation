# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `legion-qa-ai-assisted-program-ann`  
**Window:** last **30** `e2e.yml` runs + related PRs (through 2026-09-05)  
**Generated:** 2026-09-05  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**Dated note (2026-09-05 backlog batch):** Orchestrator **hard-stopped** before ticket processing. `GET /rest/api/3/myself` against `ATLASSIAN_BASE_URL` (`https://legionqaschool.atlassian.net`) with `ATLASSIAN_EMAIL` + `ATLASSIAN_API_TOKEN` returned **401** (`AUTHENTICATED_FAILED`). `GET /rest/api/3/search/jql?jql=project=DS…` returned `{"issues":[],"isLast":true}` — **not** treated as an empty In Progress queue (unauthenticated/empty search is indistinguishable from no tickets). `GET /rest/api/3/project/DS` returned **404** under the same credentials. Atlassian MCP namespace `plugin-atlassian-atlassian` is `needsAuth`; interactive `mcp_auth` is unavailable in this headless runner. **Tickets processed: 0 / budget 5.** No generation PRs opened. Metrics below retain the last evidence-based suite window (through 2026-07-09); the current last-30 `e2e.yml` list is **30/30** empty-backlog docs PR/push pairs (#16–#32 era), which do not re-measure flake.

---

## Flake rate

| | |
|---|---|
| **Number** | **Prior evidence (through 2026-07-09): 3** flaky test outcomes in **27** passing E2E runs → **3/27 runs (11%)** showed any flaky result; **~0.7%** of test executions in runs that reported counts. **This refresh (2026-09-05): insufficient data** — last 30 `e2e.yml` runs are entirely `docs(eval-report): empty backlog batch scan` PR/push pairs, not suite smoke/sanity/regression logs. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 30` on 2026-09-05; prior flake detail from earlier eval-report window (`gh run view` grepped for `flaky`, `Retry #`). CI uses `retries: 2`. |
| **What it tells us** | Empty-backlog automation noise has crowded out suite flake signal; restore a suite-focused window after Jira auth is fixed and generation resumes. |

---

## Heal success rate

| | |
|---|---|
| **Number** | **Clean heals: 1 / 2 (50%)** in the locator-repair window (unchanged — no new heal PRs since prior report). **Masked-regression count: 0**. |
| **How measured** | PR history: [#10](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/10) vs [#11](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/11). No new `heal/*` PRs in open list through 2026-09-05. |
| **What it tells us** | Heal path idle; masked-regression discipline still at 0 on last heals. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **Ticket-first generation PRs historically: 2 / 2 (100%)** first-PR CI green ([#7](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/7) DS-4, [#8](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/8) DS-1). **This batch: 0 / 0** (blocked on Jira 401 — no specs generated). |
| **How measured** | `gh pr list`; `gh run list --workflow=test-generation.yml --limit 10` (2026-09-05 in progress / queued; success 2026-09-04, 09-02, 09-01; failures 2026-08-27–31 and 2026-09-03). |
| **What it tells us** | Generation cannot clear the gate until Jira REST credentials work; do not count empty-backlog docs PRs as generation-gate samples. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **This session: 1 ask (fix secrets) vs 0 invented tickets/ACs/paths.** Did **not** treat unauthenticated empty `search/jql` as an empty backlog, and did **not** invent work from local `features/DS-*.feature.md` alone. |
| **How measured** | Session review: verified `myself` 401, `project/DS` 404, declined to invent DS tickets from local features or empty search. |
| **What it tells us** | Correct stop on missing auth beats guessing an empty queue from a permissive search response. |

---

## Top reliability risk

**Jira API auth failure (401)** blocks backlog mode entirely — `ATLASSIAN_EMAIL` / `ATLASSIAN_API_TOKEN` (or account/token pairing for `legionqaschool.atlassian.net`) must be repaired in the runner/environment secrets before any In Progress ticket can be analyzed.

## Next action

1. **Rotate/recreate** the Atlassian API token for the account in `ATLASSIAN_EMAIL`, update secrets `ATLASSIAN_API_TOKEN` / `ATLASSIAN_EMAIL` / `ATLASSIAN_BASE_URL`, and confirm `GET /rest/api/3/myself` returns 200 and `GET /rest/api/3/project/DS` returns the project.
2. Re-run **Test Generation**; process In Progress tickets missing `tests-generated`.
3. Close or merge the backlog of open empty-backlog eval-report docs PRs (#16–#32) so they stop dominating the E2E sample window.
