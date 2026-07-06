---
name: self-heal
description: Repairs drifted Playwright locators after a UI change — patch the POM, re-run, open a PR. Use when the build is red because a locator broke, fix the drifted selector, the test broke after a UI change, or heal the suite. Use ONLY after ci-failure-triage classifies the red run as a test issue (drift); never for a real app bug — route those to jira-bug-reporter instead.
---

# Self-Heal (Locator Drift)

Repairs drifted Playwright locators: patch the POM, re-run, open a PR.

## Gate (required before any edit)

**Do not start without triage's drift classification.**

1. Run [ci-failure-triage](../ci-failure-triage/SKILL.md) first (or confirm an existing triage comment on the PR).
2. Triage must classify the failure as **test issue / drift** (stale selector, renamed label, moved element — not wrong app behavior).
3. If classification is **real app bug**, **missing**, or **ambiguous** → **stop**. Route to [jira-bug-reporter](../jira-bug-reporter/SKILL.md) via the `bug-reporter` agent.

Collect from triage: root cause, failing test, trace path, affected POM file, failed run id or URL.

## Workflow

### 1. Record triage inputs

Copy into working notes: failing test name, run id, classification `drift`, affected POM file.

### 2. Find the failing locator from the trace

From the Playwright trace / error output:

- Identify the **exact locator expression** that timed out or resolved to zero elements.
- Map it to the **POM property or method** in `pages/` (see [pom-conventions](../pom-conventions/SKILL.md)).
- Note the element's **intended role** and **accessible name** from the trace context.

### 3. Re-discover the element via Playwright MCP

Use the Playwright MCP against the live app (`DIDAXIS_URL`, default `https://test.didaxis.studio`):

1. `browser_navigate` to the page/state where the element appears (replay triage steps or use `storageState` from `tests/auth.setup.ts`).
2. `browser_snapshot` — read the **accessibility tree**.
3. Find the target by **role + current accessible name** (dialog scope when inside a modal).
4. If hidden, interact only enough to reveal it (open modal, select row, scroll), then snapshot again.
5. Derive the **new locator**: `getByRole` → `getByLabel` → `getByText` → `getByTestId`. Never CSS/XPath.

The new locator must match the **same semantic intent** as the old one (same role; name updated to what the UI shows now).

If the element is missing from the a11y tree and app behavior is wrong → stop; re-triage as app bug (Gate step 3).

### 4. Patch the POM (minimal diff)

- Edit **only** the locator in the POM file from step 2.
- Update role/name/scope to match the live a11y tree; follow [pom-conventions](../pom-conventions/SKILL.md).
- Do **not** edit spec files, assertions, waits, or test logic.
- Do **not** broaden locators to force a pass (e.g. dropping `exact: true`, switching to CSS, matching a less specific ancestor).
- Fix **one** locator per run — pick the root cause triage identified.

### 5. Re-run and prove green

```bash
npx playwright test <failing-spec> --reporter=line
```

**Pass criteria (all required):**

- [ ] Targeted spec passes.
- [ ] **Zero** changes under `tests/**/*.spec.ts` — assertions identical, not weakened, removed, or replaced with vaguer checks.
- [ ] Only POM locator lines changed (plus imports if a POM moved).

If the run is still red:
- **Same locator error** → reconsider the a11y discovery; do not weaken assertions.
- **Different failure / app behavior wrong** → stop healing; re-triage. Likely
  real app bug → `bug-reporter`.
- **Green only after touching assertions** → **escalate**; revert assertion edits.

### 6. Report and open PR

Post a structured summary (PR comment or PR body):

```markdown
## Self-heal: locator drift

**Run:** <CI run id / trace link>
**Test:** `<spec>` → `<test title>`
**Classification:** drift (from triage)

### Locator diff
| Location | Before | After |
|----------|--------|-------|
| `pages/...` `propertyName` | `page.getByRole(...)` | `page.getByRole(...)` |

### Verification
- Re-run: `npx playwright test <spec>` — **green**
- Spec files: **no changes**
```

Open one PR: branch `heal/<ticket-or-spec-slug>-<short-desc>`, title `heal: update <element> locator after UI drift`, link failed CI run and triage comment.

## Rules

- **One repair per run** — do not batch unrelated locator fixes.
- **Every heal becomes a PR** — never commit directly to main; never merge automatically.
- **Never heal app bugs** — wrong behavior, missing features, API errors belong in jira-bug-reporter.
- **Never weaken assertions** — a green run via assertion changes is a failure; escalate.
- If the same locator breaks again after heal, stop and escalate — likely not simple drift.

## Related skills

- [ci-failure-triage](../ci-failure-triage/SKILL.md) — required gate; supplies drift classification
- [jira-bug-reporter](../jira-bug-reporter/SKILL.md) — route when not drift
- [pom-conventions](../pom-conventions/SKILL.md) — locator style and file layout
