# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `ai-assisted-qa-automation`  
**Window:** last **30** `e2e.yml` runs + related PRs (through 2026-09-29)  
**Generated:** 2026-09-29  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**Batch scan (2026-09-29 UTC, Cursor Automation cron 10:02 UTC / 06:00 EST):** Hard stop — **Atlassian MCP** `needsAuth` (interactive auth unavailable in Cloud Agent). **Jira REST (unauthenticated):** JQL `project = DS AND status = "In Progress" AND (labels is EMPTY OR labels not in (tests-generated))` via `POST /rest/api/3/search/jql` → `issues: []`, HTTP 200 — **false empty** (same as [36464990412](https://github.com/aprocopov-gif/ai-assisted-qa-automation/actions/runs/36464990412) with invalid Basic auth). No `ATLASSIAN_*` env vars in this Cloud Agent pod. **Processed 0 / 5** tickets; no specs, no ticket PRs, no `tests-generated` labels. Did not invent tickets from local `features/` (DS-1…DS-5 already have plans/specs). Open docs PR [#35](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/35) records the same blocker from 2026-09-28. **No new Playwright execution data** since 2026-07-09 for flake/heal/generation numerators below — metrics retained with this dated confirmation.

**Batch scan (2026-09-28 UTC, GH Test Generation [36464990412](https://github.com/aprocopov-gif/ai-assisted-qa-automation/actions/runs/36464990412)):** Hard stop — `ATLASSIAN_*` / `JIRA_PROJECT_KEY` present in `dev1`, but **`GET /rest/api/3/myself` → 401** (Basic auth email+API token). JQL returned `issues: []` (false empty). `GET /rest/api/3/issue/DS-1` → **404** (invisible).

---

## Flake rate

| | |
|---|---|
| **Number** | **3** flaky test outcomes in **27** passing E2E runs → **3/27 runs (11%)** showed any flaky result; **~0.7%** of test executions in runs that reported counts (`1 flaky` / `143 passed + 1 flaky` each). Post–Block-15 runs ([28992695571](https://github.com/aprocopov-gif/ai-assisted-qa-automation/actions/runs/28992695571) sanity, [28992482239](https://github.com/aprocopov-gif/ai-assisted-qa-automation/actions/runs/28992482239) smoke) reported **0** flaky. **2026-09-29:** unchanged — recent `e2e.yml` activity is eval/backlog scan PRs, not full suite re-runs. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 30`, then `gh run view <id> --log` grepped for `flaky`, `Retry #`, `passed on retry`. CI uses `retries: 2` (`playwright.config.ts`). Flaky tests: `ds4-delete-program` **TC-004**, `ds2-edit-program` **TC-002**, `ds4-delete-program` **TC-017**. Auth-setup `Retry #` on failed runs = hard fails, not flakes. Cleanup 404s treated as noise. |
| **What it tells us** | Retries keep CI green, but DS-2 TC-002 and DS-4 TC-004/TC-017 are recurring timing/race candidates. |

---

## Heal success rate

| | |
|---|---|
| **Number** | **Clean heals: 1 / 2 (50%)** in the recent locator-repair window. **Masked-regression count: 0** (required target: **0**). **2026-09-29:** unchanged — no new heal PRs since last refresh. |
| **How measured** | PR history (`gh pr list`, `gh pr checks`, `gh pr diff`): [#10](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/10) (first CI failed) vs [#11](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/11) (first CI passed). Counted only locator heals with assertions unchanged; masked-regression = `expect()` removed/weakened in heal diffs (**must stay 0**). |
| **What it tells us** | Heals without triage + Playwright MCP rediscovery can ship wrong selectors; masked-regression discipline holds at 0. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **First-PR CI green: 2 / 2 (100%)** for ticket-shaped generation PRs ([#7](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/7) DS-4, [#8](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/8) DS-1). **Full gate (green + conforming + maps-to-AC): incomplete / unknown** — not re-audited against Jira AC this refresh. **2026-09-29:** **0** generation PRs this batch (Jira auth blocked). |
| **How measured** | `gh pr list` for `test(DS-*)` titles; `gh pr checks` on first PR; `gh run list --workflow=test-generation.yml --limit 10`. Full gate needs green CI + `playwright-conventions.mdc` conformance + AC map in PR body. |
| **What it tells us** | Early agent-generated specs can land green on first PR, but the conforming+AC checklist is only half-instrumented. Backlog blocked when Jira credentials are invalid or MCP is unauthenticated. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **2026-09-29 batch: 0 asks, 0 invented tickets** — stopped after Atlassian MCP auth failure + unauthenticated JQL false empty; did not invent DS keys from local `features/`. **Prior Block-15 sample: ~2 asks vs ~5 invented defaults** (ask:guess ≈ 0.4). Broader suite history: **not measurable** from git alone. |
| **How measured** | Manual session review of this agent run + PR bodies (Cursor has no ask/guess telemetry). |
| **What it tells us** | Validating auth before treating empty JQL as “no work” avoids false empty-backlog exits; rotate secrets and authenticate Atlassian MCP in Cloud Agent before re-running. |

---

## Top reliability risk

**Backlog automation blocked by Jira access** — Cloud Agent Atlassian MCP `needsAuth`; GitHub `dev1` credentials return **401** on `/rest/api/3/myself` ([36464990412](https://github.com/aprocopov-gif/ai-assisted-qa-automation/actions/runs/36464990412)). Unauthenticated JQL returns `issues: []` and must not be read as an empty queue.

## Next action

1. **Rotate/fix `ATLASSIAN_API_TOKEN`** (and matching `ATLASSIAN_EMAIL`) in GitHub **`dev1`**; confirm `GET /rest/api/3/myself` → **200**.
2. **Authenticate Atlassian MCP** for the Cloud Agent automation (Cursor desktop IDE → MCP auth).
3. Ensure at least one DS ticket is **In Progress** without the `tests-generated` label.
4. **Stabilize DS-4 TC-004/TC-017** and **DS-2 TC-002** when the next full E2E window runs (web-first waits; no timeout inflation).
