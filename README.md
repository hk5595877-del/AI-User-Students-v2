# Student GPA · AI Impact Predictor v2

A standalone Streamlit machine-learning app for estimating **Post-Semester GPA** from academic, study-habit, and GenAI-usage features.

## What changed from the original project

The original app depended on an Azure ML real-time endpoint and API key. That endpoint is no longer required.

**v2 runs the trained scikit-learn pipeline directly inside Streamlit:**

Student inputs → preprocessing → Random Forest model (100 trees) → GPA estimate → educational AI-style guidance

This makes the project portable and easy to deploy on Streamlit Community Cloud, Docker, or another Python host.

## Model

The included model was retrained from `ai_student_impact_dataset.csv`.

- Target: `Post_Semester_GPA`
- Training/test split: 80/20
- Regressor: CatBoostRegressor
- Random seed: 42
- Student ID excluded from training because it is an identifier, not a meaningful predictive feature.
- Categorical variables are one-hot encoded.
- Unknown categories are handled safely.
- Missing numeric values use median imputation.

Validation results for the included model:

- MAE: approximately **0.118**
- RMSE: approximately **0.151**
- R²: approximately **0.905**

These metrics are dataset-level validation results and do not guarantee an individual's prediction accuracy.

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
