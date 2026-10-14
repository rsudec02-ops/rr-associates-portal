import streamlit as st
import os
import csv
import sqlite3
import pandas as pd
from datetime import datetime

# --- Day 11: Enterprise Industrial UI & Custom CSS Customizations ---
st.set_page_config(
    page_title="RR Associate | Operational Telemetry Portal", 
    page_icon="🏭", 
    layout="wide"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

        /* Hide Streamlit default chrome */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Ultra-Premium Industrial Dark Canvas */
        .stApp {
            background: radial-gradient(circle at top right, #0F172A, #090D16) !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            color: #F8FAFC !important;
        }

        /* High-Tech Corporate Watermark */
        .stApp::before {
            content: "RR ASSOCIATE";
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-25deg);
            font-size: 110px;
            font-weight: 900;
            color: rgba(255, 255, 255, 0.02);
            white-space: nowrap;
            pointer-events: none;
            z-index: 0;
            letter-spacing: 12px;
        }

        /* Typography Override for Ultra High Contrast */
        h1, h2, h3, h4, label, p, span { 
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            color: #F8FAFC !important;
        }

        /* Glassmorphism Card Containers */
        div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] {
            background: rgba(15, 23, 42, 0.75) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-top: 3px solid #38BDF8 !important;
            border-radius: 16px !important;
            padding: 24px !important;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5) !important;
            margin-bottom: 16px !important;
        }

        /* Executive Telemetry KPI Cards */
        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
            border: 1px solid rgba(56, 189, 248, 0.2) !important;
            border-left: 5px solid #38BDF8 !important;
            border-radius: 12px !important;
            padding: 18px 22px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3) !important;
        }

        div[data-testid="stMetricValue"] {
            font-size: 32px !important;
            color: #38BDF8 !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
        }

        div[data-testid="stMetricLabel"] {
            font-size: 13px !important;
            color: #94A3B8 !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }

        /* Industrial Glowing Action Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
            color: #FFFFFF !important;
            font-size: 17px !important;
            font-weight: 700 !important;
            height: 54px !important;
            width: 100% !important;
            border-radius: 10px !important;
            border: 1px solid #38BDF8 !important;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.3) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            letter-spacing: 0.5px !important;
        }

        .stButton>button:hover {
            background: linear-gradient(135deg, #38BDF8 0%, #0284C7 100%) !important;
            box-shadow: 0 0 30px rgba(56, 189, 248, 0.6) !important;
            transform: translateY(-2px) !important;
            color: #FFFFFF !important;
        }

        /* Form Inputs & Selectboxes Styling */
        div[data-baseweb="select"] > div, input {
            background-color: #1E293B !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            color: #F8FAFC !important;
            border-radius: 8px !important;
        }
        
        div[data-baseweb="select"] span {
            color: #F8FAFC !important;
        }

        /* Styled Telemetry Data Table */
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            overflow: hidden !important;
        }
    </style>
""", unsafe_allow_html=True)
# --- Day 12: Relational SQLite Database Engine (RR Associate ERP) ---
def init_db():
    """Creates the relational attendance schema with GIS telemetry columns."""
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            worker_name TEXT NOT NULL,
            shift_type TEXT NOT NULL,
            location TEXT NOT NULL,
            status TEXT NOT NULL,
            duration REAL DEFAULT 0.0,
            verification TEXT DEFAULT 'Pending',
            lat REAL DEFAULT 28.0588,
            lon REAL DEFAULT 77.9469
        )
    """)
    conn.commit()
    conn.close()

# Auto-initialize SQLite database engine on load
init_db()
# --- Corporate Header Banner with Logo & Watermark Support ---
col_logo, col_header = st.columns([1, 5])

