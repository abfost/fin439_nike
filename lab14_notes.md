# FIN 43900 — Lab 14: Portfolio Baselines

## Portfolio Results

| Portfolio | Expected Return | Volatility | Reserve-Eligible | Meets 6.5% Objective? |
|---|---|---|---|---|
| Benchmark | 6.80% | 10.46% | 0.0% | Yes |
| Equal Weight | 5.20% | 5.21% | 50.0% | No |
| Inverse Volatility | 3.77% | 1.05% | 90.3% | No |

## Correlation Tests

Changing the correlation between investment-grade bonds and global equity from 0.25 to 0.50 increased the benchmark's volatility from 10.46% to 11.00%.

When I changed the correlation to 1.3, the program correctly rejected the input because correlations must be between -1 and 1.

## Candidate E — Mandate Check

Candidate E allocates 40% to investment-grade bonds and 60% to global equities. It meets the 6.5% return objective but fails Meridian's reserve requirement because it has 0% reserve-eligible assets instead of the required 3%.

## Diversification

Diversification means spreading investments across different assets rather than putting everything into one investment. It reduces risk when those assets do not move together perfectly. When correlation is below +1, losses or fluctuations in one asset may be partly offset by movements in another.

### Benchmark Volatility Calculation

The benchmark portfolio contains 40% investment-grade bonds and 60% global equity.

- Bond volatility = 6% (0.06)
- Equity volatility = 16% (0.16)
- Correlation = 0.25

Portfolio variance = (0.40² × 0.06²) + (0.60² × 0.16²) + (2 × 0.40 × 0.60 × 0.06 × 0.16 × 0.25)

Portfolio variance = 0.000576 + 0.009216 + 0.001152 = 0.010944

Portfolio volatility = √0.010944 ≈ 0.1046 = **10.46%**

Because the correlation is below +1, combining the two investments reduces volatility compared with assets moving perfectly together.

## Reflection

**1. Why does inverse volatility put so much weight into Treasury bills?**

The inverse-volatility portfolio puts most of its weight into Treasury bills because they have the lowest volatility. Since the formula gives more weight to investments with less risk, Treasury bills make up 84.3% of the portfolio.

**2. Which baseline would I show the CIO first, and why?**

I would show the CIO the benchmark portfolio first because its expected return of 6.80% exceeds the 6.5% objective. However, the portfolio fails the 3% reserve requirement. I would explain that even though the benchmark meets the return objective, it is not suitable for Meridian without adjustments to satisfy the mandate.

## Before Thursday — Fund Universe

| Ticker | Fund Name | Role |
|---|---|---|
| BIL | SPDR Bloomberg 1–3 Month T-Bill ETF | Cash and reserve |
| IEF | iShares 7–10 Year Treasury Bond ETF | Government bonds |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Fixed income |
| VT | Vanguard Total World Stock ETF | Global equities |

**Historical price source:** Yahoo Finance (monthly adjusted closing prices).

**Download date:** Not yet downloaded.

## Code Explanation

The portfolio volatility function calculates the overall risk of a portfolio.

First, it uses each investment's portfolio weight to determine how much that investment contributes to risk. Next, it combines the investments' volatilities and correlations to calculate portfolio variance. Finally, it takes the square root of the variance to calculate portfolio volatility.

Correlation matters because investments do not always move in the same direction. A lower correlation can reduce overall portfolio volatility.

The program also checks that correlations are between -1 and 1 and that the correlation matrix is symmetric. If either condition is violated, it refuses to run.

## AI Code Quiz

Question: Why does the portfolio volatility calculation take the square root of variance?

My answer: Taking the square root converts variance into standard deviation, which measures portfolio volatility.

Result: Correct (1/1).

## Partner Activities

My partner and I explained diversification and discussed how portfolio weights, volatilities, and correlations affect overall portfolio risk. We each explained the volatility calculation and answered a question about the code.

We exchanged our `portfolio.py` files and checked the three baseline results. We also tested an invalid correlation of 1.3 to verify that the program rejected the input.

Finally, we discussed why inverse volatility concentrates in Treasury bills and which portfolio we would present to Meridian's CIO.