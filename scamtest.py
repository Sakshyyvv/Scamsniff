# scam_sniff_v2.py
import streamlit as st
import pandas as pd
import csv
import os
data_file = "data.csv"
report_file = "reports.csv"
# Add "user_id" column in reports.csv if starting fresh or adapt logic/check for it!
report_headers = ["handle", "user_id", "user_experience", "proof_filename"]
if not os.path.exists(report_file) or pd.read_csv(report_file).shape[1] == 3:
    # Create with user_id column if not exist or old format detected
    with open(report_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(report_headers)

# Reload after possible header update
try:
    reports_df = pd.read_csv(report_file)
except Exception:
    reports_df = pd.DataFrame(columns=report_headers)
    
# --------------------------- BACKEND SETUP ----------------------------

# Create data.csv if it doesn’t exist
if not os.path.exists(data_file):
    with open(data_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "handle", "followers", "following", "posts", "account_life_days",
            "engagement_rate", "bio_length", "contact_info", "website",
            "comments_status", "comment_type", "method_payment", "customer_tags",
            "follower_following_ratio"
        ])

# Create reports.csv if it doesn’t exist
if not os.path.exists(report_file):
    with open(report_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["handle", "user_experience", "proof_filename"])

# Load data
df = pd.read_csv(data_file)
reports_df = pd.read_csv(report_file)

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

# --------------------------- FRONTEND SECTION ----------------------------

st.image("logo.svg", width=100)
st.title("ScamSniff")
st.subheader("Sniffs out scam pages, protecting users from Instagram scams.")
st.write("Ensures safe online shopping by analyzing and verifying Instagram shopping pages before you buy.")

st.write("---")
handle = st.text_input("Enter Instagram Page Name")

# --------------------------- SITUATION 1: Handle Found ----------------------------
if handle:
    if handle in df["handle"].values:
        st.success(f"Handle '{handle}' found in our dataset.")
        row = df[df["handle"] == handle].iloc[0]

        st.write("### Page Details")
        st.write(f"**Follower/Following Ratio:** {row['follower_following_ratio']}")
        st.write(f"**Number of Posts:** {row['posts']}")
        st.write(f"**Account Life (Days):** {row['account_life_days']}")
        st.write(f"**Engagement Rate:** {row['engagement_rate']}")
        st.write(f"**Contact Info Available:** {row['contact_info']}")
        st.write(f"**Website Link Available:** {row['website']}")
        st.write(f"**Comments Status:** {row['comments_status']}")
        if row['comments_status'].upper() == "ON":
            st.write(f"**Comment Type:** {row['comment_type']}")
        else:
            st.write("**Comment Type:** NULL (Comments are OFF)")
        st.write(f"**Method of Payment:** {row['method_payment']}")
        st.write(f"**Tagged by Customers:** {row['customer_tags']}")

        if st.button("Detect Scam"):
            contact = row["contact_info"].upper()
            website = row["website"].upper()
            comments_status = row["comments_status"].upper()
            payment = row["method_payment"].upper()
            tags = row["customer_tags"].upper()

            scam_flag = (contact == "NO" and website == "NO" and comments_status == "OFF" and payment in ["PREPAY", "ADVPAY"])

            if scam_flag:
                st.error("⚠️ This page is DEFINITELY A SCAMMER.")
                st.write("Reasons:")
                st.write("- No contact information provided.")
                st.write("- No website link available.")
                st.write("- Comments are OFF (no user feedback).")
                st.write("- Payment method is risky (Advance or Prepay).")
                st.write("Confidence Score: **95%**")

                # NEW FEATURE: Check reports
                reported = reports_df[reports_df["handle"].str.lower() == handle.lower()]
                if not reported.empty:
                    st.markdown("---")
                    st.markdown(f"### 🚨 User Reports for {handle}")
                    st.markdown(
                        f"**{len(reported)} report(s)** found against this page, confirming it is **highly likely a scam.**"
                    )
                    for idx, rpt in reported.iterrows():
                        st.markdown(
                            f"<div style='background-color:#3C5B75; padding:10px; border-radius:10px; margin:5px 0;'>"
                            f"<strong>🧾 User Review {idx+1}:</strong><br>{rpt['user_experience']}</div>",
                            unsafe_allow_html=True
                        )
            else:
                st.success("✅ This page appears GENUINE based on available data.")
                st.write("Confidence Score: **80%**")

