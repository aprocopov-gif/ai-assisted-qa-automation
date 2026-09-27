# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `ai-assisted-qa-automation`  
**Window:** last **30** `e2e.yml` runs + related PRs (through 2026-09-27)  
**Generated:** 2026-09-27  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**Batch scan (2026-09-27 ~15:30 UTC):** Orchestrator backlog run **blocked on Jira auth** — `ATLASSIAN_EMAIL` + `ATLASSIAN_API_TOKEN` present but `GET /rest/api/3/myself` → **HTTP 401**; `GET /rest/api/3/issue/DS-1` → **404** (no permission / invisible). Search `/rest/api/3/search/jql` returns `issues: []` both with and without Basic auth (false empty — not a confirmed empty queue). Atlassian MCP `needsAuth` (interactive auth unavailable in this agent environment). Did **not** invent tickets from local `features/`. This run: **0 / 5** tickets processed. Corroboration: morning scan [PR #34](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/34); GH Test Generation [36249948787](https://github.com/aprocopov-gif/ai-assisted-qa-automation/actions/runs/36249948787) (2026-09-26) also **0 / 5**. **No new Playwright suite execution data** for flake/heal/generation numerators — metrics retained with this dated confirmation.

---

## Flake rate

| | |
|---|---|
| **Number** | **3** flaky test outcomes in **27** passing E2E runs → **3/27 runs (11%)** showed any flaky result; **~0.7%** of test executions in runs that reported counts (`1 flaky` / `143 passed + 1 flaky` each). Post–Block-15 runs ([28992695571](https://github.com/aprocopov-gif/ai-assisted-qa-automation/actions/runs/28992695571) sanity, [28992482239](https://github.com/aprocopov-gif/ai-assisted-qa-automation/actions/runs/28992482239) smoke) reported **0** flaky. **2026-09-27 afternoon:** unchanged — recent `e2e.yml` activity is eval/backlog scan / chore PRs, not full suite re-runs. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 30`, then `gh run view <id> --log` grepped for `flaky`, `Retry #`, `passed on retry`. CI uses `retries: 2` (`playwright.config.ts`). Flaky tests: `ds4-delete-program` **TC-004**, `ds2-edit-program` **TC-002**, `ds4-delete-program` **TC-017**. Auth-setup `Retry #` on failed runs = hard fails, not flakes. Cleanup 404s treated as noise. |
| **What it tells us** | Retries keep CI green, but DS-2 TC-002 and DS-4 TC-004/TC-017 are recurring timing/race candidates. |

---

## Heal success rate

| | |
|---|---|
| **Number** | **Clean heals: 1 / 2 (50%)** in the recent locator-repair window. **Masked-regression count: 0** (required target: **0**). **2026-09-27 afternoon:** unchanged — no new heal PRs since last refresh. |
| **How measured** | PR history (`gh pr list`, `gh pr checks`, `gh pr diff`): [#10](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/10) (first CI failed) vs [#11](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/11) (first CI passed). Counted only locator heals with assertions unchanged; masked-regression = `expect()` removed/weakened in heal diffs (**must stay 0**). |
| **What it tells us** | Heals without triage + Playwright MCP rediscovery can ship wrong selectors; masked-regression discipline holds at 0. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **First-PR CI green: 2 / 2 (100%)** for ticket-shaped generation PRs ([#7](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/7) DS-4, [#8](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/8) DS-1). **Full gate (green + conforming + maps-to-AC): incomplete / unknown** — not re-audited against Jira AC this refresh. **2026-09-27 afternoon:** **0** generation PRs this batch (Jira auth blocked; queue unreadable). |
| **How measured** | `gh pr list` for `test(DS-*)` titles; `gh pr checks` on first PR; `gh run list --workflow=test-generation.yml --limit 10`. Full gate needs green CI + `playwright-conventions.mdc` conformance + AC map in PR body. |
| **What it tells us** | Early agent-generated specs can land green on first PR, but the conforming+AC checklist is only half-instrumented. Backlog automation cannot start until Jira Basic auth succeeds. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **2026-09-27 afternoon: 0 invented tickets** — stopped after Jira **401**; did not invent DS keys from local `features/`. Escalated auth failure rather than treating empty JQL as an empty backlog. **Prior Block-15 sample: ~2 asks vs ~5 invented defaults** (ask:guess ≈ 0.4). Broader suite history: **not measurable** from git alone. |
| **How measured** | Manual session review of this run + PR bodies (Cursor has no ask/guess telemetry). |
| **What it tells us** | Empty JQL without a successful `/myself` is not evidence of an empty queue; fix secrets before claiming “no work”. |

---

## Top reliability risk

**Backlog automation blocked by invalid/expired Jira API credentials** — `ATLASSIAN_API_TOKEN` + `ATLASSIAN_EMAIL` yield HTTP 401 on `/myself`; search returns a false-empty `issues: []`. Risk: cron reports “0 tickets” while In Progress work may exist.

## Next action

1. **Rotate/fix `ATLASSIAN_API_TOKEN`** (and matching `ATLASSIAN_EMAIL`) in the `dev1` GitHub environment secrets; verify with `GET /rest/api/3/myself` → 200.
2. Optionally authenticate Atlassian MCP in Cursor desktop for labeling `tests-generated` from interactive sessions.
3. After auth works: ensure at least one DS ticket is **In Progress** without `tests-generated`, then re-run Test Generation.
4. **Stabilize DS-4 TC-004/TC-017** and **DS-2 TC-002** when the next full E2E window runs (web-first waits; no timeout inflation).
