# StudentGPA AI — Machine Learning Model Documentation

## 1. Model Overview

StudentGPA AI uses a machine learning regression model to estimate a student's Post-Semester GPA from academic, study-habit, and Generative AI usage characteristics.

The trained model is packaged with the application and loaded locally during prediction.

Model file:

`model.joblib`

---

## 2. Prediction Target

The model predicts:

`Post_Semester_GPA`

This represents the student's predicted GPA after the semester.

The model produces a numerical regression output.

---

## 3. Input Features

The prediction pipeline uses the following student characteristics:

- `Major_Category`
- `Year_of_Study`
- `Pre_Semester_GPA`
- `Weekly_GenAI_Hours`
- `Primary_Use_Case`
- `Prompt_Engineering_Skill`
- `Tool_Diversity`
- `Paid_Subscription`
- `Traditional_Study_Hours`
- `Perceived_AI_Dependency`
- `Institutional_Policy`
- `Anxiety_Level_During_Exams`

`Student_ID` is not used as a predictive feature.

---

## 4. Dataset

The model was trained using the AI Student Impact Dataset.

The dataset is identified as CC0 / Public Domain on its Kaggle dataset page.

The project does not claim exclusive ownership of the underlying dataset.

Dataset source:

https://www.kaggle.com/datasets/pavankatroth/ai-student-impact-dataset

---

## 5. Data Preprocessing

Before model training, the dataset is prepared for machine learning.

The preprocessing process includes:

- Separating predictive features from the target variable
- Excluding non-predictive identifiers
- Handling categorical variables
- Handling missing numeric values
- Preparing training and validation data
- Converting data into a format compatible with the regression model

The preprocessing implemented in `train_model.py` should be treated as the authoritative implementation.

---

## 6. Train / Validation Split

The dataset is divided into:

- 80% training data
- 20% validation data

A fixed random seed is used to improve reproducibility.

Random seed:

`42`

---

## 7. Machine Learning Algorithm

The current model uses:

`CatBoostRegressor`

CatBoost is a gradient-boosting machine learning algorithm designed to work effectively with structured/tabular data, including datasets containing categorical variables.

The trained model is serialized using Joblib.

---

## 8. Model Evaluation

The documented validation performance is approximately:

| Metric | Value |
|--------|------:|
| MAE | 0.118 |
| RMSE | 0.151 |
| R² | 0.905 |

These values represent validation performance and should not be interpreted as a guarantee of prediction accuracy for future students.

Model performance can change if:

- The dataset changes
- The training process changes
- New populations are evaluated
- Input distributions differ from the training data
- The model is retrained with different parameters

---

## 9. Model File

The trained model is stored as:

`model.joblib`

The application loads this file during execution.

The model file should remain compatible with the Python and machine-learning library versions used by the application.

---

## 10. Training Script

The model can be retrained using:

`train_model.py`

Typical training command:

```bash
python train_model.py
