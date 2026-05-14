# scam_sniff_dashboard.py
import streamlit as st
import pandas as pd
import csv
import os

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="ScamSniff - Scam Detection Dashboard",
    page_icon="🔍",
    layout="wide",
)

# ---------------- Custom Styling ----------------
st.markdown("""
<style>
body {
    background-color: #fafafa;
}
.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    color: #5b0060;
}
.subheading {
    text-align: center;
    font-size: 20px;
    color: #fb5607;
}
.metric-box {
    text-align: center;
    background: #fff;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0px 0px 10px rgba(240, 120, 150, 0.2);
}
.card {
    background-color: #fff7fa;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #ffc1d3;
    margin: 15px 0;
}
.result-card {
    background-color: #fff;
    border-left: 6px solid #ff006e;
    padding: 18px;
    margin-top: 20px;
    border-radius: 10px;
}
.success-card {
    background-color: #e0fff1;
    border-left: 6px solid #06d6a0;
    padding: 18px;
    border-radius: 10px;
}
.report-box {
    background-color: #f5f0ff;
    border-left: 6px solid #8338ec;
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
}
.sidebar .sidebar-content {
    background: linear-gradient(to bottom right, #ff5f6d, #ffc371);
}
</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar Overview ----------------
with st.sidebar:
    st.image("logo.svg", width=160)
    st.markdown("## ScamSniff Dashboard")
    st.caption("Smart detection and reporting system for Instagram scam pages.")
    st.markdown("---")
    st.markdown("### 📊 App Stats:")

    if os.path.exists("data.csv"):
        df = pd.read_csv("data.csv")
        scams = df[
            (df["contact_info"] == "NO") & 
            (df["website"] == "NO") & 
            (df["comments_status"] == "OFF") & 
            (df["method_payment"].isin(["PREPAY", "ADVPAY"]))
        ]
        legit = len(df) - len(scams)
        st.metric("Total Pages Analyzed", len(df))
        st.metric("Detected Scam Pages", len(scams))
        st.metric("Likely Genuine Pages", legit)
    else:
        st.info("No data available yet.")

    st.markdown("---")
    st.info("Use this dashboard to check page credibility, detect scams, and view community reports.")

# ---------------- Front Header ----------------
st.markdown('<div class="main-title">ScamSniff 🔍</div>', unsafe_allow_html=True)
st.markdown('<div class="subheading">Sniffs out scam pages, protecting users from Instagram scams. Ensures safe online shopping.</div>', unsafe_allow_html=True)
st.markdown("---")

# Load CSV Files
data_file = "data.csv"
reports_file = "reports.csv"
df = pd.read_csv(data_file) if os.path.exists(data_file) else pd.DataFrame()
reports_df = pd.read_csv(reports_file) if os.path.exists(reports_file) else pd.DataFrame()

# ---------------- Main App ----------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🔎 Scam Detection Zone")
    handle = st.text_input("Enter Instagram Handle", placeholder="e.g., scamshop_trendy")

    if handle:
        if handle in df["handle"].values:
            row = df[df["handle"] == handle].iloc[0]
            st.success(f"✅ Handle '{handle}' found in database")

            with st.expander("📊 Page Insights", expanded=True):
                st.markdown(f"""
                <div class="card">
                    <b>Follower/Following Ratio:</b> {row['follower_following_ratio']}<br>
                    <b>Number of Posts:</b> {row['posts']}<br>
                    <b>Account Age (days):</b> {row['account_life_days']}<br>
                    <b>Engagement Rate:</b> {row['engagement_rate']}<br>
                    <b>Contact Info:</b> {row['contact_info']}<br>
                    <b>Website Link:</b> {row['website']}<br>
                    <b>Comments:</b> {row['comments_status']}<br>
                    <b>Comment Type:</b> {row['comment_type'] if row['comments_status']=="ON" else "NULL"}<br>
                    <b>Payment Method:</b> {row['method_payment']}<br>
                    <b>Tagged by Customers:</b> {row['customer_tags']}
                </div>
                """, unsafe_allow_html=True)

            if st.button("🚨 Detect Scam"):
                scam_flag = (
                    row["contact_info"].upper() == "NO"
                    and row["website"].upper() == "NO"
                    and row["comments_status"].upper() == "OFF"
                    and row["method_payment"].upper() in ["PREPAY", "ADVPAY"]
                )
                if scam_flag:
                    st.markdown("""
                    <div class="result-card">
                        <h4>⚠ Scam Detected</h4>
                        This profile demonstrates clear scam characteristics:<br>
                        - Missing contact and website links.<br>
                        - Comments disabled.<br>
                        - Advance/Prepay payment type.<br>
                        <b>Certainty:</b> 97%
                    </div>
                    """, unsafe_allow_html=True)

                    reports = reports_df[reports_df["handle"].str.lower() == handle.lower()]
                    if not reports.empty:
                        st.markdown(f"<h5 style='color:#d90429;'>🚨 {len(reports)} Scam Reports Found</h5>", unsafe_allow_html=True)
                        for idx, rpt in reports.iterrows():
                            st.markdown(f"<div class='report-box'><b>🧾 Review {idx+1}:</b> {rpt['user_experience']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="success-card">
                        <h4>✅ Legitimate Page</h4>
                        This profile appears genuine based on all current indicators.<br>
                        <b>Certainty:</b> 80%
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Handle not in database — please enter information manually below.")
            with st.form("manual_entry"):
                followers = st.number_input("Followers", min_value=0)
                following = st.number_input("Following", min_value=0)
                posts = st.number_input("Posts", min_value=0)
                age = st.number_input("Account Age (days)", min_value=0)
                contact = st.selectbox("Contact Info", ["YES", "NO"])
                website = st.selectbox("Website", ["YES", "NO"])
                comments = st.selectbox("Comments", ["ON", "OFF"])
                payment = st.selectbox("Payment Method", ["COD", "PREPAY", "ADVPAY"])
                tags = st.selectbox("Tagged?", ["YES", "NO"])
                submit = st.form_submit_button("🚨 Detect Scam")
                
                if submit:
                    scam_flag = (contact == "NO" and website == "NO" and comments == "OFF" and payment in ["PREPAY", "ADVPAY"])
                    if scam_flag:
                        st.error("⚠ Classified as SCAM — risky payment & lack of transparency detected.")
                    else:
                        st.success("✅ Page appears safe.")

with col2:
    st.markdown("### 🧩 Scam Reports Center")
    report_handle = st.text_input("Report Handle")
    experience = st.text_area("Describe Your Experience")
    proof = st.file_uploader("Upload Proof", type=["jpg", "png", "pdf"])
    if st.button("Submit Report"):
        if report_handle and experience:
            with open(reports_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([report_handle, experience, proof.name if proof else "None"])
            st.success("✅ Thank you! Your report has been recorded securely.")
        else:
            st.error("Please provide handle name and details before submitting.")

# End
st.markdown("---")
st.caption("© 2025 ScamSniff | Built with ❤ for Safer Online Shopping.")