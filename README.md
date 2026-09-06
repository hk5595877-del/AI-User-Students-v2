# Student GPA · AI Impact Predictor v2

A standalone Streamlit machine-learning app for estimating **Post-Semester GPA** from academic, study-habit, and GenAI-usage features.

## What changed from the original project

The original app depended on an Azure ML real-time endpoint and API key. That endpoint is no longer required.

**v2 runs the trained scikit-learn pipeline directly inside Streamlit:**

Student inputs → preprocessing → CatBoostRegressor → GPA estimate → educational AI-style guidance

This makes the project portable and easy to deploy on Streamlit Community Cloud, Docker, or another Python host.

## Machine Learning Model

The application uses a CatBoostRegressor trained on the included
AI Student Impact Dataset.

- Target: `Post_Semester_GPA`
- Training/test split: 80/20
- Model: CatBoostRegressor
- Random seed: 42
- Student ID excluded from training
- Categorical variables handled by the training pipeline
- Missing values handled during preprocessing

### Validation

The included model has the following dataset-level validation results:

- MAE: approximately 0.118
- RMSE: approximately 0.151
- R²: approximately 0.905

These metrics describe validation performance on the available dataset
and do not guarantee the accuracy of an individual student's
prediction.

## Run locally

Python 3.12 is recommended.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

No `.env`, Azure endpoint, Azure API key, or cloud credentials are required.

## Retrain the model

If you update the dataset:

```bash
python train_model.py
```

This creates/updates:

- `model.joblib`
- `model_metrics.json`

## Deploy on Streamlit Community Cloud

1. Create a new GitHub repository.
2. Upload the contents of this project.
3. In Streamlit Community Cloud, select the repository and `app.py`.
4. Deploy.

No secrets are needed for the core prediction functionality.

## Docker

```bash
docker build -t student-gpa-ai-impact .
docker run -p 8501:8501 student-gpa-ai-impact
```

Open `http://localhost:8501`.

## Project structure

```text
.
├── app.py
├── train_model.py
├── model.joblib
├── model_metrics.json
├── ai_student_impact_dataset.csv
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── .python-version
├── .streamlit/
│   └── config.toml
└── assets/
```

## Important educational-use note

This is an academic estimation tool. It should not be used as an official university grading, admissions, scholarship, disciplinary, or other high-impact decision system.
