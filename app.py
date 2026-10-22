"""Lab 15 — Interactive minimum-risk portfolio decision (uses portfolio.py math)."""
import io
import streamlit as st
from portfolio import (SLEEVES, CORRELATIONS, RESERVE_ELIGIBLE,
                       search_lowest_risk, estimate_from_prices)

st.set_page_config(page_title="Lab 15 Portfolio Stability", layout="wide")
st.title("Lab 15 — Portfolio Stability Decision")
st.caption("Built with AI help; a learning demonstration, not investment advice.")

objective_pct = st.sidebar.number_input("Minimum expected return (%)", value=6.5, step=0.1, format="%.2f")
reserve_pct = st.sidebar.number_input("Minimum reserve-eligible weight (%)", min_value=0.0, max_value=100.0,
                                      value=3.0, step=1.0, format="%.2f")
file = st.sidebar.file_uploader("Upload prices.csv (Date, then ticker columns)", type=["csv"])
last_36 = st.sidebar.checkbox("Use last 36 months", value=False)

try:
    if file is None:
        source = "Meridian training inputs"
        base_sleeves = {k: v.copy() for k, v in SLEEVES.items()}
        base_corr = [row.copy() for row in CORRELATIONS]
        current_sleeves = {k: v.copy() for k, v in base_sleeves.items()}
        current_corr = [row.copy() for row in base_corr]
    else:
        contents = file.getvalue()
        base_sleeves, base_corr, n_all = estimate_from_prices(io.BytesIO(contents), False)
        current_sleeves, current_corr, n_used = estimate_from_prices(io.BytesIO(contents), last_36)
        source = f"Uploaded price data: {n_used} monthly returns" + (" (last 36)" if last_36 else " (all)")
        st.info("Returns are historical estimates, not forecasts. Record each ticker's source and download date in your Markdown file.")

    st.subheader(source)
    st.write("Edit annual expected returns below. Check which assets qualify for the reserve rule.")
    edited_sleeves = {k: v.copy() for k, v in current_sleeves.items()}
    selected_eligible = []
    for name in edited_sleeves:
        c1, c2 = st.columns([3, 2])
        with c1:
            val = st.number_input(f"{name}: expected annual return (%)", value=round(current_sleeves[name]["return"] * 100, 6),
                                  step=0.1, format="%.2f", key="return_" + name)
            edited_sleeves[name]["return"] = val / 100
        with c2:
            selected = st.checkbox(f"Reserve eligible: {name}", value=name in RESERVE_ELIGIBLE,
                                   key="eligible_" + name)
            if selected:
                selected_eligible.append(name)

    # A loaded-input baseline, using the same current objective and reserve rule.
    baseline = search_lowest_risk(base_sleeves, base_corr, objective_pct / 100,
                                  reserve_pct / 100, selected_eligible)
    actual = search_lowest_risk(edited_sleeves, current_corr, objective_pct / 100,
                                reserve_pct / 100, selected_eligible)

    def show_answer(title, result):
        st.markdown(f"### {title}")
        if result is None:
            st.warning("No mix meets the objective and reserve rule.")
        else:
            for name, wt in result["weights"].items():
                st.write(f"{name}: **{wt * 100:.2f}%**")
            st.metric("Expected return", f"{result['return'] * 100:.2f}%")
            st.metric("Volatility", f"{result['volatility'] * 100:.2f}%")
            st.metric("Reserve-eligible weight", f"{result['reserve'] * 100:.2f}%")

    left, right = st.columns(2)
    with left:
        show_answer("Current selection", actual)
    with right:
        show_answer("As loaded (all months for CSV)", baseline)
    if actual is not None and baseline is not None:
        biggest = max(abs(actual["weights"][n] - baseline["weights"][n]) for n in edited_sleeves) * 100
        st.metric("Largest weight change vs. loaded input", f"{biggest:.0f} percentage points")
    else:
        st.write("Largest weight change: unavailable because at least one mix is infeasible.")
except Exception as exc:
    st.error(f"Check the input data: {exc}")
    st.stop()
