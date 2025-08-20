import streamlit as st
import pandas as pd

st.title("💳 Credit Risk Analysis Agent")

st.write("Evaluate loan applicants for credit risk.")

# Manual Entry
st.subheader("Manual Applicant Entry")
name = st.text_input("Applicant Name")
income = st.number_input("Monthly Income ($)", min_value=0, step=100)
debt = st.number_input("Monthly Debt ($)", min_value=0, step=50)
credit_score = st.number_input("Credit Score (300-850)", min_value=300, max_value=850, step=10)
loan_amount = st.number_input("Loan Amount Requested ($)", min_value=0, step=500)

if st.button("Assess Risk"):
    dti = (debt / income) * 100 if income > 0 else 0
    st.write(f"Debt-to-Income Ratio: {dti:.2f}%")

    if credit_score >= 700 and dti < 35:
        st.write("✅ Low Risk (Good candidate for loan)")
    elif credit_score >= 600 and dti < 50:
        st.write("⚠️ Medium Risk (Consider further checks)")
    else:
        st.write("❌ High Risk (Not recommended)")

# Bulk Upload
st.subheader("Upload Applicant Dataset (CSV)")
uploaded_file = st.file_uploader("Upload file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    def evaluate(row):
        dti = (row["Debt"] / row["Income"]) * 100 if row["Income"] > 0 else 0
        if row["CreditScore"] >= 700 and dti < 35:
            return "Low Risk"
        elif row["CreditScore"] >= 600 and dti < 50:
            return "Medium Risk"
        else:
            return "High Risk"

    df["RiskLevel"] = df.apply(evaluate, axis=1)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Risk Report", data=csv, file_name="credit_risk_report.csv")
