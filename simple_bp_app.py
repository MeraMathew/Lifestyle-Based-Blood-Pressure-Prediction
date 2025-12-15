import streamlit as st
import pandas as pd
import joblib
import base64

# -------------------------------------------------------
#  PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(page_title="Blood Pressure Prediction", layout="centered")

# -------------------------------------------------------
#  BACKGROUND IMAGE
# -------------------------------------------------------
def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
                          url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .glass-card {{
        background: rgba(255, 255, 255, 0.18);
        padding: 24px;
        border-radius: 14px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.25);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_bg("Pressure.jpg")

# -------------------------------------------------------
#  GLOBAL CSS (CLEAN & SAFE)
# -------------------------------------------------------
st.markdown("""
<style>

/* Global text (white) */
html, body, [class*="st-"], .stMarkdown, .stMarkdown p,
h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

/* Labels */
label {
    color: white !important;
    font-weight: 600 !important;
}

/* Inputs */
input[type="number"], input[type="text"] {
    color: black !important;
    background-color: rgba(255,255,255,0.95) !important;
    border-radius: 6px !important;
}

/* Selectboxes */
.stSelectbox div[data-baseweb="select"] * {
    color: black !important;
}
.stSelectbox div[role="listbox"] div {
    color: black !important;
}

/* Dataframe headers */
thead th {
    color: white !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    color: black !important;
}
[data-testid="stMetricLabel"] {
    color: #222 !important;
}

/* Primary CTA Button */
[data-testid="stButton"] button,
[data-testid="stButton"] button * {
    color: black !important;
    background-color: rgba(255,255,255,0.95) !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    padding: 0.6em 1.8em !important;
    border-radius: 10px !important;
    min-height: 52px !important;
}

[data-testid="stButton"] button:hover,
[data-testid="stButton"] button:hover * {
    background-color: white !important;
    color: black !important;
}
/* -------------------------------------------------------
   RESULT METRIC BOXES
------------------------------------------------------- */
.metric-box {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

.metric-value {
    font-size: 32px;
    font-weight: 700;
    color: black;
}

.metric-label {
    font-size: 14px;
    font-weight: 600;
    color: #444;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
#  LOAD MODELS
# -------------------------------------------------------
rf_sys = joblib.load("rf_systolic.pkl")
rf_dia = joblib.load("rf_diastolic.pkl")

# -------------------------------------------------------
#  SESSION STATE INIT
# -------------------------------------------------------
if "sys_pred" not in st.session_state:
    st.session_state.sys_pred = None
    st.session_state.dia_pred = None

# -------------------------------------------------------
#  TITLE
# -------------------------------------------------------
st.markdown("<h1 style='text-align:center;'>🩺 Blood Pressure Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Machine Learning–powered health screening</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------
#  INPUT CARD
# -------------------------------------------------------
with st.container():
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("Patient & Lifestyle Inputs")

    pulse = st.number_input("Pulse Rate (beats/min)", 40, 130, 72)
    age = st.number_input("Age (years)", 18, 90, 40)
    weight = st.number_input("Weight (kg)", 35.0, 180.0, 70.0)
    height = st.number_input("Height (cm)", 130.0, 210.0, 170.0)
    sodium = st.number_input("Sodium Intake (mg/day)", 400, 7000, 2500)
    potassium = st.number_input("Potassium Intake (mg/day)", 400, 7000, 3000)
    calories = st.number_input("Daily Calories (kcal)", 800, 4500, 2200)
    drinks = st.number_input("Drinks per Day (0–10)", 0.0, 10.0, 0.0)

    gender = st.selectbox("Gender", ["Male", "Female"])
    race = st.selectbox("Race / Ethnicity", ["White", "Black", "Hispanic", "Asian", "Other"])
    ever_smoked = st.selectbox("Ever Smoked 100+ Cigarettes?", ["Yes", "No"])
    current_smoking = st.selectbox(
        "Current Smoking Status",
        ["Current Smoker", "Former Smoker", "Never Smoked"]
    )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
#  PREPARE INPUT DATA
# -------------------------------------------------------
input_data = pd.DataFrame([{
    "Pulse_Rate": pulse,
    "Age_Years": age,
    "Gender": gender,
    "Race_Ethnicity": race,
    "Weight_kg": weight,
    "Height_cm": height,
    "Sodium_mg": sodium,
    "Potassium_mg": potassium,
    "Calories_kcal": calories,
    "Ever_Smoked_100_Cigs": ever_smoked,
    "Current_Smoking_Status": current_smoking,
    "Drinks_Per_Day": drinks
}])

# -------------------------------------------------------
#  CENTERED BUTTON
# -------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🔍 Predict Blood Pressure"):
        st.session_state.sys_pred = rf_sys.predict(input_data)[0]
        st.session_state.dia_pred = rf_dia.predict(input_data)[0]

# -------------------------------------------------------
#  RESULTS
# -------------------------------------------------------
# -------------------------------------------------------
#  RESULTS
# -------------------------------------------------------
if st.session_state.sys_pred is not None:
    sys_pred = st.session_state.sys_pred
    dia_pred = st.session_state.dia_pred

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("Prediction Results")

    # ✅ DEFINE COLUMNS FIRST
    c1, c2 = st.columns(2)

    # ✅ SYSTOLIC BOX
    with c1:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Systolic BP</div>
                <div class="metric-value">{sys_pred:.1f} mmHg</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ✅ DIASTOLIC BOX
    with c2:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Diastolic BP</div>
                <div class="metric-value">{dia_pred:.1f} mmHg</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------------------------------------------
    #  RISK CATEGORY (NOW GUARANTEED TO RUN)
    # ---------------------------------------------------
    if sys_pred < 120 and dia_pred < 80:
        cat, color = "Normal", "#4CAF50"
    elif sys_pred < 130 and dia_pred < 80:
        cat, color = "Elevated", "#FFC107"
    elif sys_pred < 140 or dia_pred < 90:
        cat, color = "Stage 1 Hypertension", "#FF5722"
    else:
        cat, color = "Stage 2 Hypertension", "#D32F2F"

    st.markdown(
        f"<h3 style='text-align:center; margin-top:20px; color:{color};'>"
        f"Risk Category: {cat}</h3>",
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------------
#  FOOTER
# -------------------------------------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("⚠️ This tool is for health awareness and screening only. Not for diagnosis.")
