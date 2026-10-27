from datetime import date

# Editable decision date
DECISION_DATE = "2026-03-31"

# Editable training table:
# row number, ticker, month measured, publication date, index
TABLE = [
    (1, "AAA", "2026-01", "2026-02-10", 101.0),
    (2, "AAA", "2026-02", "2026-03-10", 104.0),
    (3, "AAA", "2026-03", "2026-04-10", 109.0),
    (4, "AAA", "2026-02", "2026-03-25", 103.0),
    (5, "BBB", "2026-01", "2026-02-10", 98.0),
    (6, "BBB", "2026-02", "2026-03-10", 97.0),
    (7, "BBB", "2026-02", "2026-03-10", 97.0),
    (8, "BBB", "2026-03", "2026-04-10", 92.0),
    (9, "CCC", "2026-01", "2026-02-10", 110.0),
    (10, "CCC", "2026-02", "2026-04-05", 112.0),
    (11, "", "2026-02", "2026-03-10", 99.0),
    (12, "CCC", "2026-02", "2026-03-10", 111.0),
]


def print_removed(label, rows):
    """Print the number and row numbers removed at a funnel step."""
    row_numbers = [row[0] for row in rows]
    print(f"{label}: {len(rows)} removed; rows {row_numbers}")


def remove_missing_tickers(rows):
    kept = []
    removed = []

    for row in rows:
        if not row[1].strip():
            removed.append(row)
        else:
            kept.append(row)

    return kept, removed


def remove_duplicates(rows):
    kept = []
    removed = []
    seen = set()

    for row in rows:
        # Ignore the row number when identifying an exact duplicate.
        data = row[1:]
        if data in seen:
            removed.append(row)
        else:
            seen.add(data)
            kept.append(row)

    return kept, removed


def keep_latest_publications(rows):
    """Keep the latest publication for each ticker and month."""
    latest = {}
    removed = []

    for row in rows:
        key = (row[1], row[2])

        if key not in latest:
            latest[key] = row
        elif row[3] > latest[key][3]:
            removed.append(latest[key])
            latest[key] = row
        else:
            removed.append(row)

    return list(latest.values()), removed


def calculate_signals(rows):
    """Calculate change from the preceding calendar month."""
    by_ticker = {}

    for row in rows:
        ticker = row[1]
        by_ticker.setdefault(ticker, []).append(row)

    signals = {}

    for ticker, ticker_rows in sorted(by_ticker.items()):
        ticker_rows.sort(key=lambda row: row[2])
        latest = ticker_rows[-1]

        year, month = map(int, latest[2].split("-"))
        if month == 1:
            previous_month = f"{year - 1}-12"
        else:
            previous_month = f"{year}-{month - 1:02d}"

        previous = next(
            (row for row in ticker_rows if row[2] == previous_month),
            None,
        )

        if previous is None or previous[4] == 0:
            signals[ticker] = (latest[2], None)
        else:
            change = (latest[4] - previous[4]) / previous[4] * 100
            signals[ticker] = (latest[2], change)

    return signals


def format_signal(signal):
    if signal is None:
        return "No data"

    month, change = signal
    if change is None:
        return f"Unavailable ({month}; previous month missing or zero)"

    return f"{change:+.2f}% ({month})"


def main():
    decision_date = date.fromisoformat(DECISION_DATE)

    print(f"Decision date: {decision_date}")
    print(f"Starting rows: {len(TABLE)}")
    print("\nROW FUNNEL")

    # Rule 1: quarantine rows without a ticker.
    valid_rows, missing = remove_missing_tickers(TABLE)
    print_removed("No ticker", missing)

    # Rule 2: remove exact duplicates.
    unique_rows, duplicates = remove_duplicates(valid_rows)
    print_removed("Exact duplicate", duplicates)

    # Rule 3: remove publications after the decision date.
    available_rows = []
    future_rows = []

    for row in unique_rows:
        if date.fromisoformat(row[3]) > decision_date:
            future_rows.append(row)
        else:
            available_rows.append(row)

    print_removed("Published after decision date", future_rows)

    # Rule 4: keep the latest available revision for each ticker and month.
    asof_panel, old_revisions = keep_latest_publications(available_rows)
    print_removed("Older publication replaced", old_revisions)

    asof_panel.sort(key=lambda row: (row[1], row[2]))
    print(f"As-of panel: {len(asof_panel)} rows; "
          f"rows {[row[0] for row in asof_panel]}")

    print("\nAS-OF PANEL")
    print("Row  Ticker  Month    Published   Index")
    for row in asof_panel:
        print(f"{row[0]:<4} {row[1]:<7} {row[2]:<8} "
              f"{row[3]:<11} {row[4]:.1f}")

    # The naive panel uses the latest publication, even if it came later.
    naive_panel, _ = keep_latest_publications(unique_rows)

    asof_signals = calculate_signals(asof_panel)
    naive_signals = calculate_signals(naive_panel)

    print("\nSIGNALS")
    print(f"{'Ticker':<8} {'As-of':<25} {'Naive':<25}")

    all_tickers = sorted(set(asof_signals) | set(naive_signals))
    for ticker in all_tickers:
        asof = format_signal(asof_signals.get(ticker))
        naive = format_signal(naive_signals.get(ticker))
        print(f"{ticker:<8} {asof:<25} {naive:<25}")


if __name__ == "__main__":
    main()

