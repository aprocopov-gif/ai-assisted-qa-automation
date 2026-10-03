# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `legion-qa-ai-assisted-program-ann`  
**Window:** `e2e.yml` runs 2026-07-10 → 2026-10-03 (daily backlog-scan runs) + related PRs  
**Generated:** 2026-10-03  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**This refresh trigger:** scheduled **Backlog mode** run (2026-10-03 10:02 UTC / 06:00 EST cron). **0 / 5** tickets processed — Jira queue unreadable (Atlassian MCP `needsAuth`; interactive auth unavailable in Cloud Agent; unauthenticated JQL returns false-empty `issues: []`; prior GH Test Generation runs corroborate **`GET /rest/api/3/myself` → 401** with `dev1` secrets). No specs, ticket PRs, or `tests-generated` labels this run.

---

## Flake rate

| | |
|---|---|
| **Number** | **0** flaky outcomes across sampled `e2e.yml` runs in window (no `flaky` / `passed on retry` in recent green logs). Eval-only PR branches (#35–#39) show **CI failures** on push/PR — DS-2 timeouts and browser-closed errors on auth-blocked scan branches, not recorded suite flakes on `main`. → **0%** suite flake in measured green runs; **insufficient data** for post-2026-07-22 production slices. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 30`; `gh run view 36993590108 --log` grepped for `flaky`, `Retry #`, `passed on retry`. Recent runs tied to `docs(eval)` backlog scans (2026-09-29→2026-10-02) — failures are workflow/env or standing DS-2 instability on eval branches, not retried passes on green `main`. |
| **What it tells us** | Standing suite flake signal remains quiet on green runs; daily auth-blocked scans do not exercise new generation paths. |

---

## Heal success rate

| | |
|---|---|
| **Number** | **Unchanged: 1 / 2 (50%)** — no new locator-heal PRs this window. **Masked-regression count: 0** (required target: **0**). |
| **How measured** | `gh pr list --state all` — no `heal/*` or "Heal:" PRs since the last window; latest heal-related PRs remain [#10](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/10) (first CI failed) / [#11](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/11) (first CI passed). No red generation run this session, so no heal was invoked. |
| **What it tells us** | Metric is stale by design (no drift to repair). Masked-regression discipline holds at 0. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **Unchanged: first-PR CI green 2 / 2 (100%)** ([#7](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/7) DS-4, [#8](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/8) DS-1). **Full gate (green + conforming + maps-to-AC): still incomplete / unknown.** |
| **How measured** | `gh pr list` — no new `test(DS-*)` generation PRs this window (recent PRs #35–#39 are `docs(eval-report)` empty-scan commits). Existing DS-1…DS-5 specs remain the last generation evidence. |
| **What it tells us** | No fresh generation evidence; backlog automation has not produced a ticket PR since auth broke. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **This session (2026-10-03 backlog scan): 0 asks vs 0 invented tickets/AC.** |
| **How measured** | Session review. Queue probe via unauthenticated Jira REST + Atlassian MCP status; automation memory cross-check (prior snapshot: all In Progress tickets already labeled `tests-generated`). Did **not** invent work from local `features/DS-*` (DS-1…DS-5 already have specs). |
| **What it tells us** | Guardrail held: false-empty JQL and missing MCP auth did not trigger speculative test generation. |

---

## Top reliability risk

**Jira API auth blocks the entire backlog pipeline.** Cloud Agent cannot authenticate Atlassian MCP; unauthenticated JQL is a false empty; GitHub `dev1` `ATLASSIAN_API_TOKEN` has returned **401** on `/rest/api/3/myself` in prior Actions runs. Until credentials are fixed, every scheduled run will report 0/5 regardless of real queue depth — a silent operational failure mode worse than a red build.

## Next action

1. **Fix `ATLASSIAN_API_TOKEN`** (and related `ATLASSIAN_*` secrets) in GitHub environment **dev1**; verify with `GET /rest/api/3/myself` → 200 from Actions and authenticate **Atlassian MCP** for Cloud Agent runs.
2. Move at least one DS ticket to **In Progress** without **`tests-generated`** to validate end-to-end generation after auth repair.
3. On the **next real generation or heal PR**, capture first-PR-green + conformance + AC-map in the PR body so generation-gate and heal metrics leave the stale state.
