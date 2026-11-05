# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `ai-assisted-qa-automation`  
**Window:** `e2e.yml` runs 2026-07-10 → 2026-07-22 (14 daily backlog-scan runs) + related PRs, plus local DS-4 re-verify  
**Generated:** 2026-07-22  

**2026-11-05 backlog scan (cron 10:02 UTC / 06:02 EDT):** Metrics **unchanged** — no ticket generation, heal, or new substantive `e2e.yml` evidence in window (recent runs remain daily auth-blocked scan PRs failing in ~10–15s). Blockers: Atlassian MCP `needsAuth` (`mcp_auth_error` on run start; interactive auth unavailable in Cloud Agent — reconnect **Atlassian** under Cursor dashboard **Integrations** for automation `1e8b0ec6-3214-47ed-ad52-fe5e53731673`); no `ATLASSIAN_*` / `DIDAXIS_*` app secrets bound; unauthenticated Jira JQL returned `issues: []` (HTTP 200, **not trustworthy**); `gh workflow run test-generation.yml` → 403. **Processed 0 / 5** tickets. Ask-vs-guess this run: **0 asks, 0 invented values** (did not guess queue contents). Agent run: https://cursor.com/agents/bc-e0d00105-2f8e-4935-9c97-07bf97f6091c

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**This refresh trigger:** single-ticket Done for **DS-4** (user-requested `run DS-4`). DS-4 already had a generated plan + spec (`tests-generated` label present); this session re-verified the existing spec rather than regenerating it.

---

## Flake rate

| | |
|---|---|
| **Number** | **0** flaky outcomes across **14** `e2e.yml` runs (2026-07-10 → 2026-07-22). Local DS-4 re-verify: **20 passed, 0 flaky, 0 retries**. → **0%** flake in the current window. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 30`, then `gh run view <id> --log` grepped for `flaky`, `Retry #`, `passed`. Sampled runs 2026-07-16→07-22 (smoke slice **40 tests → 39 passed** + 1 skip; sanity slice **54 tests → 49 passed** + 5 skips) — none reported `flaky`. Local: `npx playwright test tests/ds4-delete-program.spec.ts` → 20 passed, no `Retry #`. CI uses `retries: 2` (`playwright.config.ts`); skips are the non-admin TC-007/TC-010 gates, not failures. |
| **What it tells us** | The prior window's flake candidates (**DS-4 TC-004/TC-017**, **DS-2 TC-002**) did **not** recur — DS-4 TC-004 and TC-017 passed first-try both in CI and locally. Note: recent CI runs are daily **empty-backlog** scans exercising the standing suite, not new-code runs. |

---

## Heal success rate

| | |
|---|---|
| **Number** | **Unchanged: 1 / 2 (50%)** — no new locator-heal PRs this window. **Masked-regression count: 0** (required target: **0**). |
| **How measured** | `gh pr list --state all` — no `heal/*` or "Heal:" PRs since the last window; latest heal-related PRs remain [#10](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/10) (first CI failed) / [#11](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/11) (first CI passed). No red run this session, so no heal was invoked. |
| **What it tells us** | Metric is stale by design (no drift to repair). Masked-regression discipline holds at 0. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **Unchanged: first-PR CI green 2 / 2 (100%)** ([#7](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/7) DS-4, [#8](https://github.com/aprocopov-gif/ai-assisted-qa-automation/pull/8) DS-1). **Full gate (green + conforming + maps-to-AC): still incomplete / unknown.** |
| **How measured** | `gh pr list` — no new `test(DS-*)` generation PRs this window (all recent PRs #16–#24 are `docs(eval-report)` empty-scan commits). DS-4 re-verified **CI-adjacent green locally** this session (20/20) and its 19 TCs **map to AC** (both AC scenarios — confirm-delete + cancel — plus negatives/edges); conformance to `playwright-conventions.mdc` holds (role/label locators, one tag/test, self-cleaning via cleanup fixture). |
| **What it tells us** | No fresh generation evidence; DS-4's existing spec still passes and maps to AC, but the full conforming+AC checklist remains only half-instrumented across the suite. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **This session (DS-4 run): 0 asks vs 0 invented product values.** |
| **How measured** | Session review. Ticket read via Atlassian MCP (`getJiraIssue` DS-4); CI/PR evidence via `gh`; verification via local `npx playwright test`. No locators, credentials, or AC were invented. One judgment call recorded (not invented): proceeded despite the `tests-generated` label because the user explicitly asked to run DS-4 — flagged to the user rather than silently skipped. |
| **What it tells us** | MCP + `gh` + local run evidence continues to beat silent defaults; the single ambiguity (already-generated ticket) was surfaced, not guessed. |

---

## Top reliability risk

**Jira / Atlassian auth blocks the backlog pipeline.** Daily cron runs cannot query `project = DS AND status = "In Progress"` without Atlassian MCP or `ATLASSIAN_*` credentials, so generation-gate and heal metrics stay stale and no specs ship.

## Next action

1. Reconnect **Atlassian** MCP for automation `1e8b0ec6-3214-47ed-ad52-fe5e53731673` (and/or bind `ATLASSIAN_EMAIL`, `ATLASSIAN_API_TOKEN`, `ATLASSIAN_BASE_URL`, `JIRA_PROJECT_KEY` plus `DIDAXIS_*` for local Playwright runs).
2. Grant the Cloud Agent integration **`workflow_dispatch`** on `test-generation.yml` as a fallback when MCP auth fails.
3. Move at least one DS ticket to **In Progress** without **`tests-generated`** to validate the full analyze → spec → green → PR → label loop once auth is restored.
