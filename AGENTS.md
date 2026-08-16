# KDENCE HOUSE — Engineering Constitution

## Mission

Build a secure, explainable internal operating system for KDENCE HOUSE. V1 is the Deal Desk: property intake, underwriting, stress testing, decisioning, and deal history.

## Non-negotiable principles

1. **Correctness over cleverness.** Financial calculations must be deterministic and testable.
2. **Explainability.** Never hide a material assumption or calculation behind opaque logic.
3. **No silent assumptions.** Missing inputs must be explicit; do not invent values.
4. **Conservative by default.** Downside cases matter as much as base cases.
5. **Separate policy from code.** Investment thresholds and rules must be centralized and easy to change.
6. **Security first.** Never commit secrets, credentials, PII, financial-account data, or confidential documents.
7. **Small increments.** Prefer small, reviewable changes over giant rewrites.
8. **Tests are required.** Financial formulas and decision rules require automated tests before release.
9. **Traceability.** Preserve the inputs, assumptions, scenario, calculations, and resulting decision.
10. **No premature complexity.** Do not add microservices, event buses, AI agents, or unnecessary infrastructure until a real requirement exists.

## V1 decision model

The system may calculate and recommend a status, but it must show the reasons. A recommendation is not a substitute for human approval.

Initial statuses:

- BUY — passes all required policy gates under the selected decision scenario.
- WATCH — potentially viable but one or more gates require resolution or improved terms.
- PASS — fails a hard policy gate or presents unacceptable risk under the decision policy.

Thresholds must be configurable rather than hard-coded throughout the application.

## Financial calculation rules

- Store source inputs separately from calculated outputs.
- Preserve precision internally; round only for presentation.
- Clearly distinguish monthly, annual, and one-time figures.
- Never mix operating expenses, debt service, CapEx, and acquisition costs without labeling them.
- Every metric must have a documented formula and test coverage.

## Data model expectations

Core entities should remain modular:

- Deal
- Property
- Unit / Rent Roll
- Operating Assumption
- Financing Assumption
- Underwriting Scenario
- Calculation Result
- Stress Test
- Decision
- Decision Rationale
- Document metadata

## V1 implementation guidance

Start with a modular monolith. A practical stack is:

- TypeScript
- Next.js for the web application
- PostgreSQL for persistent data
- Prisma or an equivalent typed ORM
- Vitest for unit tests
- Playwright for critical end-to-end flows

If the implementation environment provides a stronger existing convention, follow the environment rather than introducing unnecessary tooling.

## Delivery order

1. Repository scaffolding and CI
2. Database schema
3. Domain calculation library
4. Underwriting API/service
5. Deal Desk UI
6. Stress testing
7. Decision engine
8. Authentication and authorization
9. Audit/decision history
10. Deployment and operational hardening

## Definition of done

A feature is not done merely because it renders. It must have:

- documented behavior
- validation
- tests for important paths
- sensible error handling
- no secrets committed
- clear user-facing labels
- reproducible calculations

## Codex behavior

Before changing architecture, inspect the repository and existing conventions. Prefer the smallest change that satisfies the requirement. Run relevant tests after implementation. Report what changed, what was tested, and any unresolved risk.
