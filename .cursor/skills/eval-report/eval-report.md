# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `legion-qa-ai-assisted-program-ann`  
**Window:** `e2e.yml` runs 2026-07-10 → 2026-07-22 (14 daily backlog-scan runs) + related PRs, plus local DS-4 re-verify  
**Generated:** 2026-07-22  

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
| **How measured** | `gh pr list --state all` — no `heal/*` or "Heal:" PRs since the last window; latest heal-related PRs remain [#10](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/10) (first CI failed) / [#11](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/11) (first CI passed). No red run this session, so no heal was invoked. |
| **What it tells us** | Metric is stale by design (no drift to repair). Masked-regression discipline holds at 0. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **Unchanged: first-PR CI green 2 / 2 (100%)** ([#7](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/7) DS-4, [#8](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/8) DS-1). **Full gate (green + conforming + maps-to-AC): still incomplete / unknown.** |
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

**Stale heal / full-generation-gate instrumentation.** The prior top risk (retries masking DS-4/DS-2 flakes) did **not** recur in this window and is downgraded. The dominant gap now is that recent CI is entirely daily **empty-backlog doc scans** — no new heal or ticket-generation PRs — so heal success (1/2) and the full generation gate (green + conforming + maps-to-AC) are unrefreshed and cannot be scored on fresh evidence.

## Next action

1. On the **next real generation or heal PR**, capture first-PR-green + conformance + AC-map in the PR body so the generation-gate and heal metrics leave the stale state.
2. Keep watching **DS-4 TC-004/TC-017** and **DS-2 TC-002** on PR/push slices to confirm the flake regression is durable (2+ more windows at 0).
3. When a heal is needed, use branch `heal/<spec-slug>` and prove green with **assertions unchanged** to keep heal success rate measurable under the orchestrator path.
