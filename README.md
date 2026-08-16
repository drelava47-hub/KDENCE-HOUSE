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

## Development principle

The application must be explainable. Every important decision should preserve the inputs, assumptions, formulas, thresholds, scenario, decision, and rationale that produced it.

## Security

No secrets, credentials, tenant PII, bank information, or confidential property documents belong in this public repository. Sensitive operational data must be stored in appropriately secured infrastructure.

## Status

V1 architecture and implementation are being established. See `AGENTS.md` for engineering rules and `docs/architecture/V1_SPEC.md` for the implementation specification.
