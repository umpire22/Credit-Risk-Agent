import streamlit as st
import pandas as pd

# --- Page config ---
st.set_page_config(
    page_title="💳 Credit Risk Analysis Agent",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Credit Risk Analysis Agent")
st.markdown("Evaluate loan applicants for credit risk easily and visually.")

# --- Currency selection ---
currency = st.radio("Select Currency", ["USD ($)", "NGN (₦)"])

# --- Manual Entry ---
st.subheader("Manual Applicant Entry")
name = st.text_input("Applicant Name")
income = st.number_input(f"Monthly Income ({currency})", min_value=0, step=1000)
debt = st.number_input(f"Monthly Debt ({currency})", min_value=0, step=500)
credit_score = st.number_input("Credit Score (300-850)", min_value=300, max_value=850, step=10)
loan_amount = st.number_input(f"Loan Amount Requested ({currency})", min_value=0, step=5000)

if st.button("Assess Risk"):
    dti = (debt / income) * 100 if income > 0 else 0

    # Determine risk
    if credit_score >= 700 and dti < 35:
        risk = "Low Risk"
        color = "#d4edda"  # Green
        text_color = "#155724"
        emoji = "✅"
    elif credit_score >= 600 and dti < 50:
        risk = "Medium Risk"
        color = "#fff3cd"  # Yellow
        text_color = "#856404"
        emoji = "⚠️"
    else:
        risk = "High Risk"
        color = "#f8d7da"  # Red
        text_color = "#721c24"
        emoji = "❌"

    # Display result in a card-style box
    st.markdown(
        f"""
        <div style="background-color: {color}; padding: 20px; border-radius: 10px;">
            <h3 style="color: {text_color};">{emoji} {risk}</h3>
            <p><strong>Debt-to-Income Ratio:</strong> {dti:.2f}%</p>
            <p><strong>Credit Score:</strong> {credit_score}</p>
            <p><strong>Monthly Income:</strong> {income} {currency}</p>
            <p><strong>Monthly Debt:</strong> {debt} {currency}</p>
            <p><strong>Loan Amount Requested:</strong> {loan_amount} {currency}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Bulk Upload ---
st.subheader("Upload Applicant Dataset (CSV)")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # --- Risk evaluation ---
    def evaluate(row):
        dti = (row["Debt"] / row["Income"]) * 100 if row["Income"] > 0 else 0
        if row["CreditScore"] >= 700 and dti < 35:
            return "Low Risk"
        elif row["CreditScore"] >= 600 and dti < 50:
            return "Medium Risk"
        else:
            return "High Risk"

    df["RiskLevel"] = df.apply(evaluate, axis=1)

    # --- Color-code RiskLevel ---
    def highlight_risk(row):
        color = ""
        if row["RiskLevel"] == "Low Risk":
            color = 'background-color: #d4edda; color: #155724'  # Green
        elif row["RiskLevel"] == "Medium Risk":
            color = 'background-color: #fff3cd; color: #856404'  # Yellow
        else:
            color = 'background-color: #f8d7da; color: #721c24'  # Red
        return [color] * len(row)

    st.dataframe(df.style.apply(highlight_risk, axis=1))

    # --- Download button ---
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "💾 Download Risk Report",
        data=csv,
        file_name="credit_risk_report.csv",
        mime="text/csv"
    )
