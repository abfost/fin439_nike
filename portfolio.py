"""Lab 14 — Meridian portfolio baselines. Standard library only for original output."""
from math import sqrt
from itertools import combinations

# Editable inputs. Returns and volatilities are decimals (0.035 = 3.5%).
SLEEVES = {
    "Treasury bills": {"return": 0.035, "volatility": 0.005},
    "Treasury 10-year note": {"return": 0.043, "volatility": 0.070},
    "Investment-grade bond fund": {"return": 0.050, "volatility": 0.060},
    "Global equity index fund": {"return": 0.080, "volatility": 0.160},
}
CORRELATIONS = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
]
OBJECTIVE_RETURN = 0.065
RESERVE_ELIGIBLE = ("Treasury bills", "Treasury 10-year note")


def validate_correlations(correlations, count):
    """Reject invalid shapes, out-of-range correlations and asymmetry."""
    if len(correlations) != count or any(len(row) != count for row in correlations):
        raise ValueError("Correlation table must be square with one row per sleeve.")
    for i in range(count):
        for j in range(count):
            value = correlations[i][j]
            if not isinstance(value, (int, float)) or not -1 <= value <= 1:
                raise ValueError(f"Invalid correlation [{i+1},{j+1}]: {value}. Must be between -1 and 1.")
            if abs(value - correlations[j][i]) > 1e-10:
                raise ValueError(f"Correlation table is not symmetric at [{i+1},{j+1}].")
        if abs(correlations[i][i] - 1) > 1e-10:
            raise ValueError(f"Correlation diagonal [{i+1},{i+1}] must be 1.")


def covariance_matrix(sleeves, correlations):
    """Covariance(i,j) = correlation(i,j) * volatility(i) * volatility(j)."""
    vol = [s["volatility"] for s in sleeves.values()]
    return [[correlations[i][j] * vol[i] * vol[j] for j in range(len(vol))]
            for i in range(len(vol))]


def benchmark_weights(sleeves):
    weights = {name: 0.0 for name in sleeves}
    weights["Investment-grade bond fund"] = 0.40
    weights["Global equity index fund"] = 0.60
    return weights


def equal_weights(sleeves):
    return {name: 1 / len(sleeves) for name in sleeves}


def inverse_volatility_weights(sleeves):
    inverse = {name: 1 / item["volatility"] for name, item in sleeves.items()}
    total = sum(inverse.values())
    return {name: amount / total for name, amount in inverse.items()}


def expected_return(weights, sleeves):
    return sum(weights[name] * sleeves[name]["return"] for name in sleeves)


def portfolio_volatility(weights, covariance, sleeves):
    names = list(sleeves)
    variance = sum(weights[a] * weights[b] * covariance[i][j]
                   for i, a in enumerate(names) for j, b in enumerate(names))
    return sqrt(max(variance, 0.0))


def reserve_weight(weights):
    return sum(weights[name] for name in RESERVE_ELIGIBLE)


def meets_objective(portfolio_return, target):
    return portfolio_return >= target


def show_portfolio(name, weights, sleeves, covariance):
    result_return = expected_return(weights, sleeves)
    result_volatility = portfolio_volatility(weights, covariance, sleeves)
    print(f"\n{name}")
    for sleeve, weight in weights.items():
        print(f"  {sleeve}: {weight * 100:.1f}%")
    print(f"  Expected return: {result_return * 100:.2f}%")
    print(f"  Volatility: {result_volatility * 100:.2f}%")
    print(f"  Reserve-eligible: {reserve_weight(weights) * 100:.1f}%")
    print(f"  Meets {OBJECTIVE_RETURN * 100:.1f}% objective? {'yes' if meets_objective(result_return, OBJECTIVE_RETURN) else 'no'}")


def search_lowest_risk(sleeves, correlations, objective=0.065,
                       reserve_minimum=0.03, reserve_eligible=RESERVE_ELIGIBLE):
    """Enumerate all nonnegative, fully invested 5-point allocations; return best or None."""
    names = list(sleeves)
    validate_correlations(correlations, len(names))
    covariance = covariance_matrix(sleeves, correlations)
    eligible = set(reserve_eligible)
    best = None

    def allocations(parts, n):
        if n == 1:
            yield (parts,)
            return
        for first in range(parts + 1):
            for remainder in allocations(parts - first, n - 1):
                yield (first,) + remainder

    for counts in allocations(20, len(names)):
        weights = dict(zip(names, (x / 20 for x in counts)))
        ret = expected_return(weights, sleeves)
        reserve = sum(weights[name] for name in eligible if name in weights)
        if ret + 1e-12 < objective or reserve + 1e-12 < reserve_minimum:
            continue
        vol = portfolio_volatility(weights, covariance, sleeves)
        if best is None or vol < best["volatility"] - 1e-12:
            best = {"weights": weights, "return": ret, "volatility": vol, "reserve": reserve}
    return best


def estimate_from_prices(csv_file, last_36=False):
    """Estimate annualized moments from monthly adjusted close prices; optional last 36 returns."""
    import pandas as pd  # Only needed when importing real price data into the app
    df = pd.read_csv(csv_file)
    if df.shape[1] < 2:
        raise ValueError("CSV must contain Date then at least one ticker column.")
    dates = pd.to_datetime(df.iloc[:, 0], errors="raise")
    if dates.isna().any() or not dates.is_monotonic_increasing or dates.duplicated().any():
        raise ValueError("Date must be valid, unique, and oldest first.")
    prices = df.iloc[:, 1:].apply(pd.to_numeric, errors="raise")
    if prices.isna().any().any() or (prices <= 0).any().any():
        raise ValueError("Every price must be positive and present; no missing cells.")
    returns = prices.pct_change().dropna()
    if last_36:
        returns = returns.tail(36)
    if len(returns) < 2:
        raise ValueError("At least 3 months of prices are required.")
    means = returns.mean() * 12
    vols = returns.std(ddof=1) * sqrt(12)
    if (vols <= 0).any():
        raise ValueError("At least one asset has zero estimated volatility; check prices.")
    sleeves = {ticker: {"return": float(means[ticker]), "volatility": float(vols[ticker])}
               for ticker in prices.columns}
    correlations = returns.corr().to_numpy().tolist()
    validate_correlations(correlations, len(sleeves))
    return sleeves, correlations, len(returns)


def main():
    validate_correlations(CORRELATIONS, len(SLEEVES))
    covariance = covariance_matrix(SLEEVES, CORRELATIONS)
    portfolios = {
        "Benchmark": benchmark_weights(SLEEVES),
        "Equal weight": equal_weights(SLEEVES),
        "Inverse volatility": inverse_volatility_weights(SLEEVES),
    }
    for name, weights in portfolios.items():
        show_portfolio(name, weights, SLEEVES, covariance)


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        raise SystemExit(f"INPUT ERROR: {exc}")
