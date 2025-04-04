import streamlit as st
import matplotlib.pyplot as plt
import base64

# ------------------ CONFIG ------------------
st.set_page_config(page_title=" Capital Budgeting Techniques Projects Comparison Tool", layout="centered")
st.image("mssu_logo.png", width=150)

st.title("Capital Budgeting Techniques Projects Comparison Tool")
st.markdown("Compare two investment projects using Payback Period, Net Present Value (NPV), and Profitability Index (PI).")

# ------------------ INPUTS ------------------
st.header("Project Setup")
initial_investment = st.number_input("Initial Investment ($)", value=10000.00, step=500.00)
discount_rate = st.slider("Discount Rate (%)", min_value=1, max_value=20, value=10)
rate = discount_rate / 100

st.markdown(f"**Initial Investment:** ${initial_investment:,.2f}")

# Project A
st.subheader("Project A: Enter Annual Cash Flows")
years_a = st.number_input("Number of Years (Project A)", min_value=1, max_value=10, value=4)
cash_flows_a = [st.number_input(f"Year {i+1} Cash Flow (Project A)", key=f"a{i}", value=3000.00) for i in range(int(years_a))]

# Project B
st.subheader("Project B: Enter Annual Cash Flows")
years_b = st.number_input("Number of Years (Project B)", min_value=1, max_value=10, value=4)
default_b = [1000.00, 2000.00, 4000.00, 5000.00]
cash_flows_b = [st.number_input(f"Year {i+1} Cash Flow (Project B)", key=f"b{i}", value=default_b[i] if i < 4 else 0.00) for i in range(int(years_b))]

# ------------------ CALCULATIONS ------------------
def payback_period(investment, flows):
    cum_sum = 0
    for i, cash in enumerate(flows):
        cum_sum += cash
        if cum_sum >= investment:
            prev_sum = cum_sum - cash
            fraction = (investment - prev_sum) / cash
            return round(i + fraction, 2)
    return float('inf')

def present_value_list(flows, rate):
    return [round(cf / (1 + rate) ** (i + 1), 2) for i, cf in enumerate(flows)]

pv_flows_a = present_value_list(cash_flows_a, rate)
pv_flows_b = present_value_list(cash_flows_b, rate)
pv_total_a = sum(pv_flows_a)
pv_total_b = sum(pv_flows_b)
npv_a = round(pv_total_a - initial_investment, 2)
npv_b = round(pv_total_b - initial_investment, 2)
pi_a = round(pv_total_a / initial_investment, 3)
pi_b = round(pv_total_b / initial_investment, 3)
payback_a = payback_period(initial_investment, cash_flows_a)
payback_b = payback_period(initial_investment, cash_flows_b)

# ------------------ OUTPUTS ------------------
st.header("Results")

st.subheader("Payback Period")
st.write(f"**Project A**: {payback_a:.2f} years")
st.write(f"**Project B**: {payback_b:.2f} years")

st.subheader("Net Present Value (NPV)")

st.markdown("**Project A – Present Value of Cash Flows:**")
for i, pv in enumerate(pv_flows_a):
    st.write(f"Year {i+1}: ${pv:,.2f}")
st.write(f"**Total PV of Inflows (A):** ${pv_total_a:,.2f}")
st.write(f"**NPV = ${pv_total_a:,.2f} - ${initial_investment:,.2f} = ${npv_a:,.2f}**")

st.markdown("---")

st.markdown("**Project B – Present Value of Cash Flows:**")
for i, pv in enumerate(pv_flows_b):
    st.write(f"Year {i+1}: ${pv:,.2f}")
st.write(f"**Total PV of Inflows (B):** ${pv_total_b:,.2f}")
st.write(f"**NPV = ${pv_total_b:,.2f} - ${initial_investment:,.2f} = ${npv_b:,.2f}**")

st.subheader("Profitability Index (PI)")
st.write(f"**Project A**: {pi_a:.3f}")
st.write(f"**Project B**: {pi_b:.3f}")

# ------------------ RECOMMENDATION ------------------
st.subheader("Recommendation Summary")
decision_reasons = []

if payback_a < payback_b:
    decision_reasons.append("**Payback Period**: Project A recovers the investment faster.")
else:
    decision_reasons.append("**Payback Period**: Project B recovers the investment faster.")

if npv_a > npv_b:
    decision_reasons.append(f"**NPV**: Project A creates more value (${npv_a:,.2f} vs ${npv_b:,.2f}).")
else:
    decision_reasons.append(f"**NPV**: Project B creates more value (${npv_b:,.2f} vs ${npv_a:,.2f}).")

if pi_a > pi_b:
    decision_reasons.append("**PI**: Project A provides higher return per dollar invested.")
else:
    decision_reasons.append("**PI**: Project B provides higher return per dollar invested.")

if npv_a > 0 or npv_b > 0:
    if npv_a > npv_b and npv_a > 0:
        recommended = "Project A"
    elif npv_b > npv_a and npv_b > 0:
        recommended = "Project B"
    else:
        recommended = "Both projects are financially viable."
    st.success(f"✅ Based on the analysis, **{recommended} is the better investment.**")
else:
    st.warning("⚠️ Both projects have zero or negative NPV. Reconsider investing.")

for reason in decision_reasons:
    st.markdown(f"- {reason}")

# ------------------ CHART ------------------
st.subheader("Present Value Chart")
fig, ax = plt.subplots()
years = [f"Year {i+1}" for i in range(max(len(pv_flows_a), len(pv_flows_b)))]
ax.bar(years, pv_flows_a, label='Project A', alpha=0.6)
ax.bar(years, pv_flows_b, label='Project B', alpha=0.6)
ax.set_ylabel("Present Value ($)")
ax.set_title("Year-wise Present Value of Cash Flows")
ax.legend()
st.pyplot(fig)

st.markdown("---")
st.markdown("*Developed for MSSU Capital Budgeting Analysis*")
