import pandas as pd
import streamlit as st

st.title("Customer Retention Decision Engine")
st.write("Set a budget and offer details to see who to target and the expected profit.")

df = pd.read_csv("app/scored_customers.csv")

budget = st.slider("Retention budget (NT$)", 10000, 1000000, 100000, step=10000)
offer_cost = st.slider("Cost per offer (NT$)", 10, 200, 50, step=10)
save_rate = st.slider("Offer success rate", 0.01, 0.20, 0.077, step=0.005)

df["saved_value"] = df["risk"] * save_rate * df["monthly_value"] * 12
df["expected_gain"] = df["saved_value"] - offer_cost
ranked = df.sort_values("expected_gain", ascending=False)

n_offers = min(budget // offer_cost, len(df))
smart = ranked.head(n_offers)
random_pick = df.sample(n_offers, random_state=42)

col1, col2, col3 = st.columns(3)
col1.metric("Customers targeted", f"{n_offers:,}")
col2.metric("Net profit (model)", f"NT${smart['saved_value'].sum() - n_offers * offer_cost:,.0f}")
col3.metric("Net profit (random)", f"NT${random_pick['saved_value'].sum() - n_offers * offer_cost:,.0f}")

profit = ranked["expected_gain"].cumsum().reset_index(drop=True)
st.subheader("Net profit by number of customers targeted")
st.line_chart(profit.iloc[::100])
st.write(f"Best number of customers to target: **{profit.idxmax() + 1:,}**")

st.subheader("Top 20 customers to contact")
st.dataframe(smart[["risk", "monthly_value", "expected_gain"]].head(20).round(2))