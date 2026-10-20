"""FIN 43900 Lab 13: Meridian Foundation mandate checker.

All values are editable below. Only Python standard library is used.
"""

RESERVE_SIZE_MILLIONS = 100.0
QUARTERLY_DISTRIBUTION_MILLIONS = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_DAYS = 5
MIN_LIQUID_SHARE = 90.0
ISSUER_LIMIT = 8.0

# Holding: (issuer, days to redeem, eligible for distribution reserve)
HOLDINGS = {
    "Cash": (None, 0, True),
    "Treasury bills": ("U.S. Treasury", 1, True),
    "Treasury 10-year note": ("U.S. Treasury", 1, True),
    "Global equity index fund": ("diversified fund", 2, False),
    "Investment-grade bond fund": ("diversified fund", 3, False),
    "Private real estate fund": ("diversified fund", 90, False),
    "Acme Corp bonds": ("Acme Corp", 4, False),
    "Acme Corp stock": ("Acme Corp", 1, False),
}

CANDIDATES = {
    "A": {
        "Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
        "Global equity index fund": 60, "Investment-grade bond fund": 26,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 55, "Investment-grade bond fund": 20,
        "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
        "Global equity index fund": 70, "Investment-grade bond fund": 20,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8,
    },
    "D": {
        "Cash": 3, "Treasury bills": 97, "Treasury 10-year note": 0,
        "Global equity index fund": 0, "Investment-grade bond fund": 0,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    "E": {
        "Cash": 0, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 60, "Investment-grade bond fund": 40,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
}

EXEMPT_ISSUERS = {None, "U.S. Treasury", "diversified fund"}


def evaluate(name, portfolio, reserve_minimum):
    if set(portfolio) != set(HOLDINGS):
        missing = set(HOLDINGS) - set(portfolio)
        extra = set(portfolio) - set(HOLDINGS)
        raise ValueError(f"Candidate {name}: holdings mismatch; missing={missing}, extra={extra}")

    total = sum(portfolio.values())
    lowest = min(portfolio.values())
    reserve = sum(weight for holding, weight in portfolio.items() if HOLDINGS[holding][2])
    liquid = sum(weight for holding, weight in portfolio.items()
                 if HOLDINGS[holding][1] <= LIQUIDITY_WINDOW_DAYS)

    company_totals = {}
    for holding, weight in portfolio.items():
        issuer = HOLDINGS[holding][0]
        if issuer not in EXEMPT_ISSUERS:
            company_totals[issuer] = company_totals.get(issuer, 0) + weight
    largest_company = max(company_totals.values(), default=0)

    checks = [
        ("Weights sum to 100%", total, abs(total - 100.0) < 1e-9),
        ("Long-only (lowest weight >= 0%)", lowest, lowest >= 0),
        (f"Reserve-eligible (>= {reserve_minimum:.1f}%)", reserve, reserve >= reserve_minimum),
        (f"Redeemable within {LIQUIDITY_WINDOW_DAYS} business days (>= {MIN_LIQUID_SHARE:.1f}%)", liquid, liquid >= MIN_LIQUID_SHARE),
        (f"Largest single company (<= {ISSUER_LIMIT:.1f}%)", largest_company, largest_company <= ISSUER_LIMIT),
    ]
    print(f"\nCandidate {name}")
    for label, value, passed in checks:
        print(f"  {label}: {value:.1f}% {'pass' if passed else 'FAIL'}")
    print("  Calendar-year loss: requires CIO clarification")
    failures = sum(not passed for _, _, passed in checks)
    print("  Verdict: " + ("passes every checkable rule" if failures == 0
                           else f"fails {failures} rule(s)"))


def main():
    reserve_minimum = (QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION_MILLIONS
                       / RESERVE_SIZE_MILLIONS * 100)
    print(f"Reserve minimum: {reserve_minimum:.1f}% of portfolio")
    for name, portfolio in CANDIDATES.items():
        evaluate(name, portfolio, reserve_minimum)


if __name__ == "__main__":
    main()
