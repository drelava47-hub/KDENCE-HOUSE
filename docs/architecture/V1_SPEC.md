# KDENCE HOUSE Operations — V1 Technical Specification

## 1. Product objective

Build the first useful slice of KDENCE HOUSE Operations: a Deal Desk that converts a property opportunity into a transparent underwriting decision.

Primary workflow:

1. Create a deal.
2. Enter property, income, expense, acquisition, and financing assumptions.
3. Calculate operating and financing metrics.
4. Run downside scenarios.
5. Evaluate policy gates.
6. Produce BUY / WATCH / PASS with reasons.
7. Save the scenario and decision history.

## 2. V1 user experience

### Dashboard

Show:

- active deals
- deal status
- purchase price
- NOI
- DSCR
- required cash
- decision
- key alerts

### Deal Desk

Sections:

- Identity: address, property type, units, source, notes
- Acquisition: asking price, offer price, closing costs, initial CapEx
- Income: unit rents, other income, vacancy/collection assumption
- Operating expenses: taxes, insurance, utilities, repairs, maintenance, management, other OpEx
- Financing: loan amount or LTV, interest rate, amortization, term, lender fees
- Reserves: required operating and capital reserves
- Scenario: base / downside / custom
- Results: NOI, debt service, DSCR, cash required, cash-on-cash, break-even occupancy, cap rate
- Decision: BUY / WATCH / PASS and rationale

### Scenario comparison

Allow the user to compare base case against downside cases without overwriting source assumptions.

## 3. Domain model

### Deal

- id
- name
- propertyId
- status
- source
- notes
- createdAt
- updatedAt

### Property

- id
- addressLine1
- addressLine2
- city
- state
- postalCode
- propertyType
- unitCount

### IncomeAssumption

- dealId
- annualGrossScheduledRent
- otherAnnualIncome
- vacancyRate
- collectionLossRate

### ExpenseAssumption

- dealId
- propertyTaxesAnnual
- insuranceAnnual
- utilitiesAnnual
- repairsAnnual
- maintenanceAnnual
- managementAnnual
- otherOperatingExpensesAnnual

### AcquisitionAssumption

- dealId
- purchasePrice
- closingCosts
- initialCapEx
- otherAcquisitionCosts

### FinancingAssumption

- dealId
- loanAmount
- interestRateAnnual
- amortizationYears
- lenderFees

### ReserveAssumption

- dealId
- operatingReserve
- capitalReserve

### UnderwritingScenario

- id
- dealId
- name
- rentMultiplier
- vacancyRate
- expenseMultiplier
- interestRateAnnual
- additionalAnnualCapEx
- notes

### UnderwritingResult

- scenarioId
- grossScheduledIncome
- effectiveGrossIncome
- operatingExpenses
- noi
- annualDebtService
- dscr
- cashRequired
- annualCashFlowAfterDebt
- cashOnCashReturn
- capRate
- breakEvenOccupancy
- maximumPurchasePrice

### Decision

- id
- dealId
- scenarioId
- status
- reasons
- assumptionsSnapshot
- decidedAt
- approvedBy

## 4. Calculation definitions

Use annual figures unless explicitly labeled otherwise.

### Effective Gross Income

EGI = Gross Scheduled Rent + Other Income − Vacancy/Collection Loss

### Operating Expenses

OpEx = Taxes + Insurance + Utilities + Repairs + Maintenance + Management + Other OpEx

### NOI

NOI = EGI − OpEx

NOI excludes acquisition costs, financing costs, debt service, and income taxes.

### Annual debt service

For a fully amortizing fixed-rate loan, calculate principal and interest using the standard mortgage payment formula. Support interest-only financing only as an explicitly selected financing type; do not infer it.

### DSCR

DSCR = NOI / Annual Debt Service

### Cash required

Cash Required = Down Payment + Closing Costs + Initial CapEx + Lender Fees + Required Reserves + Other Acquisition Costs

