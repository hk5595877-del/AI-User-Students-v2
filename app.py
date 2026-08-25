from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from supabase import create_client
# ==========================================
# SUPABASE CONNECTION
# ==========================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# AUTHENTICATION STATE
# ==========================================

if "user" not in st.session_state:
    st.session_state.user = None

if "account_type" not in st.session_state:
    st.session_state.account_type = None

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "home"
    

# ==========================================
# GOOGLE ANALYTICS
# ==========================================
GA_JS = """
export default function(component) {
    if (window.__student_gpa_ga_loaded) {
        return;
    }
    window.__student_gpa_ga_loaded = true;

    const measurementId = "G-BLH8FSGHR1";

    window.dataLayer = window.dataLayer || [];

    window.gtag = function() {
        window.dataLayer.push(arguments);
    };

    window.gtag("js", new Date());
    window.gtag("config", measurementId);

    const script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + measurementId;

    document.head.appendChild(script);
}
"""

ga_component = st.components.v2.component(
    "student_gpa_google_analytics",
    js=GA_JS,
)

ga_component(key="google_analytics")

APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = APP_DIR / "model.joblib"
METRICS_PATH = APP_DIR / "model_metrics.json"
DATA_PATH = APP_DIR / "ai_student_impact_dataset.csv"
# ==========================================
# THEME SETTINGS
# ==========================================

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# ==========================================
# THEME TOGGLE
# ==========================================

theme_col1, theme_col2 = st.columns([8, 1])

with theme_col2:
    if st.session_state.theme == "dark":
        if st.button("☀️", help="Switch to Light Mode"):
            st.session_state.theme = "light"
            st.rerun()
    else:
        if st.button("🌙", help="Switch to Dark Mode"):
            st.session_state.theme = "dark"
            st.rerun()

# ==========================================
# THEME STYLING
# ==========================================

if st.session_state.theme == "dark":

    st.markdown("""
    <style>

    /* Main application */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161B22;
    }

    /* Main text */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }

    p, label, span {
        color: #E6EDF3;
    }

    /* Input fields */
    input,
    textarea {
        background-color: #21262D !important;
        color: #FFFFFF !important;
        border: 1px solid #30363D !important;
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #21262D !important;
        color: #FFFFFF !important;
        border-color: #30363D !important;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 15px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        border: 1px solid #30363D;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
    }

    </style>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <style>

    /* Main application */
    .stApp {
        background-color: #FFFFFF;
        color: #111827;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F3F4F6;
    }

    /* Main text */
    h1, h2, h3, h4, h5, h6 {
        color: #111827 !important;
    }

    p, label, span {
        color: #374151;
    }

    /* Input fields */
    input,
    textarea {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border: 1px solid #D1D5DB !important;
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border-color: #D1D5DB !important;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 15px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        border: 1px solid #D1D5DB;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
    }

    </style>
    """, unsafe_allow_html=True)

    
