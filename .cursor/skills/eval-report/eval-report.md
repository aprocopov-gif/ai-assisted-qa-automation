# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `legion-qa-ai-assisted-program-ann`  
**Window:** last **30** `e2e.yml` runs + related PRs (through 2026-09-27)  
**Generated:** 2026-09-27  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**Batch scan (2026-09-27 UTC):** Cloud Agent backlog run — Atlassian MCP `needsAuth`; unauthenticated Jira JQL returned **0** eligible issues. GH Test Generation [36249948787](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/36249948787) (2026-09-26) also processed **0 / 5** tickets (no readable In Progress queue). **No new Playwright execution data** since 2026-07-09 for flake/heal/generation numerators below — metrics retained with this dated confirmation.

---

## Flake rate

| | |
|---|---|
| **Number** | **3** flaky test outcomes in **27** passing E2E runs → **3/27 runs (11%)** showed any flaky result; **~0.7%** of test executions in runs that reported counts (`1 flaky` / `143 passed + 1 flaky` each). Post–Block-15 runs ([28992695571](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/28992695571) sanity, [28992482239](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/28992482239) smoke) reported **0** flaky. **2026-09-27:** unchanged — recent `e2e.yml` activity is eval/backlog scan PRs, not full suite re-runs. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 30`, then `gh run view <id> --log` grepped for `flaky`, `Retry #`, `passed on retry`. CI uses `retries: 2` (`playwright.config.ts`). Flaky tests: `ds4-delete-program` **TC-004**, `ds2-edit-program` **TC-002**, `ds4-delete-program` **TC-017**. Auth-setup `Retry #` on failed runs = hard fails, not flakes. Cleanup 404s treated as noise. |
| **What it tells us** | Retries keep CI green, but DS-2 TC-002 and DS-4 TC-004/TC-017 are recurring timing/race candidates. |

---

## Heal success rate

| | |
|---|---|
| **Number** | **Clean heals: 1 / 2 (50%)** in the recent locator-repair window. **Masked-regression count: 0** (required target: **0**). **2026-09-27:** unchanged — no new heal PRs since last refresh. |
| **How measured** | PR history (`gh pr list`, `gh pr checks`, `gh pr diff`): [#10](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/10) (first CI failed) vs [#11](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/11) (first CI passed). Counted only locator heals with assertions unchanged; masked-regression = `expect()` removed/weakened in heal diffs (**must stay 0**). |
| **What it tells us** | Heals without triage + Playwright MCP rediscovery can ship wrong selectors; masked-regression discipline holds at 0. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **First-PR CI green: 2 / 2 (100%)** for ticket-shaped generation PRs ([#7](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/7) DS-4, [#8](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/8) DS-1). **Full gate (green + conforming + maps-to-AC): incomplete / unknown** — not re-audited against Jira AC this refresh. **2026-09-27:** **0** generation PRs this batch (empty backlog). |
| **How measured** | `gh pr list` for `test(DS-*)` titles; `gh pr checks` on first PR; `gh run list --workflow=test-generation.yml --limit 10`. Full gate needs green CI + `playwright-conventions.mdc` conformance + AC map in PR body. |
| **What it tells us** | Early agent-generated specs can land green on first PR, but the conforming+AC checklist is only half-instrumented. Backlog blocked when Jira is unreadable from Cloud Agent. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **2026-09-27 batch: 0 asks, 0 invented tickets** — queue from Jira REST (unauthenticated) + corroborating GH run; did not invent DS keys from local `features/`. **Prior Block-15 sample: ~2 asks vs ~5 invented defaults** (ask:guess ≈ 0.4). Broader suite history: **not measurable** from git alone. |
| **How measured** | Manual session review of agent transcripts + PR bodies (Cursor has no ask/guess telemetry). Guessing examples: `@high→@smoke` tag mapping, env aliases, branch naming without confirmation. |
| **What it tells us** | Repo exploration + `gh` evidence beats silent defaults; authenticate Atlassian MCP for live queue + labeling. |

---

## Top reliability risk

**Backlog automation blocked without Jira auth** — Cloud Agent cannot label `tests-generated` or confirm queue state; unauthenticated search returns empty and risks false “no work” while tickets may exist.

## Next action

1. **Authenticate Atlassian MCP** in Cursor (team Cloud Agent environment) so In Progress queue and `tests-generated` labeling work on cron runs.
2. To queue work: move a DS ticket to **In Progress** and remove **`tests-generated`** until specs land.
3. **Stabilize DS-4 TC-004/TC-017** and **DS-2 TC-002** when the next full E2E window runs (web-first waits; no timeout inflation).
