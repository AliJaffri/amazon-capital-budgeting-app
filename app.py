import streamlit as st

st.set_page_config(page_title="Projects Comparison Tool", layout="centered")

# 🟨 Add MSSU logo centered at the top
st.markdown(
    """
    <div style="text-align: center;">
        <img src="mssu_logo.png" width="150">
    </div>
    """,
    unsafe_allow_html=True
)

st.title("Project Comparison Tool")
st.markdown("Compare two investment projects using Payback Period, NPV, and Profitability Index (PI).")

# Initial inputs
st.header("Project Setup")
initial_investment = st.number_input("Initial Investment ($)", value=10000.0, step=500.0)
discount_rate = st.slider("Discount Rate (%)", min_value=1, max_value=20, value=10)
rate = discount_rate / 100

st.markdown(f"**Initial Investment:** ${initial_investment:,.2f}")

# Input cash flows for Project A
st.subheader("Project A: Enter Annual Cash Flows")
years_a = st.number_input("Number of Years (Project A)", min_value=1, max_value=10, value=4)
cash_flows_a = []
for i in range(int(years_a)):
    cash = st.number_input(f"Year {i+1} Cash Flow (Project A)", key=f"a{i}", value=3000.0)
    cash_flows_a.append(cash)

# Input cash flows for Project B
st.subheader("Project B: Enter Annual Cash Flows")
years_b = st.number_input("Number of Years (Project B)", min_value=1, max_value=10, value=4)
cash_flows_b = []
for i in range(int(years_b)):
    default_b = [1000.0, 2000.0, 4000.0, 5000.0]
    cash = st.number_input(f"Year {i+1} Cash Flow (Project B)", key=f"b{i}", value=default_b[i] if i < 4 else 0.0)
    cash_flows_b.append(cash)

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

def present_value_list(flows, rate):
    return [round(cf / (1 + rate) ** (i + 1), 2) for i, cf in enumerate(flows)]

# Calculate PVs for both projects
pv_flows_a = present_value_list(cash_flows_a, rate)
pv_flows_b = present_value_list(cash_flows_b, rate)
pv_total_a = sum(pv_flows_a)
pv_total_b = sum(pv_flows_b)

# Calculate NPV, PI, Payback
npv_a = round(pv_total_a - initial_investment, 2)
npv_b = round(pv_total_b - initial_investment, 2)
pi_a = round(pv_total_a / initial_investment, 3)
pi_b = round(pv_total_b / initial_investment, 3)
payback_a = payback_period(initial_investment, cash_flows_a)
payback_b = payback_period(initial_investment, cash_flows_b)

# Display Results
st.header("Results")

st.subheader("Payback Period")
st.write(f"**Project A**: {payback_a} years")
st.write(f"**Project B**: {payback_b} years")

st.subheader("Net Present Value (NPV)")

st.markdown("**Project A – PV of Cash Flows:**")
for i, pv in enumerate(pv_flows_a):
    st.write(f"Year {i+1}: ${pv:,.2f}")
st.write(f"**Total PV of Inflows (A):** ${pv_total_a:,.2f}")
st.write(f"**NPV = PV of Inflows - Initial Investment = ${pv_total_a:,.2f} - ${initial_investment:,.2f} = ${npv_a:,.2f}**")

st.markdown("---")

st.markdown("**Project B – PV of Cash Flows:**")
for i, pv in enumerate(pv_flows_b):
    st.write(f"Year {i+1}: ${pv:,.2f}")
st.write(f"**Total PV of Inflows (B):** ${pv_total_b:,.2f}")
st.write(f"**NPV = PV of Inflows - Initial Investment = ${pv_total_b:,.2f} - ${initial_investment:,.2f} = ${npv_b:,.2f}**")

st.subheader("Profitability Index (PI)")
st.write(f"**Project A**: {pi_a}")
st.write(f"**Project B**: {pi_b}")

# Recommendation Logic
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

# Final recommendation
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

st.markdown("---")
st.markdown("*Developed for capital budgeting analysis*")
