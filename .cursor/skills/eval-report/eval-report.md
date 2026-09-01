# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `legion-qa-ai-assisted-program-ann`  
**Window:** last **30** `e2e.yml` runs + related PRs (through 2026-07-31)  
**Generated:** 2026-09-01  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**2026-09-01 backlog scan:** JQL `project = DS AND status = "In Progress" AND (labels is EMPTY OR labels not in (tests-generated))` returned **0** eligible tickets (HTTP 200, `issues: []`). Jira REST auth is **partially broken** in this environment: `/rest/api/3/myself` → 401; `project/DS` and `issue/DS-1` → 404 (no permission). Atlassian MCP requires desktop auth. **Budget used: 0/5.** No specs written or run.

---

## Flake rate

| | |
|---|---|
| **Number** | **2** flaky test outcomes in **30** passing E2E runs → **2/30 runs (7%)** showed any flaky result. Flaky tests: `ds4-delete-program` **TC-008** ([30622204615](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/30622204615), 2026-07-31); `ds5-program-list-display` **TC-002** ([30442096403](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/30442096403), 2026-07-29). |
| **How measured** | `gh run list --workflow=e2e.yml --limit 30`, then `gh run view <id> --log` grepped for `flaky`, `Retry #`, `passed on retry`. CI uses `retries: 2` (`playwright.config.ts`). Auth-setup `Retry #` on failed runs = hard fails, not flakes. Cleanup 404s treated as noise. |
| **What it tells us** | Retries keep CI green; DS-4 TC-008 and DS-5 TC-002 are the current flake candidates in the 30-run window (DS-2 TC-002 and DS-4 TC-004/TC-017 were flaky in the prior window). |

---

## Heal success rate

| | |
|---|---|
| **Number** | **Clean heals: 1 / 2 (50%)** in the recent locator-repair window. **Masked-regression count: 0** (required target: **0**). No new heal PRs since 2026-07-10. |
| **How measured** | PR history (`gh pr list`, `gh pr checks`, `gh pr diff`): [#10](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/10) (first CI failed) vs [#11](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/11) (first CI passed). Counted only locator heals with assertions unchanged; masked-regression = `expect()` removed/weakened in heal diffs (**must stay 0**). |
| **What it tells us** | Heal discipline holds at 0 masked regressions; no new drift heals to measure in this window. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **Idle** — empty backlog; **0** new ticket-first generation PRs this run. Historical: **2 / 2 (100%)** first-PR CI green ([#7](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/7) DS-4, [#8](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/8) DS-1). |
| **How measured** | `gh pr list` for `test(DS-*)` titles; `gh run list --workflow=test-generation.yml --limit 10`. Full gate needs green CI + `playwright-conventions.mdc` conformance + AC map in PR body. |
| **What it tells us** | Queue exhaustion blocks new generation-gate measurements; prior ticket PRs remain the baseline. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **This session: 0 asks vs 0 invented product values** (empty queue — no AC to guess). **Prior Block-15 sample: ~2 asks vs ~5 invented defaults** (ask:guess ≈ 0.4). |
| **How measured** | Manual session review of agent transcripts + PR bodies (Cursor has no ask/guess telemetry). This run stopped at Jira queue scan without inventing ticket content. |
| **What it tells us** | Empty-queue exit avoids guessing AC; Jira credential repair is needed before the next generation batch. |

---

## Top reliability risk

**Retries masking DS-4 TC-008 and DS-5 TC-002 flakes** — two runs in the last 30 needed a retry to pass; smoke/sanity slices may surface these on PR CI.

## Next action

1. **Stabilize DS-4 TC-008** and **DS-5 TC-002** (web-first waits; do not raise timeouts as the fix).
2. **Repair Jira REST credentials** (`ATLASSIAN_API_TOKEN` returns 401 on `/myself`, 404 on DS project/issues) so backlog scans and `tests-generated` labeling work in automation.
3. To queue work: move a DS ticket to **In Progress** and remove (or omit) the `tests-generated` label.
