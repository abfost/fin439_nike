# Lab 13 — Portfolio Mandate Defense

## Part 1: S1–S10 Classification

| Statement | Category | Explanation |
|---|---|---|
| S1 | Hard Constraint | The seven-year horizon identifies the investment period, while annual rebalancing establishes how frequently the portfolio should be adjusted. |
| S2 | Objective | CPI plus 4% after costs over rolling five-year periods describes the return that the foundation wants to achieve. |
| S3 | Hard Constraint | The foundation needs sufficient cash or daily-liquid government securities to cover twelve months of quarterly distributions. |
| S4 | Preference | The 60% global equity and 40% U.S. investment-grade bond benchmark provides a standard for evaluating investment performance. |
| S5 | Hard Constraint | The foundation prohibits borrowing, short selling, and derivatives. |
| S6 | Hard Constraint | No single company can represent more than 8% of the total portfolio. |
| S7 | Hard Constraint | Annual turnover is limited to 25% unless the committee gives its approval. |
| S8 | Hard Constraint | At least 90% of the portfolio must be redeemable within five business days. |
| S9 | Unverifiable Promise | The 10% annual loss statement does not specify how losses are measured or what happens if the limit is breached. |
| S10 | Missing | The CIO has not specified what the pilot portfolio should optimize. Although no sector, ESG, tax, or home-bias preferences were identified, the optimization objective remains missing. |

## Part 2: Portfolio Checker Results

The Meridian Foundation manages a $100 million portfolio and distributes $0.75 million quarterly. The minimum reserve requirement is calculated as (4 × $0.75 million) / $100 million = 3.0%.

Portfolio A passes all five checkable rules. Its weights total 100%, its minimum weight is 0%, its reserve-eligible assets are 14%, its five-day liquidity is 100%, and its largest single-company exposure is 0%.

Portfolio B fails three rules. Its reserve-eligible assets are only 1%, its five-day liquidity is 85%, and its largest single-company exposure is 9%, which exceeds the 8% limit.

Portfolio C fails one rule because its reserve-eligible assets total only 2%, which is below the required 3%. All its other checkable rules pass.

The calendar-year loss restriction in S9 requires clarification from the CIO and cannot be reliably tested as written.

Verified: I ran `mandate.py` and observed A pass, B fail three rules, and C fail one rule.

## Part 3: Negative Weight Test

To test the checker, I temporarily changed Portfolio A's cash allocation from 2% to -2% and its global equity index fund allocation from 60% to 64%.

Actual test result:
I ran the modified Python checker and confirmed that Portfolio A failed exactly one rule: the long-only constraint. Its minimum weight was -2%, while its reserve-eligible assets remained at 10%. All other checkable rules passed. I then restored the original portfolio allocations.

## Part 4: Portfolio D

| Holding | Allocation |
|---|---:|
| Cash | 3% |
| Treasury bills | 97% |
| **Total** | **100%** |

I created Portfolio D with 3% cash and 97% Treasury Bills.
However, investing almost entirely in Treasury bills may make it difficult to achieve the foundation's long-term return objective of CPI plus 4% after costs. A portfolio can satisfy all numerical restrictions while still being unsuitable for a client's long-term goals.

Actual checker result:
Portfolio D passed all five checkable rules. Its weights total 100%, its minimum weight is 0%, its reserve-eligible assets are 100%, its five-day liquidity is 100% and its largest restricted single-company exposure is 0%.

My two-sentence judgment:
 The CIO could reject Portfolio D because investing almost entirely in Treasury Bills may not provide enough growth to achieve the foundation's CPI plus 4% return objective. This relates to S2, which establishes the foundation's return objective.

## Part 5: Question for the CIO

My question:
What should the portfolio's primary optimization objective be: maximizing expected returns or minimizing risk while pursuing the foundation's return target?

Design consequence:
If the CIO prioritizes maximizing expected returns, I would consider allocating more to global equities. If the CIO prioritizes reducing risk, I would consider increasing investment-grade bonds and Treasury securities, while still respecting the hard constraints.

## Part 6: Investment Policy Statement
An investment policy statement (IPS) is a document that establishes a client's investment objectives, constraints, preferences, and guidelines. It helps ensure that investment decisions are consistent with the client's financial needs.

For the Meridian Foundation, S1 establishes the seven-year investment horizon and annual rebalancing schedule. S2 identifies the CPI + 4% return objective. S3 establishes the requirement to maintain twelve months of distributions in eligible reserves. S4 provides the 60% global equity and 40% investment-grade bond benchmark.

S5 prohibits borrowing, short selling, and derivatives. S6 limits exposure to a single company to 8%. S7 restricts annual turnover to 25% without committee approval. S8 requires at least 90% of the portfolio to be redeemable within five business days.

S9 requires clarification because the calendar-year loss restriction does not specify how losses are measured or handled. S10 identifies missing information about what the portfolio should optimize.

The IPS is important because it creates a consistent framework for investment decisions and helps determine whether a portfolio is appropriate for the foundation.

## Part 7: Reflection

A portfolio can pass every rule programmed into the checker and still be found unsuitable for the client because the checker only evaluates specific measurable restrictions. It cannot determine whether a portfolio is likely to achieve return objectives or whether its overall investment strategy is appropriate.

The classification I found most difficult:
I found S9 to be the most difficult because the statement initially sounds like a hard constraint. However, guaranteeing that a portfolio will never lose more than 10% in a calendar year is unrealistic because market performance cannot be completely controlled. I classified it as an unverifiable promise because the statement does not clearly define how losses are measured or what happens if the limit is exceeded.

## Part 8: Project 2 Mandate

Client:
A fictional individual investor saving for retirement.

Investment objective:
The client wants to grow their investment portfolio over the next 20 years while maintaining a diversified investment strategy. The goal is to accumulate enough wealth to help support retirement expenses.

Hard constraints:
The portfolio must be long-only, cannot use borrowing, and cannot allocate more than 8% to one company. At least 5% must remain in cash or short-term liquid investments.

Question for the client:
 How much short-term investment loss are you comfortable accepting in exchange for the possibility of higher long-term growth?
