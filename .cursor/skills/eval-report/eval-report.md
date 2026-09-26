# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `legion-qa-ai-assisted-program-ann`  
**Window:** last **30** `e2e.yml` runs + related PRs (through 2026-09-26)  
**Generated:** 2026-09-26  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**Backlog batch note (2026-09-26):** Orchestrator could **not** read the DS In Progress queue. `GET ${ATLASSIAN_BASE_URL}/rest/api/3/myself` with `ATLASSIAN_EMAIL` + `ATLASSIAN_API_TOKEN` returned **HTTP 401** (`x-seraph-loginreason: AUTHENTICATED_FAILED`). Project `DS` and issue `DS-1` were unreachable. **Tickets processed: 0 / 5 budget.** No specs written; no ticket PRs opened. Atlassian MCP also unavailable (`needsAuth`; interactive auth not supported in this agent environment).

---

## Flake rate

| | |
|---|---|
| **Number** | **Insufficient new flake evidence in this window’s downloadable logs** for the newest runs; prior measurement (through 2026-07-09) remains the last quantified flake sample: **3 flaky outcomes in 27 passing E2E runs (~11% of runs; ~0.7% of executions)**. Newest e2e successes ([36203877159](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/36203877159), [36203874961](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/36203874961)) showed **0** `flaky` / `Retry #` / `passed on retry` markers in `gh run view --log`. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 30`; grepped recent run logs for `flaky`, `Retry #`, `passed on retry`. CI uses `retries: 2`. Most of the last-30 list are empty-backlog docs PRs (smoke-only), not full regression — flake denominators from those runs are not comparable to the July suite sample. |
| **What it tells us** | No new flake signal in the latest smoke-sized greens; historical DS-2/DS-4 retry flakes are still the last known suite risk until a fuller regression window is re-logged. |

---

## Heal success rate

| | |
|---|---|
| **Number** | **No new locator-heal PRs in this window.** Prior: **Clean heals 1 / 2 (50%)**; **masked-regression count: 0**. |
| **How measured** | `gh pr list --state all --search 'heal OR Heal'`; prior [#10](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/10) / [#11](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/11). This batch performed **0** heals (queue unreachable). |
| **What it tells us** | Heal rate unchanged; masked-regression discipline still at 0. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **This batch: 0 / 0** (no ticket generation attempted). **Recent `test-generation.yml`:** last completed runs through 2026-09-25 are **failures** before generation (e.g. [36156034228](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/36156034228) — Cursor usage limit), so they do **not** count as generation-gate samples. Prior ticket-first greens remain **2 / 2 (100%)** for [#7](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/7) / [#8](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/8). |
| **How measured** | `gh run list --workflow=test-generation.yml --limit 10`; `gh pr list` for `test(DS-*)`. Full gate = first PR CI green + conventions + AC map. |
| **What it tells us** | Generation gate is stalled upstream of Playwright: invalid/expired Jira token and intermittent Cursor usage limits prevent AC→spec PRs from entering the gate. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **This session: 1 ask (rotate/fix `ATLASSIAN_API_TOKEN`) vs 0 invented ticket ACs or specs** — ask:guess = stop-without-guess. |
| **How measured** | Session review: Jira REST 401 verified; did not invent In Progress tickets from `block2/` or `features/` caches; did not write specs without live AC. |
| **What it tells us** | Correct stop on missing auth; next run needs working Jira credentials before any generation-gate work. |

---

## Top reliability risk

**Jira API auth failure blocks the entire backlog pipeline** — `ATLASSIAN_API_TOKEN` (paired with `ATLASSIAN_EMAIL` against `https://legionqaschool.atlassian.net`) returns 401, so In Progress tickets cannot be selected or labeled `tests-generated`. Secondary: recent `test-generation.yml` failures from Cursor usage limits.

## Next action

1. **Rotate / re-issue `ATLASSIAN_API_TOKEN`** for `legion.jira@proton.me` on `legionqaschool.atlassian.net` and update the GitHub Actions secret (and local env). Confirm with `GET /rest/api/3/myself` → 200.
2. Re-run backlog mode; process up to 5 In Progress tickets missing `tests-generated`.
3. Keep prior flake follow-ups (DS-4 TC-004/TC-017, DS-2 TC-002) for the next green suite window with downloadable full logs.
