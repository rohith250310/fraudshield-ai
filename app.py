import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🏦",
    layout="wide"
)

# ----------------------------
# HEADER
# ----------------------------
st.title("🏦 FraudShield AI")
st.subheader("Mule Account Detection + Explainable AI System")

# ----------------------------
# UPLOAD DATA
# ----------------------------
file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if file is None:
    st.stop()

df = pd.read_csv(file)

# ----------------------------
# ACCOUNT ID
# ----------------------------
df.rename(columns={df.columns[0]: "Account_ID"}, inplace=True)

label_col = "F3924"

# ----------------------------
# FEATURES
# ----------------------------
features = ["F2582","F2737","F2956","F3836","F3887","F1692","F670"]

for col in features:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# ----------------------------
# NORMALIZATION
# ----------------------------
df_norm = df.copy()

for col in features:
    min_val = df[col].min()
    max_val = df[col].max()
    df_norm[col] = (df[col] - min_val) / (max_val - min_val + 1e-9)

# ----------------------------
# RISK SCORE ENGINE
# ----------------------------
df["Risk_Score"] = (
    df_norm["F2582"] * 15 +
    df_norm["F2737"] * 25 +
    df_norm["F2956"] * 20 +
    df_norm["F3836"] * 10 +
    df_norm["F3887"] * 10 +
    df_norm["F1692"] * 10 +
    df_norm["F670"] * 10
)

df["Risk_Score"] = (df["Risk_Score"] / df["Risk_Score"].max()) * 100
df["Risk_Score"] = df["Risk_Score"].fillna(0).clip(0, 100)

# ----------------------------
# CATEGORY
# ----------------------------
def categorize(x):
    if x >= 80:
        return "HIGH RISK"
    elif x >= 50:
        return "MEDIUM RISK"
    else:
        return "LOW RISK"

df["Risk_Category"] = df["Risk_Score"].apply(categorize)

# =========================================================
# 📌 TABLE
# =========================================================
st.subheader("📌 Mule Account Detection Table")

table_df = df[[
    "Account_ID",
    label_col,
    "Risk_Score",
    "Risk_Category"
]].rename(columns={
    label_col: "Mule Account Status"
})

st.dataframe(table_df, use_container_width=True)

# =========================================================
# 🚨 TOP 10
# =========================================================
st.subheader("🚨 Top 10 Suspicious Accounts")

top_df = df.sort_values("Risk_Score", ascending=False).head(10)

top_df = top_df.rename(columns={
    label_col: "Mule Account Status"
})

st.dataframe(
    top_df[[
        "Account_ID",
        "Mule Account Status",
        "Risk_Score",
        "Risk_Category"
    ]],
    use_container_width=True
)

# =========================================================
# 📊 RISK CATEGORY BAR GRAPH
# =========================================================
st.subheader("📊 Risk Category Distribution")

category_counts = df["Risk_Category"].value_counts().reset_index()
category_counts.columns = ["Risk Category", "Count"]

fig1 = px.bar(
    category_counts,
    x="Risk Category",
    y="Count",
    color="Risk Category",
    text="Count",
    title="Fraud Risk Distribution"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================================================
# 🔥 FRAUD DRIVERS (NOW BAR GRAPH - IMPORTANT UPGRADE)
# =========================================================
st.subheader("🧠 Most Important Fraud Drivers (System Level)")

driver_df = pd.DataFrame({
    "Feature": [
        "Transaction Anomaly (F2737)",
        "Account Behavior (F2582)",
        "Transaction Frequency (F2956)",
        "Large Amount Activity (F3836)",
        "Risk Signal Strength (F3887)",
        "Behavior Deviation (F1692)",
        "Velocity Pattern (F670)"
    ],
    "Impact Score": [
        25,
        15,
        20,
        10,
        10,
        10,
        10
    ]
})

fig2 = px.bar(
    driver_df,
    x="Impact Score",
    y="Feature",
    orientation="h",
    color="Impact Score",
    text="Impact Score",
    title="Key Fraud Driving Features"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# 🔍 ACCOUNT INVESTIGATION TOOL
# =========================================================
st.subheader("🔍 AI Explainable Fraud Detection")

acc_id = st.text_input("Enter Account ID to analyze")

if acc_id:

    result = df[df["Account_ID"].astype(str) == str(acc_id)]

    if len(result) == 0:
        st.error("Account not found")

    else:
        row = result.iloc[0]

        col1, col2, col3 = st.columns(3)

        col1.metric("Risk Score", round(row["Risk_Score"], 2))
        col2.metric("Risk Category", row["Risk_Category"])
        col3.metric("Mule Status", row[label_col])

        st.markdown("### 🧠 AI Explanation")

        reasons = []

        if row["F2737"] > df["F2737"].mean():
            reasons.append("High transaction anomaly (F2737)")

        if row["F2582"] > df["F2582"].mean():
            reasons.append("Unusual financial behavior (F2582)")

        if row["F2956"] > df["F2956"].mean():
            reasons.append("Abnormal transaction frequency (F2956)")

        if row["Risk_Score"] > 80:
            reasons.append("Critical risk threshold exceeded")

        if len(reasons) == 0:
            reasons.append("Normal behavioral pattern observed")

        for r in reasons:
            st.write("✔", r)

# =========================================================
# 🤖 AI RECOMMENDATION ENGINE
# =========================================================
st.divider()

st.subheader("🤖 AI Recommendation Engine")

high_risk = len(df[df["Risk_Category"] == "HIGH RISK"])

if high_risk > 0:

    st.error("🚨 HIGH ALERT: Mule Accounts Detected")

    st.markdown("""
### Recommended Actions:

- Freeze HIGH RISK accounts immediately  
- Investigate suspicious transactions  
- Perform KYC re-verification  
- Check linked account networks  
- Escalate to fraud investigation team  
""")

else:

    st.success("✅ System Normal")

    st.markdown("""
### Recommendation:

- Continue monitoring transactions  
- No immediate action required  
""")
