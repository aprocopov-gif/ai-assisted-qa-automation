# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `legion-qa-ai-assisted-program-ann`  
**Window:** last **30** `e2e.yml` runs + related PRs (through 2026-07-27)  
**Generated:** 2026-07-27  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**Batch scan (2026-07-27):** Backlog queue empty — Jira REST (unauthenticated) returned 0 eligible issues; corroborated by GH Test Generation [30201228192](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/30201228192) (2026-07-26). All 10 In Progress tickets already have `tests-generated`. **Processed: 0 / 5 budget.**

---

## Flake rate

| | |
|---|---|
| **Number** | **0** flaky markers in the last **30** E2E runs scanned (2026-07-27). Prior window (through 2026-07-09) had **3** flaky outcomes in **27** passing runs → **11%** run-level flake rate with tests `ds4-delete-program` TC-004/TC-017 and `ds2-edit-program` TC-002. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 30`, then `gh run view <id> --log` grepped for `flaky`, `Retry #`, `passed on retry`. CI uses `retries: 2` (`playwright.config.ts`). Cleanup 404s treated as noise. |
| **What it tells us** | Recent eval-scan PR runs show no flakes; historical DS-2/DS-4 timing candidates remain unverified in this window (runs are mostly docs-only). |

---

## Heal success rate

| | |
|---|---|
| **Number** | **Clean heals: 1 / 2 (50%)** in the locator-repair window (unchanged). **Masked-regression count: 0** (required target: **0**). No new heal PRs since 2026-07-09. |
| **How measured** | PR history (`gh pr list`, `gh pr checks`, `gh pr diff`): [#10](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/10) vs [#11](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/11). Masked-regression = `expect()` removed/weakened in heal diffs. |
| **What it tells us** | Heal discipline holds at 0 masked regressions; no new heal activity to measure this batch. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **First-PR CI green: 2 / 2 (100%)** for ticket-shaped generation PRs ([#7](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/7) DS-4, [#8](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/8) DS-1). **Full gate (green + conforming + maps-to-AC): incomplete / unknown**. **2026-07-27 batch: 0 generation PRs** (empty queue). |
| **How measured** | `gh pr list` for `test(DS-*)` titles; `gh run list --workflow=test-generation.yml --limit 10`; Jira backlog JQL on each automation run. |
| **What it tells us** | Queue exhausted — all In Progress tickets labeled; new work requires moving unlabeled tickets to In Progress. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **This session (2026-07-27): ~0 asks vs 0 invented product values**. Used unauthenticated Jira REST + GH Actions logs instead of inventing ticket keys. **Prior Block-15 sample: ~2 asks vs ~5 invented defaults** (ask:guess ≈ 0.4). |
| **How measured** | Manual session review + automation memory + corroborating CI logs. Atlassian MCP `needsAuth` — no live Jira labeling this run. |
| **What it tells us** | Evidence-based empty-queue exit is correct; authenticate Atlassian MCP for live labeling in Cloud Agent runs. |

---

## Top reliability risk

**Empty backlog with blocked Jira access in Cloud Agent** — automation cannot add `tests-generated` labels or discover newly queued tickets without Atlassian MCP auth or env secrets.

## Next action

1. **Authenticate Atlassian MCP** in Cursor desktop IDE so Cloud Agent runs can query Jira and apply labels.
2. **Queue new work:** move a ticket to **In Progress** without `tests-generated` (e.g. from To Do backlog).
3. When DS-2/DS-4 specs run again in full E2E (not docs-only PRs), re-scan flake rate on those tests.
