# Suite reliability report

**Suite:** Legion QA Playwright (Didaxis Studio)  
**Repo:** `legion-qa-ai-assisted-program-ann`  
**Window:** last **30** `e2e.yml` runs + related PRs (through 2026-07-26)  
**Generated:** 2026-07-26  

**Note:** Cursor has **no built-in telemetry** for these metrics. Every number below was measured from CI logs (`gh`), PR history, and session review. Refresh via the `eval-report` skill — do not invent numbers; use `insufficient data` when evidence is missing.

**2026-07-26 backlog batch:** Queue empty — Jira REST (unauthenticated) returned `issues: []` for eligible JQL; Atlassian MCP `needsAuth`; GH Test Generation [30157235398](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/30157235398) (2026-07-25) authenticated scan confirmed **10 In Progress, all `tests-generated`**. Metrics below refreshed for the current 30-run E2E window; heal/generation denominators unchanged (no new heal or generation PRs since 2026-07-09).

---

## Flake rate

| | |
|---|---|
| **Number** | **0** flaky test outcomes in **30** passing E2E runs → **0/30 runs (0%)** in the current window. Prior window (through 2026-07-09) had **3/27 runs (11%)** with flaky markers. |
| **How measured** | `gh run list --workflow=e2e.yml --limit 30`, then `gh run view <id> --log` grepped for `flaky`, `Retry #`, `passed on retry`. CI uses `retries: 2` (`playwright.config.ts`). All 30 runs in the current window are eval-scan PR/push runs (2026-07-09–2026-07-24); none reported flaky. Auth-setup `Retry #` on failed runs = hard fails, not flakes. Cleanup 404s treated as noise. |
| **What it tells us** | Recent CI window is stable; historical DS-2/DS-4 flake candidates are not surfacing in the eval-scan slice but may still exist under full regression. |

---

## Heal success rate

| | |
|---|---|
| **Number** | **Clean heals: 1 / 2 (50%)** in the locator-repair window (unchanged). **Masked-regression count: 0** (required target: **0**). |
| **How measured** | PR history (`gh pr list`, `gh pr checks`, `gh pr diff`): [#10](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/10) (first CI failed) vs [#11](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/11) (first CI passed). No new `heal/*` PRs since 2026-07-09. |
| **What it tells us** | Heal discipline holds at 0 masked regressions; no new heal events to measure since last refresh. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **First-PR CI green: 2 / 2 (100%)** for ticket-shaped generation PRs ([#7](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/7) DS-4, [#8](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/8) DS-1). **Full gate (green + conforming + maps-to-AC): incomplete / unknown** — not re-audited against Jira AC this refresh. No new generation PRs since 2026-06-22. |
| **How measured** | `gh pr list` for `test(DS-*)` titles; `gh pr checks` on first PR; `gh run list --workflow=test-generation.yml --limit 10`. Scheduled runs [30157235398](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/30157235398)–[30006711837](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/30006711837) report empty eligible queue. |
| **What it tells us** | Generation pipeline idle — all In Progress tickets already labeled; gate pass rate denominator unchanged. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **This session (2026-07-26): ~0 asks vs 0 invented product values**. Used Jira REST + GH Test Generation logs for queue corroboration instead of guessing ticket state. **Prior Block-15 sample: ~2 asks vs ~5 invented defaults** (ask:guess ≈ 0.4). |
| **How measured** | Manual session review of agent transcripts + PR bodies (Cursor has no ask/guess telemetry). This run: no AC/locator/credential invention; Atlassian MCP auth gap documented rather than bypassed. |
| **What it tells us** | Empty-queue runs should corroborate via authenticated GH workflow logs when MCP auth is unavailable. |

---

## Top reliability risk

**Backlog starvation** — no eligible In Progress tickets without `tests-generated`; generation and flake/heal metrics cannot improve until new work enters the queue. Secondary: historical DS-2/DS-4 flakes may reappear under full `@regression` runs not exercised by eval-scan PRs.

## Next action

1. **Queue work:** Move a DS ticket to **In Progress** without `tests-generated`, or remove that label to re-run generation.
2. **Authenticate Atlassian MCP** in Cursor desktop so Cloud Agent runs can label tickets after PR open.
3. When the queue has tickets, run full generation-gate checklist (green + conventions + AC map) on the first PR per ticket.
