# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `ai-assisted-qa-automation`  
**Window:** `e2e.yml` runs 2026-07-10 → 2026-07-22 (14 daily backlog-scan runs) + related PRs, plus local DS-4 re-verify  
**Generated:** 2026-11-16  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**This refresh trigger:** Scheduled **Cursor Automation** backlog batch (`1e8b0ec6-3214-47ed-ad52-fe5e53731673`, cron 06:00 EST weekdays). **0 / 5** tickets processed — Jira queue unreachable (Atlassian MCP `needsAuth`; no `ATLASSIAN_*` / `DIDAXIS_*` in Cloud Agent env; unauthenticated Jira REST returned `issues: []`).

**Prior refresh context:** single-ticket Done for **DS-4** (user-requested `run DS-4`, 2026-07-22 window below).

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

## Automation backlog scan (2026-11-16)

| | |
|---|---|
| **Queue JQL** | `project = DS AND status = "In Progress" AND (labels is EMPTY OR labels not in (tests-generated)) ORDER BY priority ASC, key ASC` |
| **Tickets processed** | **0 / 5** (budget unused) |
| **Blockers** | Atlassian MCP requires desktop IDE OAuth (`mcp_auth` unavailable here); `ATLASSIAN_*` / `DIDAXIS_*` not in VM env; `gh workflow run test-generation.yml` → **403**; unauthenticated POST `/rest/api/3/search/jql` → HTTP 200 with `issues: []` (untrusted empty). |
| **Ask-vs-guess (this run)** | **0 invented** ticket keys, AC, or credentials; did not assume queue is empty. |
| **Agent run** | https://cursor.com/agents/bc-c89182ec-5afc-475c-adea-a093e989b3ed |

Historical snapshot (2026-07-30, authenticated CI): all **In Progress** DS tickets already carried `tests-generated`; work queues when a ticket is moved to **In Progress** without that label.

---

## Top reliability risk

**Backlog orchestration blocked by Jira integration auth.** Eight consecutive daily scans (2026-11-11 → 2026-11-16) processed **0** tickets for the same reason. Until Atlassian MCP is connected for automation `1e8b0ec6-3214-47ed-ad52-fe5e53731673` (or Jira/Didaxis secrets are on the Cloud Agent / `test-generation.yml` can be dispatched), generation-gate and heal metrics stay stale and the In Progress queue cannot be trusted.

Secondary: **E2E CI on doc-scan PRs** still fails early (`Playwright does not support chromium on ubuntu26.04-x64` per recent runs) — does not block backlog enumeration but hides smoke signal on scan branches.

## Next action

1. **Reconnect Atlassian MCP** for this automation in Cursor **Integrations** (same team as the bot), then re-run the cron or move a DS ticket to **In Progress** without `tests-generated` to validate end-to-end.
2. Optionally add **`ATLASSIAN_*` + `DIDAXIS_*`** to the linked Cloud Agent environment, or grant the integration token **`workflow_dispatch`** on `test-generation.yml` (currently **403**).
3. On the **next real generation or heal PR**, capture first-PR-green + conformance + AC-map in the PR body.
4. Fix or pin CI runner image so `e2e.yml` is meaningful on automation doc PRs.
