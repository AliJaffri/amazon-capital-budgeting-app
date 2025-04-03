# Streamlit app for comparing two Amazon projects with recommendations
import streamlit as st

st.set_page_config(page_title="Amazon Project Comparison", layout="centered")

st.title("Amazon Project Comparison Tool")
st.markdown("Evaluate two investment projects using Payback Period, NPV, and PI.")

# Fixed Inputs
st.header("Project Setup")
initial_investment = 10000.0
years = 4
discount_rate = st.slider("Select Discount Rate (%)", 1, 20, 10)

# Convert discount rate to decimal for calculations
rate = discount_rate / 100

st.markdown(f"**Initial Investment:** ${initial_investment:,.2f}")
st.markdown("**Project Duration:** 4 years")

# Project A: Fixed equal cash inflows
st.subheader("Project A: Equal Cash Flows")
cash_flows_a = [3000.0] * years
st.write(f"Annual Cash Inflows: $3000 for each year")

# Project B: Variable Cash Flows
st.subheader("Project B: Varying Cash Flows")
cash_flows_b = [1000.0, 2000.0, 4000.0, 5000.0]
for i, cf in enumerate(cash_flows_b):
    st.write(f"Year {i+1}: ${cf}")

# Calculation functions
def payback_period(investment, flows):
    cum_sum = 0
    for i, cash in enumerate(flows):
        cum_sum += cash
        if cum_sum >= investment:
            prev_sum = cum_sum - cash
            fraction = (investment - prev_sum) / cash
            return round(i + fraction, 2)
    return float('inf')

def present_value(flows, rate):
    return sum(cf / (1 + rate) ** (i + 1) for i, cf in enumerate(flows))

def npv(investment, flows, rate):
    pv_total = present_value(flows, rate)
    return round(pv_total - investment, 2)

def pi(investment, flows, rate):
    pv_total = present_value(flows, rate)
    return round(pv_total / investment, 3)

# Perform calculations
payback_a = payback_period(initial_investment, cash_flows_a)
payback_b = payback_period(initial_investment, cash_flows_b)
npv_a = npv(initial_investment, cash_flows_a, rate)
npv_b = npv(initial_investment, cash_flows_b, rate)
pi_a = pi(initial_investment, cash_flows_a, rate)
pi_b = pi(initial_investment, cash_flows_b, rate)

# Results
st.header("Results")
st.subheader("Payback Period")
st.write(f"Project A: {payback_a} years")
st.write(f"Project B: {payback_b} years")

st.subheader("Net Present Value (NPV)")
st.write(f"Project A: ${npv_a:,.2f}")
st.write(f"Project B: ${npv_b:,.2f}")

st.subheader("Profitability Index (PI)")
st.write(f"Project A: {pi_a}")
st.write(f"Project B: {pi_b}")

# Recommendation
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
    recommended = "Project A" if (npv_a > npv_b and npv_a > 0) else "Project B"
    st.success(f"✅ Based on the analysis, **{recommended} is the better investment**.")
else:
    st.warning("⚠️ Both projects have negative or zero NPV. Reconsider the investment.")

for reason in decision_reasons:
    st.markdown(f"- {reason}")

st.markdown("---")
st.markdown("*Developed for MSSU Capital Budgeting Class*")
