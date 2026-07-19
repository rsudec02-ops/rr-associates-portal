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
# Place this near the top under your role/language selectors
system_status = st.sidebar.toggle("Portal Active (Allow Worker Clock-ins)", value=True)
st.divider()
# --- Worker Input Fields ---
worker_name = st.text_input("Enter Worker Name / श्रमिक का नाम दर्ज करें")
shift_type = st.selectbox("Select Shift Type / शिफ्ट का प्रकार", ["Day / दिन", "Night / रात"])
location_tag = st.selectbox("Select Site Location / साइट का स्थान", ["Wagon Tippler", "Wonder Cement Ltd"])

# =====================================================================
# SYSTEM PROFILE INTERFACES (Day 1 Shells)
# =====================================================================
if "Worker" in user_role:
    if not system_status:
        st.warning("⚠️ SYSTEM MAINTENANCE MODE: The worker terminal is currently locked by the administrator. Please try again later.")
    else:
        if lang == "English":
            st.header("Worker Terminal")
            st.info("Welcome to your daily shift terminal.")
            # Simulated GPS Device Check (Aligarh Grinding Unit)
            st.subheader("📍 Location Verification")
            gps_lat = st.number_input("Target Latitude (Aligarh Unit: 28.XXXX)", value=28.0588, format="%.4f")
            gps_lon = st.number_input("Target Longitude (Aligarh Unit: 77.XXXX)", value=77.9469, format="%.4f")
            
            # Check if the worker is within the boundary limits of the Aligarh Unit
            if (27.9 <= gps_lat <= 28.2) and (77.8 <= gps_lon <= 78.1):
                st.success("✅ GPS Location Verified: Inside Wonder Cement Aligarh Site Boundary.")
                location_verified = True
            else:
                st.error("❌ Access Denied: You must be physically present at the Aligarh Facility.")
                location_verified = False
            # Check if the database file exists; if not, create it
            if not os.path.exists("attendance.csv"):
                with open("attendance.csv", "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Timestamp", "Worker Name", "Shift Type", "Location"])

            # Interactive button logic
            if st.button("Mark Shift Clock-In"):
                if not location_verified:
                    st.error("Cannot clock in. GPS verification failed.")
                elif worker_name.strip() == "":
                    st.error("Please enter a worker name before clocking in.")
                else:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open("attendance.csv", "a", newline="", encoding="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow([current_time, worker_name, shift_type, location_tag])
                    st.success(f"Shift successfully logged for {worker_name} at {current_time}!")
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

        # --- Live Shift Charts Panel ---
        st.markdown("### 📊 Live Shift Trends")
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.markdown("**📌 Shifts Logged by Location**")
            if "Location" in df.columns:
                location_counts = df["Location"].value_counts()
                st.bar_chart(location_counts)
            else:
                st.info("No location data found yet.")

        with col_chart2:
            st.markdown("**⏰ Shift Type Breakdown**")
            if "Shift Type" in df.columns:
                shift_counts = df["Shift Type"].value_counts()
                st.bar_chart(shift_counts)
            else:
                st.info("No shift type data found yet.")
        # --- Live Data Table ---
        st.subheader("📋 Live Attendance Logs")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No attendance records found yet. Data will appear once workers clock in.")
elif "Admin" in user_role:
    st.header("Executive Admin Control Center")
    st.write("System-wide configurations, database overrides, and portal security.")

    st.subheader("⚙️ System Operational Status")
    if system_status:
        st.success("System Status: OPERATIONAL. Workers can log shifts normally.")
    else:
        st.warning("System Status: MAINTENANCE MODE. Worker terminals are locked.")

    st.divider()

    # --- Database File Manager Panel ---
    st.subheader("📁 System Database Overview")
    if os.path.exists("attendance.csv"):
        import pandas as pd
        df = pd.read_csv("attendance.csv", encoding="utf-8")
        
        st.info(f"Database Integrity: Healthy. Current logs contain {df.shape[0]} rows and {df.shape[1]} columns.")
        
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Master Data Backup (.CSV)",
            data=csv_data,
            file_name="master_attendance_backup.csv",
            mime="text/csv"
        )
    else:
        st.error("System Error: Local database file 'attendance.csv' not detected.")    