# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `legion-qa-ai-assisted-program-ann`  
**Window:** last **30** `e2e.yml` runs + related PRs (through 2026-07-30)  
**Generated:** 2026-07-30  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

---

## Flake rate

| | |
|---|---|
| **Number** | **1** flaky test outcome in **30** passing E2E runs → **1/30 runs (3%)** showed a flaky result. Flaky test: `ds5-program-list-display` **TC-002** (Empty state when no programs exist) in run [30442096403](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/30442096403) (2026-07-29). Prior window (through 2026-07-09) had **3/27 runs (11%)** with DS-2/DS-4 flakes. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 30`, then `gh run view <id> --log` grepped for `flaky`, `Retry #`, `passed on retry`. All 30 most recent runs (IDs 29324029171–30442096403) are green; only one reported `1 flaky`. CI uses `retries: 2` (`playwright.config.ts`). |
| **What it tells us** | DS-5 TC-002 is a new flake candidate; prior DS-2/DS-4 cluster has not recurred in this 30-run window. |

---

## Heal success rate

| | |
|---|---|
| **Number** | **Clean heals: 1 / 2 (50%)** in the recent locator-repair window (unchanged). **Masked-regression count: 0** (required target: **0**). |
| **How measured** | PR history (`gh pr list`, `gh pr checks`, `gh pr diff`): [#10](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/10) (first CI failed) vs [#11](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/11) (first CI passed). No new `heal/*` PRs since last refresh. |
| **What it tells us** | Heal discipline holds; no new drift repairs to score this window. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **First-PR CI green: 2 / 2 (100%)** for ticket-shaped generation PRs ([#7](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/7) DS-4, [#8](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/8) DS-1). **This batch: 0 generation PRs** — backlog queue empty (all 10 In Progress DS tickets already labeled `tests-generated`). |
| **How measured** | `gh run list --workflow=test-generation.yml --limit 3`; authenticated Jira scan in [30453852479](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/30453852479) (2026-07-29) confirmed **0 eligible** tickets. Unauthenticated Jira REST fallback also returned `issues: []`. |
| **What it tells us** | Generation pipeline is idle until a ticket moves to In Progress without `tests-generated`. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **This batch session: ~0 asks vs 0 invented product values**. Used automation memory + GH workflow logs for queue state; did not fabricate ticket keys or ACs. **Prior Block-15 sample: ~2 asks vs ~5 invented defaults** (ask:guess ≈ 0.4). |
| **How measured** | Manual session review of this automation run + prior agent transcripts. Atlassian MCP unavailable (`needsAuth`); corroborated empty queue via authenticated GH Actions Jira scan [30453852479](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/30453852479) rather than guessing ticket availability. |
| **What it tells us** | Empty-queue runs should exit early with evidence from authenticated CI scans; Jira labeling remains blocked until Atlassian MCP is authenticated in Cloud Agent. |

---

## Top reliability risk

**Backlog exhaustion + Jira auth gap in Cloud Agent** — all In Progress DS tickets are labeled `tests-generated`, so the automation produces no new specs; Atlassian MCP `needsAuth` prevents live labeling even when work exists. DS-5 TC-002 flaked once in the latest window.

## Next action

1. **Queue work:** move a DS ticket to **In Progress** and remove `tests-generated` when regenerated tests are needed.
2. **Authenticate Atlassian MCP** in Cursor desktop so Cloud Agent runs can label tickets after PRs open.
3. **Investigate DS-5 TC-002 flake** — empty-state assertion may race against program cleanup; stabilize with web-first waits, not timeout increases.
