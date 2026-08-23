"""
KDENCE MVP — Minimum Viable Acquisition Machine
=================================================

The smallest working version of the pipeline:

    PROPERTY DATABASE -> BUY BOX -> PASS/FAIL -> ALERT
    -> UNDERWRITE -> SHADE LINE -> HUMAN REVIEW -> DECISION

Phase 2 (stubbed, not wired to real data yet):

    ACTUALS -> VARIANCE -> FEEDBACK -> MODEL UPDATE

Design rules this file follows on purpose:
  - PROC-001: a listing claim (source="listing") is NEVER treated as a
    verified underwriting input. It has to be tagged source="verified"
    (comps/lease/rent-roll/legal-unit-count) before it can drive a
    DSCR calculation. Where a field is still a listing claim, the
    Shade Line puts the deal on HOLD instead of scoring it as if it
    were real.
  - Screening assumptions (vacancy 5%, opex 10%) are placeholders per
    the Level-1/Level-2/Level-3 assumption system — they make
    screening conservative, not accurate. They never loosen once
    research-derived actuals exist; actuals only refine Level 2/3.
  - The machine does not decide whether to buy. It flags. A human
    makes the final call at the HUMAN REVIEW step.
"""

from dataclasses import dataclass, field
from typing import Literal, Optional


# ---------------------------------------------------------------------------
# LAYER 1 — DATA
# ---------------------------------------------------------------------------

EvidenceSource = Literal["listing", "verified", "assumption"]

# Buy-box tiers (from the Bronx geographic buy box already on file)
PRIMARY_AREAS = {
    "Pelham Bay",
    "Pelham Parkway",
    "Morris Park",
    "Van Nest",
    "Westchester Square",
    "Unionport",
}
SECONDARY_AREAS = {"Fordham", "Belmont", "Kingsbridge", "Norwood"}
WATCHLIST_AREAS = {"Mott Haven", "Port Morris", "Riverdale", "Spuyten Duyvil"}
EXCLUSION_FLAGS = {"distressed_title", "legally_unclear", "speculative_appreciation_only"}


@dataclass
class Property:
    """One deal record with the inputs needed for the acquisition pipeline."""

    deal_id: str
    address: str
    neighborhood: str
    unit_count: int
    purchase_price: float

    # Rent: tagged with its evidence source. "listing" = asking rent from
    # StreetEasy/Zillow — a lead-generation input, not underwriting evidence.
    gross_scheduled_rent_annual: float
    rent_source: EvidenceSource

    # From DOB/certificate of occupancy, not the listing.
    legal_unit_count_verified: bool
    exclusion_flags: set[str] = field(default_factory=set)

    # Financing assumptions (screening-level placeholders unless overridden)
    down_payment_pct: float = 0.25
    interest_rate: float = 0.07
    loan_term_years: int = 30

    # Screening-level opex/vacancy placeholders (Level 1 assumption system)
    vacancy_pct: float = 0.05
    opex_pct: float = 0.10

    # Filled in later by the pipeline
    pipeline_log: list[str] = field(default_factory=list)

    def log(self, stage: str, message: str) -> None:
        self.pipeline_log.append(f"[{stage}] {message}")


# ---------------------------------------------------------------------------
# LAYER 2 — RULES (Buy Box)
# ---------------------------------------------------------------------------


def buy_box_screen(prop: Property) -> bool:
    """PROPERTY DATABASE -> BUY BOX -> PASS/FAIL."""

    if prop.exclusion_flags & EXCLUSION_FLAGS:
        prop.log("BUY BOX", f"FAIL — exclusion flag(s): {prop.exclusion_flags & EXCLUSION_FLAGS}")
        return False

    if prop.unit_count != 3:
        prop.log("BUY BOX", f"FAIL — unit count {prop.unit_count} is outside the 3-family buy box")
        return False

    if prop.neighborhood in PRIMARY_AREAS:
        prop.log("BUY BOX", f"PASS — {prop.neighborhood} is a primary target area")
        return True
    if prop.neighborhood in SECONDARY_AREAS:
        prop.log("BUY BOX", f"PASS — {prop.neighborhood} is a secondary opportunity zone")
        return True
    if prop.neighborhood in WATCHLIST_AREAS:
        prop.log("BUY BOX", f"FAIL — {prop.neighborhood} is watchlist-only, not primary buy box")
        return False

    prop.log("BUY BOX", f"FAIL — {prop.neighborhood} is outside the defined geographic buy box")
    return False


# ---------------------------------------------------------------------------
# LAYER 3 — WORKFLOW (Alert)
# ---------------------------------------------------------------------------


def alert(prop: Property) -> None:
    """BUY BOX PASS -> ALERT. In v0.1 this prints a notification hook."""

    msg = f"ALERT: {prop.deal_id} ({prop.address}) matched the buy box — routing to underwriting."
    prop.log("ALERT", msg)
    print(msg)


# ---------------------------------------------------------------------------
# UNDERWRITING (DSCR Calculator v0.1)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class UnderwritingResult:
    effective_gross_income: float
    operating_expenses: float
    noi: float
    annual_debt_service: float
    dscr: float
    cash_required_to_close: float
    annual_cash_flow: float
    cash_on_cash_return: float


