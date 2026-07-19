import streamlit as st
from datetime import datetime
import csv
import os

# --- Industrial System Theme UI Customizations ---
st.set_page_config(page_title="RR Associates Portal", page_icon="🏗️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    h1 { color: #0B2545; font-family: 'Arial Black', sans-serif; } /* Navy Blue */
    h2, h3 { color: #0B2545; }
    
    /* Custom Large Buttons for Glove Users / Dusty Screen Environments */
    .stButton>button {
        background-color: #F26419 !important; /* Safety Orange */
        color: white !important;
        font-size: 22px !important;
        font-weight: bold !important;
        height: 65px !important; 
        width: 100% !important;
        border-radius: 10px !important;
        border: 2px solid #D64F0C !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover { background-color: #D64F0C !important; cursor: pointer; }
    
    .card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 8px;
        border-left: 6px solid #0B2545;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Top Navigation Bar ---
st.title("🏗️ RR Associates Portal")
st.caption("Industrial Operations System • Wonder Cement Sites")

col_lang, col_role = st.columns([1, 2])
with col_lang:
    lang = st.radio("Language / भाषा", ["English", "हिन्दी"])

with col_role:
    user_role = st.selectbox(
        "Select Profile / प्रोफ़ाइल चुनें",
        ["👷 Worker / श्रमिक", "📋 Supervisor / पर्यवेक्षक", "🔑 Admin (Me) / एडमिन"]
    )

st.divider()
# --- Worker Input Fields ---
worker_name = st.text_input("Enter Worker Name / श्रमिक का नाम दर्ज करें")
shift_type = st.selectbox("Select Shift Type / शिफ्ट का प्रकार", ["Day / दिन", "Night / रात"])
location_tag = st.selectbox("Select Site Location / साइट का स्थान", ["Wagon Tippler", "Wonder Cement Ltd"])

# =====================================================================
# SYSTEM PROFILE INTERFACES (Day 1 Shells)
# =====================================================================
if "Worker" in user_role:
    if lang == "English":
        st.header("Worker Terminal")
        st.info("Welcome to your daily shift terminal.")

        # Check if the database file exists; if not, create it
        if not os.path.exists("attendance.csv"):
            with open("attendance.csv", "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Worker Name", "Shift Type", "Location"])

        # Interactive button logic
        if st.button("Mark Shift Clock-In"):
            if worker_name.strip() == "":
                st.error("Please enter a worker name before clocking in.")
            else:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open("attendance.csv", "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([current_time, worker_name, shift_type, location_tag])
                st.success(f"Shift successfully logged for {worker_name} at {current_time}!")
elif "Supervisor" in user_role:
    st.header("Supervisor Control Desk")
    st.write("Manage field crews, machinery checkpoints, and site metrics.")

    
    if os.path.exists("attendance.csv"):
        
        import pandas as pd
        df = pd.read_csv("attendance.csv", encoding="utf-8")

        # --- Analytics Metrics ---
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Total Logged Shifts", value=len(df))
        with col2:
            # Counts unique worker names
            unique_workers = df["Worker Name"].nunique() if "Worker Name" in df.columns else 0
            st.metric(label="Unique Personnel on Site", value=unique_workers)

        st.divider()

        # --- Live Data Table ---
        st.subheader("📋 Live Attendance Logs")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No attendance records found yet. Data will appear once workers clock in.")
elif "Admin" in user_role:
    st.header("Executive Control Command")
    st.write("Operational health dashboard for RR Associates management.")
    st.markdown("""
    <div class="card">
        <h4>🏢 Target Client Location</h4>
        <p><b>Primary Site:</b> Wonder Cement Ltd (Wagon Tippler Systems)</p>
        <p><b>Status:</b> System Active</p>
    </div>
    """, unsafe_allow_html=True)
    
    