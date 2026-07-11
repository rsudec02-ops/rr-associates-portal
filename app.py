import streamlit as st
import datetime

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

# =====================================================================
# SYSTEM PROFILE INTERFACES (Day 1 Shells)
# =====================================================================

if "Worker" in user_role:
    if lang == "English":
        st.header("Worker Terminal")
        st.info("Welcome to your daily shift terminal. Follow safety protocols.")
        if st.button("⏱️ MARK SHIFT CLOCK-IN"):
            st.success(f"System Logged Attendance at {datetime.datetime.now().strftime('%H:%M:%S')}")
    else:
        st.header("श्रमिक टर्मिनल")
        st.info("आपके दैनिक शिफ्ट टर्मिनल में आपका स्वागत है। सुरक्षा नियमों का पालन करें।")
        if st.button("⏱️ उपस्थिति दर्ज करें (क्लॉक इन)"):
            st.success(f"उपस्थिति दर्ज की गई: {datetime.datetime.now().strftime('%H:%M:%S')}")

elif "Supervisor" in user_role:
    st.header("Supervisor Control Desk")
    st.write("Manage field crews, machinery checkpoints, and alert channels.")
    st.text_input("Enter Active Shift ID", placeholder="e.g., WONDER-SHIFT-A")
    if st.button("💾 SAVE SHIFT METRICS"):
        st.success("Log basic details stored safely.")

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
    