# --------------------------- SITUATION 2: Handle Not Found ----------------------------
    else:
        st.warning(f"Handle '{handle}' not found. Please enter details manually:")

        followers = st.number_input("Number of Followers", min_value=0)
        following = st.number_input("Number of Following", min_value=0)
        posts = st.number_input("Number of Posts", min_value=0)
        account_life = st.number_input("Account Life (days)", min_value=0)
        contact = st.selectbox("Contact Info Available?", ["YES", "NO"])
        website = st.selectbox("Website Link Available?", ["YES", "NO"])
        comments = st.selectbox("Comments Status", ["ON", "OFF"])
        tags = st.selectbox("Tagged by Customers?", ["YES", "NO"])
        payment = st.selectbox("Method of Payment", ["COD", "PREPAY", "ADVPAY"])

        follower_following_ratio = followers / (following + 1) if following >= 0 else 0
        engagement_rate = (posts + followers * 0.001) / (followers + 1) if followers > 0 else 0

        st.write("### Derived Features")
        st.info(f"Follower/Following Ratio: {follower_following_ratio:.2f}")
        st.info(f"Approx. Engagement Rate: {engagement_rate:.4f}")

        if st.button("Detect Scam"):
            scam_flag = (contact == "NO" and website == "NO" and comments == "OFF" and payment in ["PREPAY", "ADVPAY"])
            if scam_flag:
                st.error("⚠️ This handle is DEFINITELY A SCAMMER.")
                st.write("Reasons:")
                st.write("- No contact info or website available.")
                st.write("- Comments are disabled (no user feedback).")
                st.write("- Payment method is risky (Advance or Prepay).")
                st.write("Confidence Score: **95%**")

                # Check if there are existing user reports
                reported = reports_df[reports_df["handle"].str.lower() == handle.lower()]
                if not reported.empty:
                    st.markdown("---")
                    st.markdown(f"### 🚨 User Reports for {handle}")
                    st.markdown(
                        f"**{len(reported)} report(s)** found against this page, confirming it is **highly likely a scam.**"
                    )
                    for idx, rpt in reported.iterrows():
                        st.markdown(
                            f"<div style='background-color:#003366; padding:10px; border-radius:10px; margin:5px 0;'>"
                            f"<strong>🧾 User Review {idx+1}:</strong><br>{rpt['user_experience']}</div>",
                            unsafe_allow_html=True
                        )
            else:
                st.success("✅ This page appears GENUINE based on user inputs.")
                st.write("Confidence Score: **80%**")

# --- REPORT A SCAM SECTION ---
st.write("---")
st.header("📢 Report a Scam")

report_handle = st.text_input("Enter the Instagram Page Name to Report")
user_id = st.text_input("Your email or username (private, only to avoid duplicate reports)", key="user_id")
report_experience = st.text_area("Describe your experience")
proof = st.file_uploader("Upload Proof (optional: image/pdf)", type=['png', 'jpg', 'jpeg', 'pdf'])

if st.button("Submit Report"):
    if not report_handle or not user_id or not report_experience:
        st.error("Please provide handle, your email/username, and a description.")
    else:
        found_duplicate = False
        # Check for duplicates: same user_id + handle
        if not reports_df.empty:
            found_duplicate = (
                (reports_df["handle"].str.lower() == report_handle.lower())
                & (reports_df["user_id"].str.lower() == user_id.lower())
            ).any()
        if found_duplicate:
            st.error("You have already submitted a report for this handle. One report per handle per user is allowed.")
        else:
            with open(report_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    report_handle,
                    user_id,
                    report_experience,
                    proof.name if proof else "None"
                ])
            st.success("✅ Your report has been successfully submitted!")


# End
st.markdown("---")
st.caption("© 2025 ScamSniff | Built with ❤ for Safer Online Shopping.")