st.set_page_config(
    page_title="Student 🎓 GPA AI Impact Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)
# ==========================================
# AUTHENTICATION UI
# ==========================================

def show_auth_page():


    st.title("🎓 StudentGPA AI")

    st.subheader(
        "AI-Powered Student GPA & GenAI Impact Predictor"
    )

    st.write(
        "StudentGPA AI uses academic performance, study habits, "
        "GenAI usage, and other student factors to estimate "
        "post-semester GPA and provide personalized study guidance."
    )

    st.info(
        "Create an account to access the GPA prediction system. "
        "Choose the account type that matches you."
    )

    auth_option = st.radio(
        "Choose an option",
        ["🔐 Sign In", "📝 Create Account"],
        horizontal=True
    )

    st.divider()

    # ==========================================
    # CREATE ACCOUNT
    # ==========================================

    if auth_option == "📝 Create Account":

        st.subheader("Create your account")

        account_type = st.radio(
            "Account type",
            ["🎓 Student", "🏫 Institute"],
            horizontal=True
        )

        if account_type == "🎓 Student":
            name_label = "Full Name"
        else:
            name_label = "Institute Name"

        full_name = st.text_input(
            name_label,
            key="signup_name"
        )

        email = st.text_input(
            "Email Address",
            key="signup_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="signup_confirm_password"
        )

        if st.button(
            "Create Account",
            type="primary",
            use_container_width=True
        ):

            if not full_name.strip():

                st.error(
                    f"Please enter your {name_label.lower()}."
                )

            elif not email.strip():

                st.error(
                    "Please enter your email address."
                )

            elif not password:

                st.error(
                    "Please enter a password."
                )

            elif len(password) < 6:

                st.error(
                    "Password must be at least 6 characters."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                selected_account_type = (
                    "student"
                    if account_type == "🎓 Student"
                    else "institute"
                )

                try:

                    response = supabase.auth.sign_up(
                        {
                            "email": email.strip(),
                            "password": password,
                            "options": {
                                "data": {
                                    "full_name": full_name.strip(),
                                    "account_type": selected_account_type
                                }
                            }
                        }
                    )

                    if response.user:

                        st.success(
                            "✅ Account created successfully!"
                        )

                        st.info(
                            "📧 Please check your email and "
                            "confirm your account before signing in."
                        )

                except Exception as e:

                    st.error(
                        f"Unable to create account: {str(e)}"
                    )

    # ==========================================
    # SIGN IN
    # ==========================================

    else:

        st.subheader("Sign in to your account")

        email = st.text_input(
            "Email Address",
            key="signin_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="signin_password"
        )

        if st.button(
            "Sign In",
            type="primary",
            use_container_width=True
        ):

            if not email.strip():

                st.error(
                    "Please enter your email address."
                )

            elif not password:

                st.error(
                    "Please enter your password."
                )

            else:

                try:

                    response = (
                        supabase.auth
                        .sign_in_with_password(
                            {
                                "email": email.strip(),
                                "password": password
                            }
                        )
                    )

                    if response.user:

                        st.session_state.user = response.user

                        user_id = response.user.id

                        profile_response = (
                            supabase
                            .table("profiles")
                            .select(
                                "full_name, account_type"
                            )
                            .eq(
                                "id",
                                user_id
                            )
                            .single()
                            .execute()
                        )

                        if profile_response.data:

                            st.session_state.account_type = (
                                profile_response
                                .data["account_type"]
                            )

                        st.success(
                            "✅ Sign in successful!"
                        )

                        st.rerun()

                except Exception:

                    st.error(
                        "❌ Sign in failed. Please check "
                        "your email, password, and email "
                        "verification."
                    )
# ==========================================
# LOGGED-IN HOME PAGE
# ==========================================

def show_home_page():

    # Get logged-in user's account type
    account_type = st.session_state.get(
        "account_type",
        "student"
    )

    # Try to get the user's name from Supabase
def show_home_page():

    # Try to get the user's profile from Supabase
    full_name = "User"
    account_type = st.session_state.get(
        "account_type",
        "student"
    )

    try:

        if st.session_state.user:

            user_id = st.session_state.user.id

            profile_response = (
                supabase
                .table("profiles")
                .select("full_name, account_type")
                .eq("id", user_id)
                .execute()
            )
            st.write("DEBUG PROFILE:", profile_response.data)

            if profile_response.data:

                profile = profile_response.data[0]

                full_name = (
                    profile.get("full_name")
                    or "User"
                )

                account_type = (
                    profile.get("account_type")
                    or "student"
                )

    except Exception as e:

        st.error(
            f"Profile loading error: {e}"
        )

    # ==========================================
    # WELCOME SECTION
    # ==========================================

    st.title(
        f"👋 Welcome, {full_name}!"
    )

    if account_type == "student":

        st.caption(
            "🎓 Student Account"
        )

    else:

        st.caption(
            "🏫 Institute Account"
        )


    st.subheader(
        "AI-Powered Student GPA & GenAI Impact Predictor"
    )

    st.write(
        "StudentGPA AI helps you understand your academic "
        "performance by combining academic information, "
        "study habits, and Generative AI usage."
    )

    st.write(
        "Use our machine-learning system to estimate your "
        "post-semester GPA and receive useful educational "
        "guidance based on your profile."
    )


    # ==========================================
    # START PREDICTION
    # ==========================================

    st.divider()

    st.subheader(
        "🚀 Ready to explore your academic performance?"
    )

    st.write(
        "Enter your academic and study information to "
        "receive an estimated post-semester GPA."
    )

    if st.button(
        "🚀 Start GPA Prediction",
        type="primary",
        use_container_width=True
    ):

        st.session_state.current_page = "GPA Predictor"
        st.rerun()


    # ==========================================
    # FEATURES
    # ==========================================

    st.divider()

    st.subheader(
        "✨ What can StudentGPA AI do?"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            "### 🎓 GPA Prediction"
        )

        st.write(
            "Estimate your post-semester GPA using "
            "your academic performance and study profile."
        )


    with col2:

        st.markdown(
            "### 🤖 GenAI Impact"
        )

        st.write(
            "Explore how your Generative AI usage "
            "relates to your academic profile."
        )


    with col3:

        st.markdown(
            "### 📊 Academic Insights"
        )

        st.write(
            "Understand important factors that may "
            "influence your predicted GPA."
        )


    # ==========================================
    # HOW IT WORKS
    # ==========================================

    st.divider()

    st.subheader(
        "🔍 How StudentGPA AI Works"
    )

    step1, step2, step3, step4 = st.columns(4)

    with step1:

        st.markdown(
            "### 1️⃣"
        )

        st.markdown(
            "**Enter your profile**"
        )

        st.write(
            "Provide your academic information "
            "and study habits."
        )


    with step2:

        st.markdown(
            "### 2️⃣"
        )

        st.markdown(
            "**Describe your GenAI usage**"
        )

        st.write(
            "Tell us how you use Generative AI "
            "for your academic activities."
        )


    with step3:

        st.markdown(
            "### 3️⃣"
        )

        st.markdown(
            "**Get your prediction**"
        )

        st.write(
            "Our machine-learning model estimates "
            "your post-semester GPA."
        )


    with step4:

        st.markdown(
            "### 4️⃣"
        )

        st.markdown(
            "**Understand your results**"
        )

        st.write(
            "Receive general educational guidance "
            "based on your profile."
        )


    # ==========================================
    # WHY USE STUDENTGPA AI
    # ==========================================

    st.divider()

    st.subheader(
        "💡 Why use StudentGPA AI?"
    )

    st.write(
        "StudentGPA AI is designed to help students "
        "better understand their academic habits and "
        "make more informed study decisions."
    )

    st.markdown(
        """
        - 📈 Understand your academic trajectory
        - 🤖 Explore your GenAI usage
        - 📚 Identify study habits that may need attention
        - 🧠 Receive general educational guidance
        """
    )


    # ==========================================
    # DISCLAIMER
    # ==========================================

    st.divider()

    st.warning(
        "⚠️ Educational tool only: GPA predictions are "
        "estimates generated by a machine-learning model. "
        "They are not official academic decisions, "
        "admission decisions, or guarantees of future "
        "academic performance."
    )


# ==========================================
# PROTECT THE MAIN APPLICATION
# ==========================================

if st.session_state.user is None:

    show_auth_page()

    st.stop()
# ==========================================
# MAIN NAVIGATION
# ==========================================

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

with st.sidebar:

    st.title("🎓 StudentGPA AI")

    st.divider()

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.current_page = "Home"
        st.rerun()

    if st.button("🎓 GPA Predictor", use_container_width=True):
        st.session_state.current_page = "GPA Predictor"
        st.rerun()

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.session_state.account_type = None
        st.session_state.current_page = "Home"
        st.rerun()
if st.session_state.current_page == "Home":

        show_home_page()

        st.stop()

st.divider()

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
        "You can predict your post-semester GPC 📈 before the ending of you semester"
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
