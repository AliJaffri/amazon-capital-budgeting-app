
# Streamlit app for comparing two Amazon projects
import streamlit as st
import numpy as np

st.set_page_config(page_title="Amazon Project Comparison", layout="centered")

st.title("Amazon Project Comparison Tool")
st.markdown("Use this tool to compare two Amazon investment projects.")

# Input section
st.header("Project Setup")
initial_investment = st.number_input("Initial Investment (in million $)", min_value=0.0, value=5.0)
years = st.slider("Project Duration (years)", 1, 10, 5)
discount_rate = st.slider("Discount Rate (%)", 1, 20, 8) / 100

st.subheader("Project A (Same Cash Flows)")
cash_flow_a = st.number_input("Annual Cash Inflow for Project A (in million $)", min_value=0.0, value=1.25)

st.subheader("Project B (Different Cash Flows)")
cash_flows_b = []
for i in range(years):
    cash = st.number_input(f"Year {i+1} Cash Inflow (in million $)", min_value=0.0, value=1.25, key=f"b_{i}")
    cash_flows_b.append(cash)

# Calculation functions
def payback_period(investment, flows):
    cum_sum = 0
    for i, cash in enumerate(flows):
        cum_sum += cash
        if cum_sum >= investment:
            return i + 1
    return float('inf')

def npv(investment, flows, rate):
    pv = sum(cf / (1 + rate)**(i+1) for i, cf in enumerate(flows))
    return pv - investment

def pi(investment, flows, rate):
    pv = sum(cf / (1 + rate)**(i+1) for i, cf in enumerate(flows))
    return pv / investment

# Construct cash flows for Project A
cash_flows_a = [cash_flow_a] * years

# Calculate metrics
st.header("Results")
st.subheader("Payback Period")
st.write(f"Project A: {payback_period(initial_investment, cash_flows_a)} years")
st.write(f"Project B: {payback_period(initial_investment, cash_flows_b)} years")

st.subheader("Net Present Value (NPV)")
st.write(f"Project A: ${npv(initial_investment, cash_flows_a, discount_rate):,.2f} million")
st.write(f"Project B: ${npv(initial_investment, cash_flows_b, discount_rate):,.2f} million")

st.subheader("Profitability Index (PI)")
st.write(f"Project A: {pi(initial_investment, cash_flows_a, discount_rate):.3f}")
st.write(f"Project B: {pi(initial_investment, cash_flows_b, discount_rate):.3f}")

st.markdown("---")
st.markdown("*Developed for MSSU Capital Budgeting Class*")