with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    else:
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
                color: #F59E0B;
                padding: 20px;
                border-radius: 14px;
                text-align: center;
                font-weight: 800;
                font-size: 24px;
                border: 2px solid #F59E0B;
                box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5);
            ">
                🏗️ RR
            </div>
        """, unsafe_allow_html=True)

with col_header:
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            padding: 20px 28px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-bottom: 4px solid #F59E0B;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div>
                <div style="display: flex; align-items: center; gap: 12px;">
                    <h1 style="
                        color: #FFFFFF !important; 
                        margin: 0; 
                        font-size: 30px; 
                        font-weight: 800; 
                        letter-spacing: -0.5px;
                    ">
                        RR ASSOCIATE
                    </h1>
                    <span style="
                        background: rgba(245, 158, 11, 0.2); 
                        color: #F59E0B; 
                        border: 1px solid #F59E0B; 
                        padding: 3px 10px; 
                        border-radius: 20px; 
                        font-size: 11px; 
                        font-weight: 700;
                        letter-spacing: 1px;
                    ">
                        ENTERPRISE
                    </span>
                </div>
                <p style="
                    color: #38BDF8 !important; 
                    margin: 6px 0 0 0; 
                    font-size: 15px; 
                    font-weight: 600;
                ">
                    ⚡ Operational Telemetry & Field Force Command Portal | 📍 Wonder Cement (Aligarh Unit)
                </p>
            </div>
            <div style="text-align: right;">
                <div style="color: #10B981; font-weight: 700; font-size: 13px; display: flex; align-items: center; gap: 6px; justify-content: flex-end;">
                    <span style="height: 8px; width: 8px; background-color: #10B981; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #10B981;"></span>
                    SYSTEM ONLINE
                </div>
                <div style="color: #64748B; font-size: 11px; margin-top: 4px; font-weight: 600;">
                    SECURE TELEMETRY LINK
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
st.divider()
# --- Top Navigation Bar ---
st.title("🏗️ RR Associates Portal")
st.caption("Industrial Operations System • Wonder Cement Sites")

col_lang, col_role = st.columns([1, 2])
with col_lang:
    lang = st.radio("Language / भाषा", ["English", "हिन्दी"])
with col_role:
    user_role = st.selectbox(
        "Select Profile / प्रोफाइल चुनें",
        ["👤 Worker / श्रमिक", "👔 Supervisor / पर्यवेक्षक", "🔑 Admin (Me) / एडमिन"]
    )

# --- Secure Role Authentication Gate ---
authenticated = True  # Default for workers

if "Supervisor" in user_role:
    sup_pin = st.sidebar.text_input("Enter Supervisor PIN:", type="password")
    if sup_pin != "RRSuper2026":
        authenticated = False
        st.sidebar.error("❌ Invalid Supervisor PIN")
        st.warning("⚠️ Please enter the authorized Supervisor PIN in the sidebar to access the Control Desk.")

elif "Admin" in user_role:
    admin_pin = st.sidebar.text_input("Enter Admin Master Key:", type="password")
    if admin_pin != "RRAdmin2026!":
        authenticated = False
        st.sidebar.error("❌ Access Denied: Invalid Master Key")
        st.warning("🔒 **RESTRICTED AREA:** Enter the secure Admin Master Key in the sidebar to view executive operations and analytics.")
# Place this near the top under your role/language selectors
system_status = st.sidebar.toggle("Portal Active (Allow Worker Clock-ins)", value=True)
st.divider()
# --- Worker Input Fields ---
worker_name = st.text_input("Enter Worker Name / श्रमिक का नाम दर्ज करें")
shift_type = st.selectbox("Select Shift Type / शिफ्ट का प्रकार", ["Day / दिन", "Night / रात"])
location_tag = st.selectbox("Select Site Location / साइट का स्थान", ["Wagon Tippler", "Wonder Cement Ltd"])
location_verified = False
# ==========================================
# UNIFIED USER ROLE ROUTING (Zero-Error Chain)
# ==========================================

if "Worker" in user_role:
    # --- Worker Terminal ---
    if not system_status:
        st.warning("⚠️ SYSTEM MAINTENANCE MODE: The worker terminal is currently locked by the administrator.")
    else:
        if lang == "English":
            st.header("Worker Terminal")
            st.info("Welcome to your daily shift terminal.")
            st.subheader("📍 Location Verification")
            gps_lat = st.number_input("Target Latitude (Aligarh Unit: 28.XXXX)", value=28.0588, format="%.4f")
            gps_lon = st.number_input("Target Longitude (Aligarh Unit: 77.XXXX)", value=77.9469, format="%.4f")
            
            if (27.9 <= gps_lat <= 28.2) and (77.8 <= gps_lon <= 78.1):
                st.success("✅ GPS Location Verified: Inside Wonder Cement Aligarh Site Boundary.")
                location_verified = True
            else:
                st.error("❌ Access Denied: You must be physically present at the Aligarh Facility.")
                location_verified = False

            if not os.path.exists("attendance.csv"):
                with open("attendance.csv", "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Timestamp", "Worker Name", "Shift Type", "Location", "Status"])

            if st.button("Mark Shift Clock-In"):
                if not location_verified:
                    st.error("Cannot clock in. GPS verification failed.")
                elif worker_name.strip() == "":
                    st.error("Please enter a worker name before clocking in.")
                else:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    current_hour = datetime.now().hour
                    current_minute = datetime.now().minute
                    
                    arrival_status = "On Time"
                    if current_hour > 8 or (current_hour == 8 and current_minute > 15):
                        arrival_status = "Late Arrival"
                    
                    # Commit record directly to SQLite database
                    # Commit record with GIS telemetry directly to SQLite database
                    conn = sqlite3.connect("attendance.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO attendance (timestamp, worker_name, shift_type, location, status, duration, verification, lat, lon)
                        VALUES (?, ?, ?, ?, ?, 0.0, 'Pending', ?, ?)
                    """, (current_time, worker_name, shift_type, location_tag, arrival_status, gps_lat, gps_lon))
                    conn.commit()
                    conn.close()

                    st.success(f"✅ Transaction Authenticated | Employee: {worker_name} | Status: [{arrival_status}] | GPS Tagged.")
