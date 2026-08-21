from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = APP_DIR / "model.joblib"
METRICS_PATH = APP_DIR / "model_metrics.json"
DATA_PATH = APP_DIR / "ai_student_impact_dataset.csv"

st.set_page_config(
    page_title="Student 🎓 GPA AI Impact Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        st.error("The trained model is missing. Run `python train_model.py` first.")
        st.stop()
    return joblib.load(MODEL_PATH)

@st.cache_data
def load_metrics():
    if METRICS_PATH.exists():
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    return {}

model = load_model()
metrics = load_metrics()

st.title("🎓 Student GPA · AI Impact Predictor")
st.caption("A machine-learning estimate of post-semester GPA based on academic, study, and GenAI-usage features.")

with st.sidebar:
    st.header("About")
    st.write(
        "This version runs the trained model locally inside Streamlit. "
        "It no longer depends on an Azure ML endpoint or API key."
    )
    if metrics:
        st.divider()
        st.subheader("Model validation")
        st.metric("R²", f"{metrics.get('r2', 0):.3f}")
        st.metric("MAE", f"{metrics.get('mae', 0):.3f}")
        st.caption("Validation metrics are estimates on a held-out test set; they are not a guarantee for an individual student.")

st.info(
    "Educational tool only: the prediction is an estimate, not an official academic decision, "
    "admission decision, or guarantee of future GPA."
)

st.subheader("Student profile")
col1, col2, col3 = st.columns(3)

with col1:
    major = st.selectbox("🎓 Major", ["Humanities", "Medical", "Business", "STEM", "Arts"])
    year = st.selectbox("📚 Year of study", ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"])
    pre_gpa = st.number_input("📈 Pre-semester GPA", 0.0, 4.0, 3.0, 0.01)
    traditional_hours = st.number_input("📖 Traditional study hours / week", 0.0, 100.0, 10.0, 0.5)

with col2:
    genai_hours = st.number_input("🤖 GenAI hours / week", 0.0, 100.0, 5.0, 0.5)
    use_case = st.selectbox(
        "🛠️ Primary GenAI use case",
        ["Copywriting/Drafting", "Ideation", "Summarizing_Reading",
         "Debugging/Troubleshooting", "Direct_Answer_Generation"],
    )
    prompt_skill = st.selectbox("🧠 Prompt-engineering skill", ["Beginner", "Intermediate", "Advanced"])
    tool_diversity = st.slider("🧩 GenAI tool diversity", 1, 5, 2)

with col3:
    paid = st.selectbox("💳 Paid GenAI subscription", ["No", "Yes"])
    ai_dependency = st.slider("🔗 Perceived AI dependency", 1, 10, 5)
    policy = st.selectbox(
        "🏫 Institutional GenAI policy",
        ["Strict_Ban", "Allowed_With_Citation", "Actively_Encouraged"],
    )
    anxiety = st.slider("😰 Exam anxiety", 1, 10, 5)

def make_features():
    return pd.DataFrame([{
        "Major_Category": major,
        "Year_of_Study": year,
        "Pre_Semester_GPA": pre_gpa,
        "Weekly_GenAI_Hours": genai_hours,
        "Primary_Use_Case": use_case,
        "Prompt_Engineering_Skill": prompt_skill,
        "Tool_Diversity": tool_diversity,
        "Paid_Subscription": paid == "Yes",
        "Traditional_Study_Hours": traditional_hours,
        "Perceived_AI_Dependency": ai_dependency,
        "Institutional_Policy": policy,
        "Anxiety_Level_During_Exams": anxiety,
    }])

def coach_text(prediction):
    messages = []
    if pre_gpa < 2.5:
        messages.append("Your starting GPA is the strongest area to focus on; consistent foundational study is important.")
    if traditional_hours < 8:
        messages.append("Consider increasing traditional study time gradually, especially before exams.")
    if genai_hours > traditional_hours:
        messages.append("Your GenAI use exceeds your traditional study time. Use AI as a learning aid rather than a replacement for practice.")
    if ai_dependency >= 8:
        messages.append("High AI dependency can be risky academically. Try solving problems independently before checking AI.")
    if anxiety >= 8:
        messages.append("High exam anxiety may make preparation and practice tests especially valuable.")
    if not messages:
        messages.append("Your profile is relatively balanced. Keep monitoring your study habits and use GenAI to reinforce learning.")
    messages.append(f"The model estimates a post-semester GPA of about {prediction:.2f}.")
    return messages

if st.button("🔮 Predict Post-Semester GPA", type="primary", use_container_width=True):
    features_df = make_features()
    prediction = float(np.clip(model.predict(features_df)[0], 0.0, 4.0))

    st.divider()
    a, b, c = st.columns(3)
    with a:
        st.metric("Predicted Post-Semester GPA", f"{prediction:.2f} / 4.00")
    with b:
        change = prediction - pre_gpa
        st.metric("Estimated change vs. starting GPA", f"{change:+.2f}")
    with c:
        if prediction >= 3.5:
            band = "Strong"
        elif prediction >= 3.0:
            band = "Moderate"
        else:
            band = "Needs attention"
        st.metric("Prediction band", band)

    st.subheader("🤖 AI Study Coach")
    for msg in coach_text(prediction):
        st.write("• " + msg)

    st.caption(
        "The coach provides general educational guidance from the entered profile. "
        "It does not diagnose students or make institutional decisions."
    )

st.divider()
st.caption("Built with Streamlit + scikit-learn. No Azure ML endpoint is required.")
