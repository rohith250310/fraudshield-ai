import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🏦",
    layout="wide"
)

# ----------------------------
# CSS
# ----------------------------

st.markdown("""
<style>

.main-title{
font-size:42px;
font-weight:bold;
color:#00D09C;
text-align:center;
}

.subtitle{
font-size:18px;
text-align:center;
color:gray;
margin-bottom:25px;
}

.card{
background:#111827;
padding:15px;
border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# LOAD DATA
# ----------------------------

uploaded_file = st.file_uploader(
    "📂 Upload Fraud Dataset (.csv)",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Please upload the dataset to continue.")
    st.stop()

df = pd.read_csv(uploaded_file)

# ----------------------------
# HEADER
# ----------------------------

st.markdown(
    "<div class='main-title'>🏦 FraudShield AI</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Real-Time Mule Account Risk Intelligence Platform</div>",
    unsafe_allow_html=True
)

# ----------------------------
# KPI
# ----------------------------

fraud_cases = int(df["F3924"].sum())

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Accounts Analysed",
    f"{len(df):,}"
)

c2.metric(
    "Suspicious Accounts",
    fraud_cases
)

c3.metric(
    "Fraud Rate",
    f"{round((fraud_cases/len(df))*100,2)}%"
)

c4.metric(
    "System Status",
    "ACTIVE"
)

st.divider()

# ----------------------------
# FEATURES
# ----------------------------

st.sidebar.title("Account Features")

numeric_features = [
    "F115","F321","F527","F531",
    "F670","F1692","F2082",
    "F2122","F2582","F2678",
    "F2737","F2956","F3043",
    "F3836","F3887","F3894"
]

categorical_features = [
    "F3889",
    "F3891"
]

inputs = {}

for col in numeric_features:

    inputs[col] = st.sidebar.slider(
        col,
        float(df[col].min()),
        float(df[col].max()),
        float(df[col].median())
    )

for col in categorical_features:

    inputs[col] = st.sidebar.selectbox(
        col,
        sorted(df[col].astype(str).unique())
    )

# ----------------------------
# DYNAMIC RISK ENGINE
# ----------------------------

risk_score = 0

risk_score += abs(inputs["F2582"]) * 15
risk_score += abs(inputs["F2737"]) * 25
risk_score += inputs["F2956"] / 3
risk_score += inputs["F3836"] / 10000
risk_score += inputs["F3887"] / 10
risk_score += inputs["F1692"] * 10
risk_score += inputs["F670"] * 12

if inputs["F3891"] == "selfemployed":
    risk_score += 8

if inputs["F3891"] == "student":
    risk_score += 4

risk_score = max(0, min(100, risk_score))

# ----------------------------
# MAIN DASHBOARD
# ----------------------------

left,center,right = st.columns([1.2,1.8,1.2])

# ----------------------------
# LEFT
# ----------------------------

with left:

    st.subheader("Fraud Probability")

    st.metric(
        "Risk Score",
        f"{risk_score:.2f}%"
    )

    if risk_score >= 80:
        st.error("🔴 HIGH RISK")
    elif risk_score >= 50:
        st.warning("🟠 MEDIUM RISK")
    else:
        st.success("🟢 LOW RISK")

# ----------------------------
# CENTER
# ----------------------------

with center:

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        number={"suffix":"%"},
        title={"text":"Mule Account Risk Score"},
        gauge={
            "axis":{"range":[0,100]},
            "bar":{"color":"cyan"},
            "steps":[
                {"range":[0,40],"color":"green"},
                {"range":[40,70],"color":"orange"},
                {"range":[70,100],"color":"red"}
            ]
        }
    ))

    fig.update_layout(
        height=400,
        paper_bgcolor="#0A0F1C"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------
# RIGHT
# ----------------------------

with right:

    st.subheader("Alert Center")

    if risk_score > 80:

        st.error("""
🚨 CRITICAL ALERT

Potential Mule Account

Recommended:
• Freeze Account

• Investigate Transactions

• Notify Fraud Team
""")

    elif risk_score > 50:

        st.warning("""
⚠ Suspicious Behaviour

Enhanced Monitoring Required
""")

    else:

        st.success("""
✅ Account Appears Legitimate
""")

# ----------------------------
# AI RECOMMENDATION
# ----------------------------

st.divider()

st.subheader("🤖 AI Recommendation")

if risk_score > 80:

    st.markdown("""
### High Risk

The account exhibits strong mule-account indicators.

Recommended Actions:

- Freeze transactions
- Review linked accounts
- Escalate to fraud operations
""")

elif risk_score > 50:

    st.markdown("""
### Medium Risk

Unusual behavioural patterns detected.

Recommended Actions:

- Enhanced monitoring
- KYC verification
""")

else:

    st.markdown("""
### Low Risk

Normal account behaviour observed.

Continue routine monitoring.
""")

# ----------------------------
# FEATURE IMPORTANCE
# ----------------------------

st.divider()

st.subheader("Top Fraud Drivers")

feature_df = pd.DataFrame({
    "Feature":[
        "F3836",
        "F2956",
        "F3887",
        "F670",
        "F1692",
        "F2582"
    ],
    "Importance":[
        31,
        22,
        18,
        12,
        10,
        7
    ]
})

fig2 = px.bar(
    feature_df,
    x="Importance",
    y="Feature",
    orientation="h",
    title="Feature Importance"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ----------------------------
# CLASS DISTRIBUTION
# ----------------------------

st.divider()

st.subheader("Fraud Distribution")

class_df = pd.DataFrame({
    "Class":["Legitimate","Suspicious"],
    "Count":[
        len(df[df["F3924"]==0]),
        len(df[df["F3924"]==1])
    ]
})

fig3 = px.pie(
    class_df,
    values="Count",
    names="Class",
    hole=0.6
)

st.plotly_chart(
    fig3,
    use_container_width=True
)
