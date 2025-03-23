import streamlit as st
import matplotlib.pyplot as plt

st.title("💰 Compound interest calculation 💰")

# User input for investment parameters
Initial_capital = st.number_input("Initial capital (€):", min_value=0, value=1000, step=100)
Monthly_contribution = st.number_input("Monthly contribution (€):", min_value=0, value=100, step=10)
Annual_interest_rate = st.slider("Annual interest rate (%):", 0.0, 20.0, 5.0, 0.1)
Years = st.slider("Period (Years):", 1, 50, 10)
Inflation = st.slider("Annual inflation (%):", 0.0, 10.0, 2.0, 0.1)
Freq = st.selectbox("Frequency capitalization:", ["Annual", "Semester", "Quarterly", "Monthly"])

# Calculations for investment periods
Periods_per_year = {"Annual": 1, "Semester": 2, "Quarterly": 4, "Monthly": 12}[Freq]
Rate_period = Annual_interest_rate / 100 / Periods_per_year
Inflation_period = Inflation / 100 / Periods_per_year
Total_periods = Years * Periods_per_year
Contribution_period = Monthly_contribution * 12 / Periods_per_year

# Calculation of investment values over time
Values = [Initial_capital] # Investment history
Value = Initial_capital

# Cycle repeating for each investment period.
for _ in range(Total_periods):
    Interest = Value * Rate_period
    Value += Interest + Contribution_period
    Values.append(Value)

# Calculation of real values considering inflation
Real_values = [Values[i] * (1 - Inflation_period) ** i for i in range(len(Values))]

# Calculation of total contributions over time
Contributions = [Initial_capital + Contribution_period * i for i in range(Total_periods + 1)]

# Displaying key results
st.header("Results")
Final_value = Values[-1]
Real_value = Real_values[-1]
Total_contribution = Initial_capital + (Contribution_period * Total_periods)
Interest_earned = Final_value - Total_contribution
st.metric("Final value", f"€{Final_value:,.2f}")
st.metric("Real value (with inflation)", f"€{Real_value:,.2f}")
st.metric("Total contribution", f"€{Total_contribution:,.2f}")
st.metric("Interest earned", f"€{Interest_earned:,.2f}")

# Creating the investment graph
st.subheader("Investment graph")
fig, ax = plt.subplots(figsize=(10, 5))
x = [i / Periods_per_year for i in range(Total_periods + 1)]

# Adding the three lines to the graph
ax.plot(x, Values, label="Nominal value", color="blue", linewidth=2)
ax.plot(x, Real_values, label="Real value", color="green", linewidth=2)
ax.plot(x, Contributions, label="Contributions", color="red", linestyle="--")

# Chart configuration
ax.set_xlabel("Years")
ax.set_ylabel("Value (€)")
ax.grid(True, alpha=0.3)
ax.legend()

st.pyplot(fig)

st.subheader("Investment tips")
st.info("""
- A 1% increase in the rate of return can have a significant impact in the long run.
- Starting investing early is often more important than the rate of return.
- Inflation reduces purchasing power over time, so always consider the real value.
- Diversifying investments can help manage risk.
""")
