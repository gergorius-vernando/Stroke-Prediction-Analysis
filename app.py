import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Prediksi Risiko Stroke", page_icon="🏥", layout="centered")

rf_model = joblib.load('models/rf_model.pkl')
log_model = joblib.load('models/log_model.pkl')
scaler = joblib.load('models/scaler.pkl')
FEATURE_COLUMNS = joblib.load('models/feature_columns.pkl')

st.title("Prediksi Risiko Stroke")
st.caption("Demo Model Machine Learning — Random Forest & Logistic Regression")

model_choice = st.radio("Pilih model:", ["Random Forest", "Logistic Regression"], horizontal=True)

st.subheader("Data Pasien")
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Usia (tahun)", 0, 120, 50)
    avg_glucose_level = st.number_input("Rata-rata Glukosa (mg/dL)", 0.0, 400.0, 100.0)
    bmi = st.number_input("BMI", 0.0, 100.0, 25.0)
with col2:
    hypertension = st.selectbox("Hipertensi", ["Tidak", "Ya"])
    heart_disease = st.selectbox("Penyakit Jantung", ["Tidak", "Ya"])
    smoking_status_id = st.selectbox(
        "Status Merokok",
        ["Tidak Diketahui", "Tidak Pernah Merokok", "Mantan Perokok", "Perokok Aktif"]
    )

smoking_map = {
    "Tidak Diketahui": "Unknown",
    "Tidak Pernah Merokok": "never smoked",
    "Mantan Perokok": "formerly smoked",
    "Perokok Aktif": "smokes",
}
smoking_status = smoking_map[smoking_status_id]

if st.button("Prediksi", type="primary"):
    input_data = pd.DataFrame([{
        'age': age,
        'avg_glucose_level': avg_glucose_level,
        'bmi': bmi,
        'hypertension': 1 if hypertension == "Ya" else 0,
        'heart_disease': 1 if heart_disease == "Ya" else 0,
        'smoking_status_formerly smoked': 1 if smoking_status == "formerly smoked" else 0,
        'smoking_status_never smoked': 1 if smoking_status == "never smoked" else 0,
        'smoking_status_smokes': 1 if smoking_status == "smokes" else 0,
    }])[FEATURE_COLUMNS]

    if model_choice == "Random Forest":
        proba = rf_model.predict_proba(input_data)[0, 1]
        threshold = 0.2
    else:
        input_scaled = scaler.transform(input_data)
        proba = log_model.predict_proba(input_scaled)[0, 1]
        threshold = 0.6

    label = "BERISIKO STROKE" if proba >= threshold else "TIDAK BERISIKO"

    st.divider()
    st.metric("Probabilitas Risiko Stroke", f"{proba*100:.1f}%")
    if proba >= threshold:
        st.error(f"⚠️ {label}")
    else:
        st.success(f"✅ {label}")
    st.caption(f"Model: {model_choice}")

st.divider()
st.caption("⚠️ Ini demo akademik, bukan alat diagnosis medis. Precision model tergolong rendah (~17%), hasil positif perlu dikonfirmasi pemeriksaan medis lanjutan.")