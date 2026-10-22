"""FIN 439 Lab 15: interactive portfolio stability decision."""
import io
import streamlit as st
from portfolio import SLEEVES, CORRELATIONS, RESERVE_ELIGIBLE, search_lowest_risk, estimate_from_prices

st.set_page_config(page_title="Lab 15 Portfolio Stability", layout="wide")
st.title("Lab 15 — Portfolio Stability Decision")
st.caption("Built with AI help; a learning demonstration, not investment advice.")

objective = st.sidebar.number_input("Minimum expected return (%)", value=6.5, step=0.1, format="%.2f") / 100
reserve_min = st.sidebar.number_input("Minimum reserve-eligible weight (%)", min_value=0.0, max_value=100.0, value=3.0, step=1.0) / 100
upload = st.sidebar.file_uploader("Upload prices.csv (date first, then tickers)", type=["csv"])
last_36 = st.sidebar.checkbox("Use last 36 months", value=False)


def render_result(label, result):
    st.subheader(label)
    if result is None:
        st.warning("No mix meets the objective and reserve rule.")
        return
    for name, weight in result["weights"].items():
        st.write(f"{name}: **{100 * weight:.2f}%**")
    st.metric("Expected return", f"{100 * result['return']:.2f}%")
    st.metric("Volatility", f"{100 * result['volatility']:.2f}%")
    st.metric("Reserve-eligible weight", f"{100 * result['reserve']:.2f}%")


def maximum_change(a, b):
    if a is None or b is None:
        return None
    return max(abs(a["weights"][name] - b["weights"][name]) for name in a["weights"]) * 100


try:
    if upload is None:
        baseline_sleeves = {k: v.copy() for k, v in SLEEVES.items()}
        baseline_corr = [row.copy() for row in CORRELATIONS]
        active_sleeves = {k: v.copy() for k, v in baseline_sleeves.items()}
        active_corr = [row.copy() for row in baseline_corr]
        source_id = "meridian"
        st.subheader("Meridian training data")
    else:
        data = upload.getvalue()
        baseline_sleeves, baseline_corr, n_all = estimate_from_prices(io.BytesIO(data), False)
        active_sleeves, active_corr, n_used = estimate_from_prices(io.BytesIO(data), last_36)
        source_id = str(hash(data)) + ("_36" if last_36 else "_all")
        st.subheader(f"Uploaded ETF prices: {n_used} monthly returns" + (" (last 36)" if last_36 else " (all months)"))
        st.info("All return, volatility, and correlation inputs are historical estimates, not forecasts. Record each ticker's source and actual download date in the notes.")

    st.write("Edit expected annual returns or reserve eligibility. With a CSV uploaded, the return boxes refresh when you switch between all months and 36 months.")
    edited = {k: v.copy() for k, v in active_sleeves.items()}
    eligible = []
    for name in edited:
        a, b = st.columns([3, 2])
        with a:
            val = st.number_input(
                f"{name}: expected annual return (%)",
                value=round(active_sleeves[name]["return"] * 100, 4),
                step=0.1, format="%.2f", key=f"return_{source_id}_{name}",
            )
            edited[name]["return"] = val / 100
        with b:
            default = name in RESERVE_ELIGIBLE or (upload is not None and name.upper() in {"SGOV", "IEF"})
            checked = st.checkbox(f"Reserve eligible: {name}", value=default, key=f"eligible_{name}")
            if checked:
                eligible.append(name)

    current = search_lowest_risk(edited, active_corr, objective, reserve_min, eligible)
    baseline = search_lowest_risk(baseline_sleeves, baseline_corr, objective, reserve_min, eligible)
    l, r = st.columns(2)
    with l:
        render_result("Current selection", current)
    with r:
        render_result("As loaded (Meridian or all CSV months)", baseline)
    difference = maximum_change(current, baseline)
    st.write("Largest weight change vs. loaded input: " + (f"**{difference:.0f} percentage points**" if difference is not None else "unavailable because a portfolio is infeasible"))

    if upload is not None:
        st.divider()
        st.subheader("All months vs. last 36 months — unedited historical estimates")
        recent_sleeves, recent_corr, recent_n = estimate_from_prices(io.BytesIO(data), True)
        all_result = search_lowest_risk(baseline_sleeves, baseline_corr, objective, reserve_min, eligible)
        recent_result = search_lowest_risk(recent_sleeves, recent_corr, objective, reserve_min, eligible)
        c1, c2 = st.columns(2)
        with c1:
            render_result(f"All months ({n_all} returns)", all_result)
        with c2:
            render_result(f"Last {recent_n} months", recent_result)
        comparison = maximum_change(all_result, recent_result)
        st.write("Largest change between estimation windows: " + (f"**{comparison:.0f} percentage points**" if comparison is not None else "unavailable because one or both windows are infeasible"))
except Exception as error:
    st.error(f"Unable to compute this portfolio: {error}")
    st.stop()
