# StudentGPA AI — System Architecture

## 1. Overview

StudentGPA AI is a Streamlit-based machine learning application designed to estimate student GPA outcomes using academic, study-habit, and Generative AI usage features.

The application uses a locally stored machine learning model rather than relying on an external Azure ML prediction endpoint.

---

## 2. Main Technologies

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- CatBoost
- Joblib
- Supabase Authentication
- Google Analytics
- GitHub
- Streamlit Community Cloud

---

## 3. Application Architecture

The application follows this general flow:

User
↓
Streamlit Web Interface
↓
Authentication / Account Management
↓
Prediction Interface
↓
Input Validation & Transformation
↓
Machine Learning Model
↓
Prediction
↓
Result + AI Coaching / Guidance

---

## 4. Authentication

User authentication is handled through Supabase.

The application uses:

- Supabase project URL
- Supabase API key
- Email/password authentication

Supabase credentials are stored using Streamlit secrets and are not intended to be committed to the public repository.

---

## 5. Machine Learning Pipeline

The machine learning pipeline consists of:

1. Dataset preparation
2. Feature preprocessing
3. Training/validation split
4. CatBoost regression model training
5. Model evaluation
6. Model serialization
7. Prediction inside the Streamlit application

The trained model is stored locally as:

`model.joblib`

Model evaluation information is stored as:

`model_metrics.json`

---

## 6. Dataset

The project uses the AI Student Impact Dataset.

The dataset was obtained from Kaggle and is identified as CC0 / Public Domain on its dataset page.

The project does not claim exclusive ownership of the underlying third-party dataset.

The dataset is used for machine learning development and prediction functionality.

---

## 7. Prediction Flow

### Student Prediction

A student enters the required academic and AI-usage information through the Streamlit interface.

The application:

1. Collects the input.
2. Validates the values.
3. Converts the input into the format expected by the model.
4. Sends the processed data to the local machine learning model.
5. Receives the predicted GPA.
6. Displays the result.
7. Provides additional AI-related guidance where applicable.

---

## 8. Institute Prediction

Institute accounts can use batch prediction functionality.

The institute provides student information through a CSV file.

The application:

1. Accepts the uploaded CSV.
2. Validates the required columns.
3. Converts values into the model's expected format.
4. Performs predictions for the uploaded records.
5. Displays the prediction results.
6. Allows the resulting information to be used for further analysis.

The application should validate uploaded files before processing them.

---

## 9. SSC / HSSC Prediction

The application includes percentage-to-GPA conversion functionality for SSC/HSSC prediction.

The conversion process is separate from the normal university GPA input workflow.

The application converts percentage values into an equivalent GPA representation before using the prediction pipeline and can convert the resulting GPA back into a percentage representation for display.

The conversion scale is defined within the application code.

---

## 10. Analytics

Google Analytics is used to measure application activity and selected application events.

Analytics is intended to provide information about application usage and feature interaction.

Analytics credentials/configuration should not be treated as user authentication credentials.

---

## 11. Deployment

The application can be deployed using Streamlit Community Cloud.

The deployment process generally consists of:

1. GitHub repository
2. Streamlit Community Cloud
3. Python dependencies from `requirements.txt`
4. Streamlit secrets configuration
5. Application startup through `app.py`

---

## 12. Important Project Files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application |
| `train_model.py` | Machine learning training pipeline |
| `model.joblib` | Trained machine learning model |
| `model_metrics.json` | Model evaluation metrics |
| `ai_student_impact_dataset.csv` | Machine learning dataset |
| `requirements.txt` | Python dependencies |
| `pyproject.toml` | Python project configuration |
| `README.md` | Project overview and setup instructions |
| `PROJECT_AUTHORS.md` | Project authorship information |
| `LICENSE` | Project licensing information |
| `THIRD_PARTY_NOTICES.md` | Third-party materials and licenses |
| `DATASET_NOTICE.md` | Dataset licensing information |
| `IP_AND_OWNERSHIP.md` | Intellectual property information |
| `PRIVACY_POLICY.md` | Privacy policy |
| `TERMS_OF_SERVICE.md` | Terms of service |

---

## 13. Security

Sensitive configuration values should be stored through environment variables or Streamlit secrets.

The following should never be committed to the public repository:

- API keys
- Passwords
- Authentication secrets
- Private credentials
- Service-account credentials
- Private certificates

The `.gitignore` file should be configured to prevent accidental commits of sensitive files.

---

## 14. Current Architecture

The current version is designed to operate without the previous Azure ML real-time inference dependency.

The machine learning model is packaged with the application and loaded locally during application execution.

This reduces dependence on an external model endpoint and simplifies deployment.

---

## 15. Future Improvements

Potential future improvements include:

- Production database architecture
- Subscription/payment integration
- Advanced institute dashboards
- User prediction history
- Model monitoring
- Automated model retraining
- Additional educational prediction models
- Improved analytics
- Role-based administration
- Scalable cloud infrastructure
