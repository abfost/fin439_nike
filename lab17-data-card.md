# Lab 17 — PAYEMS Point-in-Time Audit

## Data card

**Series:** PAYEMS — All Employees, Total Nonfarm.

**Source:** U.S. Bureau of Labor Statistics, distributed through [FRED](https://fred.stlouisfed.org/series/PAYEMS) and [ALFRED](https://alfred.stlouisfed.org/series?seid=PAYEMS), Federal Reserve Bank of St. Louis.

**Measure:** Nonfarm payroll employment in the United States, from the Current Employment Statistics establishment survey.

**Units:** Thousands of persons, seasonally adjusted; monthly. For example, 159,536 represents approximately 159.536 million payroll jobs.

**Publication lag:** Data for an observation month become available in the following month. The exact release date must be checked before using the series in a trading decision. A date such as December 1 labels the December observation; it does not mean the value was available on December 1.

**Revisions:** PAYEMS is revised. Historical ALFRED snapshots must be compared with current FRED data to identify the values available at a past decision date.

**Download date:** October 29, 2026, at 2:10:52 p.m. Eastern. This timestamp refers to the verification download used for this card.

## Known-answer check

Live ALFRED downloads for October 5, 2026 matched the lab:

| Series | Last observation known then | Value |
|---|---|---:|
| BAA | September 2026 | 6.47 |
| FEDFUNDS | September 2026 | 3.75 |
| DGS10 | October 2, 2026 | 5.28 |
| MORTGAGE30US | October 1, 2026 | 7.28 |

## PAYEMS revision probe

Using January 15, 2025 as the historical snapshot:

| Evidence | Result |
|---|---:|
| Last observation available then | December 2024 |
| December 2024 value known then | 159,536 |
| December 2024 value in the October 29, 2026 download | 158,316 |
| Revision: current minus historical | −1,220 |
| Current observations after the last date known then | 21 |
| Revised dates present in both downloads | 381 |

The December 2024 estimate decreased by 1.220 million payroll jobs between these snapshots. The revision count covers the full downloaded history, independently of the chart start date.

## Last-month comparison

On September 30, 2026, the latest available observation was August 2026, with a value of 159,075.

In the October 29 download, the latest observation was September 2026, at 159,044. Comparing these snapshots produced one later observation and two revised shared dates. This shows both publication delay and revisions.

## Three-value source check

The current FRED CSV values were compared with the [FRED PAYEMS data table](https://fred.stlouisfed.org/data/PAYEMS) on October 29, 2026. All three matched. This check was completed with AI assistance rather than as a personal by-hand check.

| Observation month | Downloaded value | FRED data-table value | Result |
|---|---:|---:|---|
| October 2024 | 157,945 | 157,945 | Match |
| November 2024 | 158,079 | 158,079 | Match |
| December 2024 | 158,316 | 158,316 | Match |

## How the app works

The app downloads current observations from FRED and a historical snapshot from ALFRED. The historical request includes the selected vintage date, which prevents it from substituting today’s revised history for what was available then.

Missing values are excluded rather than filled. The app compares matching observation dates to count revisions and counts current observations after the last observation available in the historical snapshot.

The combined chart compares six interest rates. PAYEMS has its own chart because its units are thousands of jobs rather than percentages. Individual comparison charts show today’s history alongside the historical snapshot.

## Fresh eyes — Partner feedback

**Partner’s challenge — publication timing:** “Does the January 15 snapshot establish the first day the December payroll number could have been used?”

**My response:** No—the snapshot establishes that the number was available by January 15, but does not establish its first release date or time. Before using PAYEMS in Project 2, I would verify publication timing and use the vintage available before each trading decision.

**Question about the code:** “What prevents the historical download function from returning today’s revised values?”

**My answer:** The `download_asof` function requests data from ALFRED with a `vintage_date` parameter matching the selected “As known on” date. It retrieves that historical snapshot instead of substituting the current FRED download.

## My call — Quarantine

I would quarantine PAYEMS until Project 2 retrieves the historical vintage available at each decision date and respects publication timing. The change in December 2024 from 159,536 to 158,316 shows why today’s history cannot stand in for information available in January 2025.

I would admit the series once the backtest applies that availability rule consistently and verifies release timing. A fixed lag applied to today’s revised data would not resolve the revision problem.

## Reflection

PAYEMS has both publication delay and revision risk. The observation month alone does not establish when a value became usable.

A backtest using today’s history would overstate the information available to the strategy at the time. This could distort signals and measured performance, although it would not necessarily increase every performance measure.

“Cleaned the data” is not a data card because it does not explain the measure, units, source, publication timing, or revision history.
