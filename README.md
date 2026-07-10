# Legion QA — Playwright (Didaxis)

End-to-end Playwright suite for [Didaxis Studio](https://test.didaxis.studio), plus Cursor agents/skills for ticket → test generation, triage, and self-heal.

## Prerequisites

- Node.js 20+ (CI uses 22 for E2E)
- Access to a Didaxis environment and an API token

## Install & configure

```bash
git clone <this-repo>
cd legion-qa-ai-assisted-program-ann
npm install
cp .env.example .env
```

Edit `.env` with real values. **Never commit `.env` or put real secrets in `.env.example`.**

### Run tests (required for Playwright)

| Variable | Purpose |
|---|---|
| `DIDAXIS_URL` | App base URL |
| `DIDAXIS_EMAIL` / `DIDAXIS_PASSWORD` | Admin login → `storageState` |
| `DIDAXIS_API_TOKEN` | Bearer token for program API cleanup/seeding |

Optional permission probes: `DIDAXIS_ALT_EMAIL` / `DIDAXIS_ALT_PASSWORD`. Specs currently read `DIDAXIS_NONADMIN_EMAIL` / `DIDAXIS_NONADMIN_PASSWORD` — set those to the same values (see `.env.example`).

### Agent / CI setup (not needed for `npx playwright test`)

| Variable | Purpose |
|---|---|
| `CURSOR_API_KEY` | Headless Cursor agent in `.github/workflows/test-generation.yml` |
| `ATLASSIAN_API_TOKEN` | Jira API (agent workflow + Atlassian MCP) |
| `ATLASSIAN_BASE_URL` | Jira site URL |
| `ATLASSIAN_EMAIL` | Atlassian account for the API token |

MCP tokens for interactive Cursor (GitHub, Atlassian, Playwright) live in **Cursor Settings → MCP**, not in `.env`.

## Run tests

```bash
# Full suite
npm test
# or
npx playwright test

# Headed / UI / debug
npm run test:headed
npm run test:ui
npm run test:debug

# HTML report
npm run report
```

### Tagged slices

Each test has exactly one tag: `@smoke`, `@sanity`, `@regression`, `@api`, `@e2e`, or `@destructive`.

```bash
npm run test:smoke
npm run test:sanity
npm run test:regression
npm run test:api
npm run test:e2e
npm run test:destructive   # --workers=1; shared-state mutations only
```

`@destructive` is only for tests that mutate shared/global state (locale, roles, flags, settings) and must revert in `afterEach`/`afterAll`. Own-data create/cleanup keeps an importance tag.

### CI (`.github/workflows/e2e.yml`)

| Trigger | Suite |
|---|---|
| Pull request | `npm run test:smoke` |
| Push | `npm run test:sanity` |
| Manual (`workflow_dispatch`) | `npm run test:regression` (or choose smoke/sanity) |

Ticket-scoped scripts (DS-1 … DS-5) are also in `package.json` (`npm run test:ds1`, etc.).

## Cursor agents & skills

Project guidance lives under `.cursor/`:

- **Rules** — `constitution.mdc` (always-on non-negotiables), `playwright-conventions.mdc`, `qa-orchestrator.mdc`
- **Agents** — `triage` (red CI), `bug-reporter` (Jira bug), `test-writer` (plan → spec)
- **Skills** — `api-cleanup`, `ci-failure-triage`, `didaxis-program-deleter`, `explore-and-generate`, `exploratory-charter`, `jira-bug-reporter`, `jira-ticket-analyzer`, `pom-conventions`, `eval-report`, `self-heal`
- **Hooks** — `afterFileEdit` guards in `.cursor/hooks.json` block WON'T violations and weakened `expect(` under `tests/**` / `pages/**`

Open the repo in Cursor; rules apply automatically. Invoke agents/skills by name when working tickets, failures, or new coverage.
