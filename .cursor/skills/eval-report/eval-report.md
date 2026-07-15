# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `legion-qa-ai-assisted-program-ann`  
**Window:** last **30** `e2e.yml` runs + related PRs (through 2026-07-15)  
**Generated:** 2026-07-15  

**Batch note (2026-07-15):** Backlog automation scan — Jira queue empty (`issues: []` for In Progress DS tickets without `tests-generated`). Atlassian MCP `needsAuth` (interactive auth unavailable in Cloud Agent); unauthenticated Jira REST corroborates empty queue. GH Test Generation [29331406669](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/29331406669) (2026-07-14) also completed with **0 eligible tickets** (all In Progress DS tickets already labeled `tests-generated`). **0 tickets processed**; no generation PRs opened this run.

**Batch note (2026-07-14):** Backlog automation scan — Jira queue empty (`issues: []` for In Progress DS tickets without `tests-generated`). Atlassian MCP `needsAuth` (interactive auth unavailable in Cloud Agent); unauthenticated Jira REST corroborates empty queue. GH Test Generation [29191733137](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/29191733137) (2026-07-12) also completed with no new PRs. **0 tickets processed**; no generation PRs opened this run.

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

---

## Flake rate

| | |
|---|---|
| **Number** | **0** runs with flaky/retry signals in **27** passing E2E runs → **0/27 runs (0%)** showed any flaky result in the current window. Latest green runs ([29324034850](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/29324034850), [29241387553](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/29241387553), [29188489392](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/29188489392)) report **49 passed, 0 flaky** each. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 30`, then `gh run view <id> --log` grepped for `flaky`, `Retry #`, `passed on retry`. CI uses `retries: 2` (`playwright.config.ts`). Auth-setup `Retry #` on failed runs = hard fails, not flakes. Cleanup 404s treated as noise. |
| **What it tells us** | Flake rate remains at 0% in the current window; recent empty-backlog eval commits land green with 0 flaky. |

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
| **Number** | **This refresh session: 0 asks vs 0 invented product values** (empty queue — no spec generation). **Prior Block-15 sample: ~2 asks vs ~5 invented defaults** (ask:guess ≈ 0.4). Broader suite history: **not measurable** from git alone. |
| **How measured** | Manual session review of agent transcripts + PR bodies (Cursor has no ask/guess telemetry). This run used Jira REST + GH Actions corroboration instead of inventing ticket keys. |
| **What it tells us** | Empty-queue guardrail worked — no invented tickets or specs. Atlassian MCP auth remains the blocker for live labeling. |

---

## Top reliability risk

**Backlog automation blocked on Jira access in Cloud Agent** — Atlassian MCP requires desktop IDE auth; unauthenticated REST returns empty results, preventing queue discovery and `tests-generated` labeling even when tickets exist.

## Next action

1. **Authenticate Atlassian MCP** in Cursor desktop IDE so Cloud Agent runs can query Jira and add labels.
2. To queue work: move a DS ticket to **In Progress** and remove (or omit) the **`tests-generated`** label.
3. **Stabilize DS-4 TC-004/TC-017** and **DS-2 TC-002** if flakes reappear in PR/push CI (web-first waits; do not raise timeouts as the fix).
