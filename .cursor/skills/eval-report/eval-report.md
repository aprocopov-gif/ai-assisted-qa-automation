# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `legion-qa-ai-assisted-program-ann`  
**Window:** last **30** `e2e.yml` runs + related PRs (through 2026-07-22)  
**Generated:** 2026-07-22  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

### 2026-07-22 backlog batch scan (empty queue)

| | |
|---|---|
| **Queue JQL** | `project = DS AND status = "In Progress" AND (labels is EMPTY OR labels not in (tests-generated)) ORDER BY priority ASC, key ASC` |
| **Eligible tickets** | **0** — Jira REST `/rest/api/3/search/jql` returned `issues: []` (HTTP 200). Atlassian MCP `needsAuth` (labeling unavailable in Cloud Agent). |
| **Corroboration** | GH Test Generation [29829799189](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/29829799189) (2026-07-21) authenticated scan also found empty queue; all In Progress tickets already have `tests-generated`. |
| **Processed / skipped** | **0 / 0** — per orchestrator guardrails, empty queue → exit without starting coordinator. |
| **E2E spot-check** | Last **10** `e2e.yml` runs (2026-07-17–2026-07-21 eval scans): all **success**, **0** flaky/retry markers in logs. |
| **Metrics below** | Unchanged from 2026-07-09 full refresh — no new generation or heal PRs in window. |

---

## Flake rate

| | |
|---|---|
| **Number** | **3** flaky test outcomes in **27** passing E2E runs → **3/27 runs (11%)** showed any flaky result; **~0.7%** of test executions in runs that reported counts (`1 flaky` / `143 passed + 1 flaky` each). Post–Block-15 runs ([28992695571](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/28992695571) sanity, [28992482239](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/28992482239) smoke) reported **0** flaky. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 30`, then `gh run view <id> --log` grepped for `flaky`, `Retry #`, `passed on retry`. CI uses `retries: 2` (`playwright.config.ts`). Flaky tests: `ds4-delete-program` **TC-004**, `ds2-edit-program` **TC-002**, `ds4-delete-program` **TC-017**. Auth-setup `Retry #` on failed runs = hard fails, not flakes. Cleanup 404s treated as noise. |
| **What it tells us** | Retries keep CI green, but DS-2 TC-002 and DS-4 TC-004/TC-017 are recurring timing/race candidates. |

---

## Heal success rate

| | |
|---|---|
| **Number** | **Clean heals: 1 / 2 (50%)** in the recent locator-repair window. **Masked-regression count: 0** (required target: **0**). |
| **How measured** | PR history (`gh pr list`, `gh pr checks`, `gh pr diff`): [#10](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/10) (first CI failed) vs [#11](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/11) (first CI passed). Counted only locator heals with assertions unchanged; masked-regression = `expect()` removed/weakened in heal diffs (**must stay 0**). |
| **What it tells us** | Heals without triage + Playwright MCP rediscovery can ship wrong selectors; masked-regression discipline holds at 0. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **First-PR CI green: 2 / 2 (100%)** for ticket-shaped generation PRs ([#7](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/7) DS-4, [#8](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/8) DS-1). **Full gate (green + conforming + maps-to-AC): incomplete / unknown** — not re-audited against Jira AC this refresh. |
| **How measured** | `gh pr list` for `test(DS-*)` titles; `gh pr checks` on first PR; `gh run list --workflow=test-generation.yml --limit 10`. Full gate needs green CI + `playwright-conventions.mdc` conformance + AC map in PR body. |
| **What it tells us** | Early agent-generated specs can land green on first PR, but the conforming+AC checklist is only half-instrumented. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **This refresh session: ~0 asks vs 0 invented product values**. **Prior Block-15 sample: ~2 asks vs ~5 invented defaults** (ask:guess ≈ 0.4). Broader suite history: **not measurable** from git alone. |
| **How measured** | Manual session review of agent transcripts + PR bodies (Cursor has no ask/guess telemetry). Guessing examples: `@high→@smoke` tag mapping, env aliases, branch naming without confirmation. |
| **What it tells us** | Repo exploration + `gh` evidence beats silent defaults; still prefer one explicit ask when tags or credentials are under-specified. |

---

## Top reliability risk

**Retries masking DS-4 and DS-2 flakes** — three distinct tests passed only on retry in the last 30 runs; tagged smoke/sanity slices may surface these more often in PR/push CI.

## Next action

1. **Stabilize DS-4 TC-004 and TC-017** and **DS-2 TC-002** (fix races with web-first waits; do not raise timeouts as the fix).
2. On the next generation PR, add an explicit **generation-gate checklist** (green + conventions + AC map) in the PR body and apply label **`tests-generated`**.
3. When opening a heal repair PR, use branch `heal/<spec-slug>` and prove green with **assertions unchanged** so heal success rate stays measurable under the orchestrator path.
