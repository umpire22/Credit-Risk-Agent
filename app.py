import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page config ---
st.set_page_config(
    page_title="💳 Credit Risk Analysis Dashboard",
    page_icon="💳",
    layout="wide"
)

# --- Custom CSS for gradient background and cards ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #fbc2eb, #a6c1ee);
}
h1, h2, h3 {
    color: #3b3b3b;
}
.card {
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.metric-card {
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("💳 Credit Risk Analysis Dashboard")
st.markdown("Evaluate loan applicants visually and interactively.")

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
    if credit_score >= 700 and dti < 35:
        risk = "Low Risk"
        color = "#28a745"  # Green
        emoji = "✅"
    elif credit_score >= 600 and dti < 50:
        risk = "Medium Risk"
        color = "#ffc107"  # Yellow
        emoji = "⚠️"
    else:
        risk = "High Risk"
        color = "#dc3545"  # Red
        emoji = "❌"

    st.markdown(f"""
    <div class="card" style="background-color:{color}; color:white;">
        <h3>{emoji} {risk}</h3>
        <p><strong>Debt-to-Income Ratio:</strong> {dti:.2f}%</p>
        <p><strong>Credit Score:</strong> {credit_score}</p>
        <p><strong>Monthly Income:</strong> {income} {currency}</p>
        <p><strong>Monthly Debt:</strong> {debt} {currency}</p>
        <p><strong>Loan Amount Requested:</strong> {loan_amount} {currency}</p>
    </div>
    """, unsafe_allow_html=True)

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

    # --- Display dataframe ---
    def highlight_risk(row):
        if row["RiskLevel"] == "Low Risk":
            color = 'background-color: #d4edda; color: #155724'
        elif row["RiskLevel"] == "Medium Risk":
            color = 'background-color: #fff3cd; color: #856404'
        else:
            color = 'background-color: #f8d7da; color: #721c24'
        return [color]*len(row)

    st.dataframe(df.style.apply(highlight_risk, axis=1))

    # --- Summary Metrics ---
    total = len(df)
    low = len(df[df["RiskLevel"] == "Low Risk"])
    medium = len(df[df["RiskLevel"] == "Medium Risk"])
    high = len(df[df["RiskLevel"] == "High Risk"])

    st.subheader("📊 Risk Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f'<div class="metric-card" style="background-color:#6c757d;"><h3>Total Applicants</h3><h2>{total}</h2></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-card" style="background-color:#28a745;"><h3>Low Risk</h3><h2>{low}</h2></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metric-card" style="background-color:#ffc107; color:#212529;"><h3>Medium Risk</h3><h2>{medium}</h2></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="metric-card" style="background-color:#dc3545;"><h3>High Risk</h3><h2>{high}</h2></div>', unsafe_allow_html=True)

    # --- Risk Distribution Chart ---
    st.subheader("📈 Risk Distribution")
    fig = px.pie(df, names='RiskLevel', title='Risk Level Distribution', 
                 color='RiskLevel', color_discrete_map={'Low Risk':'#28a745','Medium Risk':'#ffc107','High Risk':'#dc3545'})
    st.plotly_chart(fig, use_container_width=True)

    # --- Download button ---
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "💾 Download Risk Report",
        data=csv,
        file_name="credit_risk_report.csv",
        mime="text/csv"
    )
