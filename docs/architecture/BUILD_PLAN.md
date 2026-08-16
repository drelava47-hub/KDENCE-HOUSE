# KDENCE HOUSE Operations — Build Plan

## Phase 0 — Foundation

- [x] Create repository README
- [x] Establish engineering constitution in `AGENTS.md`
- [x] Establish V1 technical specification

## Phase 1 — Application skeleton

- [ ] Initialize TypeScript / Next.js application
- [ ] Add linting and formatting
- [ ] Add unit-test runner
- [ ] Add end-to-end test runner
- [ ] Add CI workflow
- [ ] Add environment-variable validation

## Phase 2 — Domain engine

- [ ] Implement typed domain models
- [ ] Implement income calculations
- [ ] Implement expense calculations
- [ ] Implement NOI
- [ ] Implement mortgage/debt-service calculations
- [ ] Implement DSCR
- [ ] Implement cash-required calculation
- [ ] Implement cash-on-cash return
- [ ] Implement cap rate
- [ ] Implement break-even occupancy
- [ ] Implement maximum purchase price solver
- [ ] Add comprehensive financial unit tests

## Phase 3 — Persistence

- [ ] Add PostgreSQL connection
- [ ] Add ORM/schema
- [ ] Add migrations
- [ ] Persist deals and assumptions
- [ ] Persist scenarios and results
- [ ] Persist decisions and rationale

## Phase 4 — Deal Desk UI

- [ ] Dashboard
- [ ] Deal creation
- [ ] Deal editing
- [ ] Underwriting input form
- [ ] Results panel
- [ ] Scenario comparison
- [ ] Decision panel
- [ ] Deal history

## Phase 5 — Security

- [ ] Authentication
- [ ] Authorization
- [ ] Secure secret management
- [ ] Audit trail
- [ ] Backup/recovery plan

## Phase 6 — Deployment

- [ ] Production environment
- [ ] Database provisioning
- [ ] CI/CD
- [ ] Monitoring and error reporting
- [ ] Smoke tests

## Phase 7 — Expansion

Only after V1 is stable:

- acquisition pipeline
- capital command center
- property operations
- portfolio intelligence
- document intelligence
- workflow automation

## First Codex assignment

Implement **Phase 1 only**. Do not build business features yet.

Acceptance criteria:

1. The application starts locally.
2. TypeScript compiles cleanly.
3. Linting runs cleanly.
4. Unit tests run.
5. End-to-end test harness runs against a basic home page.
6. CI runs the same checks.
7. README documents local setup.
8. No secrets are committed.

After Phase 1 is complete, stop and report the files changed, commands run, test results, and any assumptions. Do not proceed automatically to Phase 2.
