---
name: exploratory-charter
description: >-
  Turns a feature + a risk into a short exploratory charter and a findings
  template. Use when the user asks for an exploratory charter, session charter,
  ET charter, risk-based exploration, or a findings log for a feature — not for
  writing Playwright specs or Gherkin (those are jira-ticket-analyzer /
  test-writer).
---

# Exploratory charter

Keep the **format**. The human does the thinking (what to probe, what matters).
Do not invent deep test design, do not write Playwright, and do not expand into
a full test plan unless asked.

## Inputs

Ask only if missing:

1. **Feature** — what is under exploration (page, flow, ticket, or area)
2. **Risk** — what could go wrong / why this session exists

Optional (fill blanks if given): time box, environment, build/branch, explorer.

## Procedure

1. Fill the **Charter** template from the feature + risk.
2. Hand back an empty **Findings** template for the session log.
3. Stop. Do not run the exploration unless the user asks.

## Charter template

```markdown
# Charter: <short title>

| Field | Value |
|---|---|
| Feature | <feature> |
| Risk focus | <risk> |
| Mission | Explore <feature> to learn whether <risk> shows up in practice |
| Time box | <e.g. 45–60 min> |
| Environment | <URL / build / branch> |
| Out of scope | <what this session will not chase> |
| Notes / setup | <accounts, data, flags — if any> |
```

## Findings template

```markdown
# Findings: <same title>

| # | Area / step | Observation | Severity (bug / question / idea / ok) | Evidence | Follow-up |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |

## Session debrief
- Covered:
- Not covered / time ran out:
- Bugs to file:
- Questions for product/dev:
```

## Example

**Input:** feature = Program create modal; risk = duplicate names silently overwrite or confuse the list.

**Charter (filled):**

```markdown
# Charter: Program create — duplicate names

| Field | Value |
|---|---|
| Feature | Program create modal |
| Risk focus | Duplicate names silently overwrite or confuse the list |
| Mission | Explore Program create modal to learn whether duplicate names silently overwrite or confuse the list |
| Time box | 45 min |
| Environment | DIDAXIS_URL (dev) |
| Out of scope | Edit/delete flows, AI generation config |
| Notes / setup | Admin storageState; unique prefix for any creates |
```

Then return the blank Findings template for the explorer to fill during/after the session.
