# KDENCE HOUSE Operations

KDENCE HOUSE Operations is the internal operating system for the KDENCE HOUSE investment and property operations platform.

## V1 Mission

Turn a property opportunity into a disciplined investment decision:

**Property → Underwrite → Stress Test → Decision → Save**

## Architecture

The system is designed around a 3 → 1 → ∞ model:

- **3 — Inputs:** capital, assets, intelligence
- **1 — Control System:** doctrine, data, decisions, governance, execution
- **∞ — Compounding:** repeatable acquisition, operations, learning, and scale

## V1: Deal Desk

The first release focuses on acquisition underwriting. It will capture a property, calculate operating economics and financing metrics, run downside scenarios, and produce a transparent BUY / WATCH / PASS decision.

### Core capabilities

- Property and deal intake
- Rent and operating assumptions
- NOI calculation
- Debt service and DSCR
- Cash required and reserve analysis
- Cash-on-cash return
- Break-even occupancy
- Interest-rate, rent, vacancy, expense, and CapEx stress tests
- Maximum purchase price analysis
- Decision rationale and assumptions
- Persistent deal history

## Development

### Prerequisites

- Node.js 20.9 or newer
- npm

### Local setup

```bash
git clone <repository-url>
cd KDENCE-HOUSE
npm install
cp .env.example .env.local
npm run dev
```

Open `http://localhost:3000` to verify the application starts. The Phase 1 home page intentionally contains only a minimal runtime proof.

### Verification commands

```bash
npm run lint
npm run format:check
npm test
npm run build
npm run test:e2e
```

`npm run test:e2e` starts the Next.js development server automatically and runs the Playwright smoke test against the home page.

### Environment variables

Phase 1 validates `APP_ENV` when provided. Supported values are `development`, `test`, and `production`. It defaults to `development` when omitted. No secret values are required for the application skeleton.

Keep local environment files out of version control. Only `.env.example` belongs in the repository.

## Development principle

The application must be explainable. Every important decision should preserve the inputs, assumptions, formulas, thresholds, scenario, decision, and rationale that produced it.

## Security

No secrets, credentials, tenant PII, bank information, or confidential property documents belong in this public repository. Sensitive operational data must be stored in appropriately secured infrastructure.

## Status

Phase 1 application skeleton is implemented. Business/domain features remain intentionally unimplemented until Phase 2 is authorized. See `AGENTS.md`, `docs/architecture/V1_SPEC.md`, and `docs/architecture/BUILD_PLAN.md` for engineering rules and implementation scope.
