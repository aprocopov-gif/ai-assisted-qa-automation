# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `ai-assisted-qa-automation`  
**Window:** `e2e.yml` runs 2026-07-10 → 2026-09-30 (daily backlog-scan runs) + related PRs  
**Generated:** 2026-09-30  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**This refresh trigger:** scheduled **Backlog mode** run (2026-09-30 10:00 UTC / 06:00 EST cron). **0 / 5** tickets processed — Jira queue unreadable (Atlassian MCP `needsAuth`; unauthenticated JQL returns false-empty `issues: []`; GH Test Generation [36464990412](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/36464990412) corroborates **`GET /rest/api/3/myself` → 401** with `dev1` secrets). No specs, ticket PRs, or `tests-generated` labels this run.

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
| **Number** | **This session (2026-09-30 backlog scan): 0 asks vs 0 invented tickets/AC.** |
| **How measured** | Session review. Queue probe via unauthenticated Jira REST + Atlassian MCP status; corroboration via `gh run view 36464990412 --log`. Did **not** invent work from local `features/DS-*` (DS-1…DS-5 already have specs). |
| **What it tells us** | Guardrail held: false-empty JQL and missing MCP auth did not trigger speculative test generation. |

---

## Top reliability risk

**Jira API auth blocks the entire backlog pipeline.** Cloud Agent cannot authenticate Atlassian MCP; unauthenticated JQL is a false empty; GitHub `dev1` `ATLASSIAN_API_TOKEN` returns **401** on `/rest/api/3/myself`. Until credentials are fixed, every scheduled run will report 0/5 regardless of real queue depth — a silent operational failure mode worse than a red build.

## Next action

1. **Fix `ATLASSIAN_API_TOKEN`** (and related `ATLASSIAN_*` secrets) in GitHub environment **dev1**; verify with `GET /rest/api/3/myself` → 200 from Actions and authenticate **Atlassian MCP** for Cloud Agent runs.
2. Move at least one DS ticket to **In Progress** without **`tests-generated`** to validate end-to-end generation after auth repair.
3. On the **next real generation or heal PR**, capture first-PR-green + conformance + AC-map in the PR body so generation-gate and heal metrics leave the stale state.