def underwrite(prop: Property, vacancy_pct: Optional[float] = None, opex_pct: Optional[float] = None) -> UnderwritingResult:
    """Calculate screening-level underwriting metrics.

    Uses the screening-level vacancy/opex placeholders unless Level 2 or
    Level 3 verified data overrides them. The optional vacancy_pct / opex_pct
    arguments let stress tests reuse the same deterministic formulas.
    """

    vacancy = prop.vacancy_pct if vacancy_pct is None else vacancy_pct
    opex_rate = prop.opex_pct if opex_pct is None else opex_pct

    egi = prop.gross_scheduled_rent_annual * (1 - vacancy)
    opex = egi * opex_rate
    noi = egi - opex

    down_payment = prop.purchase_price * prop.down_payment_pct
    loan_amount = prop.purchase_price - down_payment

    monthly_rate = prop.interest_rate / 12
    n_payments = prop.loan_term_years * 12
    if monthly_rate > 0:
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** n_payments) / (
            (1 + monthly_rate) ** n_payments - 1
        )
    else:
        monthly_payment = loan_amount / n_payments
    annual_debt_service = monthly_payment * 12

    dscr = noi / annual_debt_service if annual_debt_service else 0
    annual_cash_flow = noi - annual_debt_service
    cash_required_to_close = down_payment  # closing costs omitted in v0.1, per the calculator spec
    coc_return = annual_cash_flow / cash_required_to_close if cash_required_to_close else 0

    result = UnderwritingResult(
        effective_gross_income=egi,
        operating_expenses=opex,
        noi=noi,
        annual_debt_service=annual_debt_service,
        dscr=dscr,
        cash_required_to_close=cash_required_to_close,
        annual_cash_flow=annual_cash_flow,
        cash_on_cash_return=coc_return,
    )

    prop.log("UNDERWRITE", f"NOI=${noi:,.0f}  DSCR={dscr:.2f}  CoC={coc_return:.1%}")
    return result


# ---------------------------------------------------------------------------
# RISK STRESS TESTING
# ---------------------------------------------------------------------------

STRESS_SCENARIOS = {
    "base": {"vacancy_delta": 0.00, "opex_delta": 0.00},
    "stress": {"vacancy_delta": 0.00, "opex_delta": 0.10},
    "downside": {"vacancy_delta": 0.10, "opex_delta": 0.15},
    "severe": {"vacancy_delta": 0.20, "opex_delta": 0.25},
}


def run_stress_tests(prop: Property) -> dict[str, UnderwritingResult]:
    """Run BASE / STRESS / DOWNSIDE / SEVERE vacancy and opex shocks."""

    results = {}
    for name, shock in STRESS_SCENARIOS.items():
        vacancy = min(prop.vacancy_pct + shock["vacancy_delta"], 0.95)
        opex_pct = prop.opex_pct + shock["opex_delta"]
        results[name] = underwrite(prop, vacancy_pct=vacancy, opex_pct=opex_pct)

    summary = "  ".join(f"{name}={r.dscr:.2f}" for name, r in results.items())
    prop.log("STRESS TEST", f"DSCR by scenario — {summary}")
    return results


# ---------------------------------------------------------------------------
# SHADE LINE ENGINE v0.1
# ---------------------------------------------------------------------------

ShadeLineFlag = Literal["REJECT", "HOLD", "PASS"]


def shade_line(
    prop: Property,
    uw: UnderwritingResult,
    stress_results: dict[str, UnderwritingResult],
    dscr_min: float = 1.25,
    downside_dscr_min: float = 1.00,
) -> tuple[ShadeLineFlag, str]:
    """Evaluate explicit, traceable policy gates before human review."""

    if uw.dscr < dscr_min:
        reason = f"DSCR {uw.dscr:.2f} is below the policy minimum of {dscr_min:.2f}"
        prop.log("SHADE LINE", f"REJECT — {reason}")
        return "REJECT", reason

    downside_dscr = stress_results["downside"].dscr
    if downside_dscr < downside_dscr_min:
        reason = (
            f"base DSCR {uw.dscr:.2f} passes, but downside DSCR {downside_dscr:.2f} "
            f"falls below the {downside_dscr_min:.2f} floor (vacancy +10pp, expenses +15%)"
        )
        prop.log("SHADE LINE", f"REJECT — {reason}")
        return "REJECT", reason

    if not prop.legal_unit_count_verified:
        reason = "legal unit count is unverified (DOB/certificate of occupancy not yet checked)"
        prop.log("SHADE LINE", f"HOLD — {reason}")
        return "HOLD", reason

    if prop.rent_source == "listing":
        reason = "rent assumption is an unverified listing claim (PROC-001: needs comps/lease/rent-roll to convert to a verified input)"
        prop.log("SHADE LINE", f"HOLD — {reason}")
        return "HOLD", reason

    reason = f"DSCR {uw.dscr:.2f} clears the {dscr_min:.2f} minimum, unit count and rent are verified"
    prop.log("SHADE LINE", f"PASS — {reason}")
    return "PASS", reason


