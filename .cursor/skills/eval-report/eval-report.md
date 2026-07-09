# Reliability eval report

**Suite:** Legion QA Playwright (Didaxis)  
**Window:** last **15** `e2e.yml` runs + related PRs (through 2026-07-06)  
**Generated:** 2026-07-08  
**Note:** Cursor has **no built-in telemetry** for flake, heal, generation-gate, or ask-vs-guess. Every number below was measured from CI logs, PR history, and session review.

---

## Flake rate

| | |
|---|---|
| **Number** | **1** flaky test outcome in last **15** E2E runs → **~0.7%** of completed tests in the only run that reported flaky (`1 flaky` / `143 passed + 1 flaky` in [run 28762948379](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/actions/runs/28762948379)); **1/15** runs showed any flaky result |
| **How measured** | `gh run list --workflow=e2e.yml --limit 15`, then `gh run view <id> --log` grepped for `Retry #`, `flaky`. Playwright CI uses `retries: 2`. The only pass-on-retry was `tests/ds4-delete-program.spec.ts` → **TC-004: Deleted program name can be reused** (timeout on `locator.click`, then passed). Several other runs showed `Retry #` on **auth.setup** but those **failed** after retries (not flake — hard fail). |
| **What it tells us** | Suite is mostly stable under retries, but DS-4 TC-004 is a real flake candidate — retries are masking a timing/locator race, not fixing it. |

---

## Heal success rate

| | |
|---|---|
| **Number** | **Clean heals: 1 / 2 (50%)** in the recent locator-repair window. **Masked-regression count: 0** (required target: **0**). |
| **How measured** | PR history (`gh pr list`): [#10](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/10) (POM locator update — merged, then **main E2E failed** on auth/`getByTitle`/`getByAltText` drift) vs [#11](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/11) (self-heal skill + **restored** role/label locators — E2E **SUCCESS**). “Clean” = green after heal with assertions unchanged. “Masked regression” = heal that weakened/deleted assertions or papered over a triage-classified **app bug** — none found in PR diffs/bodies for #10/#11. No formal `heal/*` repair PRs yet under the post-skill orchestrator path. |
| **What it tells us** | Locator heals without triage + accessibility-tree rediscovery can land **wrong** selectors and break main; the constitution/self-heal gate exists for a reason. Masked-regression discipline is holding at 0 so far. |

---

## Generation-gate pass rate

| | |
|---|---|
| **Number** | **First-PR CI green: 2 / 2 (100%)** for ticket-shaped generation PRs in history. **Full gate (green + conforming + maps-to-AC): not fully evidenced** → treat as **incomplete / unknown**, not 100%. |
| **How measured** | PRs titled like generated specs: [#7](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/7) `test(DS-4)…`, [#8](https://github.com/aprocopov-gif/legion-qa-ai-assisted-program-ann/pull/8) `test(DS-1)…` — each **1 commit**, `Playwright E2E` **SUCCESS** on the PR. Neither carries the `tests-generated` label. Conformance to `playwright-conventions.mdc` and AC mapping were **not** re-audited against Jira in this eval (would need ticket AC + spec review). Scheduled `test-generation.yml` runs are **workflow-green** but do not prove a generated-spec gate by themselves. |
| **What it tells us** | Early generated specs can land green on first PR, but without a recorded conforming+AC checklist the generation gate is only half-instrumented. |

---

## Ask-vs-guess

| | |
|---|---|
| **Number** | **This framework session (sample): ~2 clarifying asks vs ~5 invented defaults** (ask:guess ≈ **0.4**). Broader suite history: **not measurable** from git alone. |
| **How measured** | Manual session review of this branch’s agent work (no Cursor telemetry). Examples of **asking / confirming** were rare; examples of **inventing** include: hyphenated branch name, `DIDAXIS_NONADMIN_*` aliases beside `ALT_*`, `@high→@smoke` / `@medium→@sanity` / `@low→@regression` mapping without confirmation, and optional workflow_dispatch suite choices. |
| **What it tells us** | Agents still default to guessing when a value is under-specified — fine for format, risky for credentials, tag semantics, and product intent. Prefer one explicit ask over a silent default when the wrong choice is expensive. |

---

## Top reliability risk

**Retries + untriaged locator patches** — DS-4 TC-004 already passes only on retry, and PR #10 showed a “heal” can ship bad locators and red `main`. Together they hide instability until a merge or a flaky-green CI run.

## Next action

1. **Stabilize DS-4 TC-004** (fix the click/timeout race; do not raise timeouts as the fix).  
2. Keep this eval mandatory after every orchestrator backlog batch / heal cycle / generation PR (see `qa-orchestrator.mdc` → **Reliability eval**).  
3. On the next generated-spec PR, record an explicit **generation-gate** checklist (green + conventions + AC map) in the PR body so the third metric becomes a real rate, not “unknown.”