elif "Supervisor" in user_role:
    if authenticated:
        st.header("Supervisor Control Desk")
        st.write("Manage field crews, machinery checkpoints, and site metrics.")
    # --- Supervisor Control Desk ---
    st.header("Supervisor Control Desk")
    st.write("Manage field crews, machinery checkpoints, and site metrics.")
    
    st.markdown("### 📋 Supervisor Audit & Telemetry Verification Queue")
    conn = sqlite3.connect("attendance.db")
    df = pd.read_sql_query("SELECT * FROM attendance ORDER BY id DESC", conn)
    conn.close()

    if df.empty:
        st.info("No worker telemetry records found in the database.")
    else:
        st.dataframe(df, use_container_width=True)
        st.markdown("---")
        st.markdown("#### ⚙️ Execute Audit Certification")
        
        pending_records = df[df["verification"] == "Pending"]
        
        if not pending_records.empty:
            record_ids = pending_records["id"].tolist()
            selected_id = st.selectbox("Select Record ID to Certify/Audit:", record_ids)
            
            col_app, col_rej = st.columns(2)
            
            with col_app:
                if st.button("✅ Approve Record"):
                    conn = sqlite3.connect("attendance.db")
                    cursor = conn.cursor()
                    cursor.execute("UPDATE attendance SET verification = 'Approved' WHERE id = ?", (selected_id,))
                    conn.commit()
                    conn.close()
                    st.success(f"Record #{selected_id} officially certified!")
                    st.rerun()
                    
            with col_rej:
                if st.button("❌ Reject Record"):
                    conn = sqlite3.connect("attendance.db")
                    cursor = conn.cursor()
                    cursor.execute("UPDATE attendance SET verification = 'Rejected' WHERE id = ?", (selected_id,))
                    conn.commit()
                    conn.close()
                    st.error(f"Record #{selected_id} flagged and rejected.")
                    st.rerun()
        else:
            st.success("🎉 All operational records are fully audited and certified!")

elif "Admin" in user_role:
    if authenticated:
        st.header("🏢 Admin Operations & Analytics Portal")
        st.write("Executive summary, site metrics, and data export control.")
    conn = sqlite3.connect("attendance.db")
    df_admin = pd.read_sql_query("SELECT * FROM attendance ORDER BY id DESC", conn)
    conn.close()

    if df_admin.empty:
        st.info("No attendance telemetry recorded yet in SQLite database.")
    else:
        # --- Operational KPI Cards ---
        st.markdown("### 📈 Core Operational Metrics")
        m1, m2, m3, m4 = st.columns(4)
        
        total_logs = len(df_admin)
        pending_logs = len(df_admin[df_admin["verification"] == "Pending"])
        approved_logs = len(df_admin[df_admin["verification"] == "Approved"])
        rejected_logs = len(df_admin[df_admin["verification"] == "Rejected"])

        m1.metric("Total Clock-Ins", total_logs)
        m2.metric("Pending Audits", pending_logs)
        m3.metric("Approved Logs", approved_logs)
        m4.metric("Flagged/Rejected", rejected_logs)

        st.markdown("---")
        st.markdown("### 📋 Master Database Overview")
        st.dataframe(df_admin, use_container_width=True)

        # ==========================================
        # PASTE STEP 3 GIS MAP MODULE RIGHT HERE:
        # ==========================================
        st.markdown("---")
        st.markdown("### 🗺️ Live GIS Satellite Tracking & Geofence Map")
        st.write("Visualizing active workforce check-in coordinates around the Wonder Cement Aligarh Facility.")
        
        if "lat" in df_admin.columns and "lon" in df_admin.columns:
            st.map(df_admin, latitude="lat", longitude="lon", zoom=12, use_container_width=True)
        else:
            st.info("GIS coordinate columns pending synchronization.")
        # ==========================================
        # --- Advanced Shift Analytics & Visual Trends ---
        st.markdown("---")
        st.markdown("### 📊 Advanced Workforce Analytics & Performance Trends")
        st.write("Visualizing real-time attendance behavior, punctuality, and shift distribution.")

        if not df_admin.empty and "status" in df_admin.columns:
            col_chart1, col_chart2 = st.columns(2)

            with col_chart1:
                st.markdown("#### 🕒 Punctuality Breakdown (On-Time vs. Late)")
                status_counts = df_admin["status"].value_counts()
                st.bar_chart(status_counts)

            with col_chart2:
                st.markdown("#### 🔄 Shift Type Distribution")
                if "shift_type" in df_admin.columns:
                    shift_counts = df_admin["shift_type"].value_counts()
                    st.bar_chart(shift_counts)
                else:
                    st.info("Shift type telemetry data unavailable.")
        else:
            st.info("Insufficient data to render telemetry analytics charts.")

        # --- CSV Data Exporter ---
        st.markdown("---")
        st.markdown("#### 📥 Export Operational Telemetry Data")
        csv_data = df_admin.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📄 Export Master Attendance Logs (CSV)",
            data=csv_data,
            file_name=f"rr_associate_attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