If loan amount is entered directly, down payment = Purchase Price − Loan Amount. If LTV is used, derive loan amount from purchase price × LTV.

### Cash flow after debt

Annual Cash Flow After Debt = NOI − Annual Debt Service − recurring non-operating cash costs explicitly included by policy.

### Cash-on-cash return

Cash-on-Cash = Annual Cash Flow After Debt / Cash Required

### Cap rate

Cap Rate = NOI / Purchase Price

### Break-even occupancy

Break-even occupancy must be calculated from the modeled revenue and fixed/variable operating assumptions. Document the exact formula in the calculation library and test it with known cases.

### Maximum purchase price

The maximum price should be solved from the selected policy constraints rather than guessed. At minimum, support a DSCR-constrained maximum price based on projected NOI and financing assumptions. Additional constraints can be added later.

## 5. Stress-test library

V1 should include these scenario templates:

### Base

User's stated assumptions.

### Rate shock

Increase interest rate by a configurable number of percentage points.

### Rent stress

Reduce effective rent/income by a configurable percentage.

### Vacancy stress

Increase vacancy/collection loss to a configurable rate.

### Expense stress

Increase operating expenses by a configurable percentage.

### Combined downside

Apply multiple shocks together.

Do not hard-code permanent economic forecasts. Scenario parameters must be stored with the scenario.

## 6. Decision engine

The decision engine evaluates explicit policy gates.

Suggested V1 gate categories:

1. DSCR minimum
2. Reserve sufficiency
3. Maximum leverage / LTV
4. Cash requirement within available acquisition capital
5. Downside survivability
6. Data completeness

The exact numeric thresholds should live in a policy configuration object and be editable without rewriting calculation formulas.

Output example:

- status: WATCH
- reasons:
  - Base DSCR passes.
  - Combined downside DSCR falls below policy minimum.
  - Required reserves are incomplete.
- unresolvedItems:
  - confirm insurance quote
  - obtain verified rent roll

The engine must not present a recommendation as guaranteed financial advice.

## 7. API/service boundaries

Keep domain calculations independent from the web UI.

Suggested service boundaries:

- deals: CRUD and lifecycle
- underwriting: calculate scenario
- stress-tests: generate scenario variants
- decisions: evaluate policy gates
- audit: store calculation/decision snapshots

The frontend should call application services rather than duplicate financial formulas.

## 8. Validation

Reject or flag:

- negative purchase price
- negative rents or expenses where not explicitly allowed
- interest rates below zero unless a future policy explicitly permits them
- impossible loan amounts
- amortization periods <= 0
- vacancy rates outside 0–100%
- missing required property identity
- incomplete financing assumptions when debt metrics are requested

## 9. Testing strategy

Unit tests must cover:

- EGI
- OpEx
- NOI
- mortgage payment / debt service
- DSCR
- cash required
- cash-on-cash return
- cap rate
- break-even occupancy
- maximum purchase price
- each stress scenario
- each decision gate
- combined decision outcomes

Include edge cases and at least one manually verified fixture per major formula.

End-to-end tests must cover:

1. create a deal
2. enter assumptions
3. calculate underwriting
4. run downside scenario
5. save decision
6. reopen deal and see identical saved result

## 10. Security and privacy

The repository is public. No production secrets or private operational data may be committed.

Before production use, implement authentication, authorization, encrypted transport, secure secret management, database access controls, audit logging, and appropriate backup/recovery.

## 11. V1 non-goals

Do NOT build yet:

- tenant portal
- rent collection
- maintenance dispatch
- lender integrations
- automated MLS scraping
- bank integrations
- AI deal sourcing
- multi-company accounting
- mobile native application
- microservice infrastructure

Those are future modules. V1 exists to prove the underwriting core.

## 12. Definition of V1 success

A user can enter a real acquisition opportunity, reproduce the underwriting numbers, stress it, see exactly which policy gates pass/fail, save the decision, and return later without losing the assumptions or rationale.