# ---------------------------------------------------------------------------
# HUMAN REVIEW -> DECISION
# ---------------------------------------------------------------------------


def human_review(
    prop: Property,
    uw: UnderwritingResult,
    stress_results: dict[str, UnderwritingResult],
    shade_flag: ShadeLineFlag,
    shade_reason: str,
) -> str:
    """Print a decision packet and return a placeholder human-review state."""

    print("\n" + "=" * 70)
    print(f"HUMAN REVIEW PACKET — {prop.deal_id} — {prop.address}")
    print("=" * 70)
    print(f"Neighborhood:        {prop.neighborhood}")
    print(f"Purchase price:      ${prop.purchase_price:,.0f}")
    print(f"Gross rent (annual): ${prop.gross_scheduled_rent_annual:,.0f}  (source: {prop.rent_source})")
    print(f"NOI:                 ${uw.noi:,.0f}")
    print(f"DSCR (base):         {uw.dscr:.2f}")
    print("DSCR by scenario:    " + "  ".join(f"{name}={r.dscr:.2f}" for name, r in stress_results.items()))
    print(f"Cash-on-cash:        {uw.cash_on_cash_return:.1%}")
    print(f"Shade Line flag:     {shade_flag} — {shade_reason}")
    print("-" * 70)
    for entry in prop.pipeline_log:
        print(entry)
    print("=" * 70)

    if shade_flag == "REJECT":
        decision = "REJECT"
    elif shade_flag == "HOLD":
        decision = "WATCH — pending evidence verification"
    else:
        # A PASS still requires a human decision, not an automatic buy.
        decision = "PENDING HUMAN DECISION (BUY / WATCH / REJECT)"

    prop.log("HUMAN REVIEW", f"Decision: {decision}")
    return decision


# ---------------------------------------------------------------------------
# THE MINIMUM VIABLE MACHINE — runs one property through the full pipeline
# ---------------------------------------------------------------------------


def run_pipeline(prop: Property) -> Optional[str]:
    print(f"\n>>> Running {prop.deal_id} ({prop.address}) through KDENCE...")

    if not buy_box_screen(prop):
        print(f"    Result: FAIL at buy box — not proceeding. ({prop.pipeline_log[-1]})")
        return None

    alert(prop)
    uw = underwrite(prop)
    stress_results = run_stress_tests(prop)
    shade_flag, shade_reason = shade_line(prop, uw, stress_results)
    decision = human_review(prop, uw, stress_results, shade_flag, shade_reason)
    return decision


# ---------------------------------------------------------------------------
# PHASE 2 STUB — ACTUALS -> VARIANCE -> FEEDBACK -> MODEL UPDATE
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ActualsRecord:
    deal_id: str
    period: str
    actual_noi: float


def record_variance(uw: UnderwritingResult, actuals: ActualsRecord) -> dict[str, float | str]:
    """Compare underwritten NOI to actual NOI for future feedback review."""

    underwritten_noi = uw.noi
    variance_pct = (actuals.actual_noi - underwritten_noi) / underwritten_noi if underwritten_noi else 0
    return {
        "deal_id": actuals.deal_id,
        "period": actuals.period,
        "underwritten_noi": underwritten_noi,
        "actual_noi": actuals.actual_noi,
        "variance_pct": variance_pct,
    }


# ---------------------------------------------------------------------------
# DEMO — sample property database
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sample_properties = [
        Property(
            deal_id="DEAL-0001",
            address="123 Sample St",
            neighborhood="Morris Park",
            unit_count=3,
            purchase_price=750_000,
            gross_scheduled_rent_annual=72_000,
            rent_source="verified",
            legal_unit_count_verified=True,
        ),
        Property(
            deal_id="DEAL-0002",
            address="456 Listing Ave",
            neighborhood="Pelham Bay",
            unit_count=3,
            purchase_price=800_000,
            gross_scheduled_rent_annual=84_000,
            rent_source="listing",
            legal_unit_count_verified=True,
        ),
        Property(
            deal_id="DEAL-0003",
            address="789 Overleveraged Blvd",
            neighborhood="Fordham",
            unit_count=3,
            purchase_price=950_000,
            gross_scheduled_rent_annual=60_000,
            rent_source="verified",
            legal_unit_count_verified=True,
        ),
        Property(
            deal_id="DEAL-0004",
            address="1 Watchlist Way",
            neighborhood="Riverdale",
            unit_count=3,
            purchase_price=700_000,
            gross_scheduled_rent_annual=70_000,
            rent_source="verified",
            legal_unit_count_verified=True,
        ),
        Property(
            deal_id="DEAL-0005",
            address="55 Thin Margin Ter",
            neighborhood="Van Nest",
            unit_count=3,
            purchase_price=780_000,
            gross_scheduled_rent_annual=71_500,
            rent_source="verified",
            legal_unit_count_verified=True,
        ),
    ]

    decisions = {}
    for p in sample_properties:
        decisions[p.deal_id] = run_pipeline(p)

    print("\n" + "#" * 70)
    print("PIPELINE SUMMARY")
    print("#" * 70)
    for deal_id, decision in decisions.items():
        print(f"{deal_id}: {decision}")
