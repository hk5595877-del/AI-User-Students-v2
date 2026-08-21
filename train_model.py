from pathlib import Path
import json
import joblib
import pandas as pd
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "ai_student_impact_dataset.csv"
MODEL_PATH = ROOT / "model.joblib"
METRICS_PATH = ROOT / "model_metrics.json"

TARGET = "Post_Semester_GPA"
ID_COLUMN = "Student_ID"
RANDOM_STATE = 42

df = pd.read_csv(DATA_PATH)
if TARGET not in df.columns:
    raise ValueError(f"Missing target column: {TARGET}")

X = df.drop(columns=[TARGET, ID_COLUMN], errors="ignore")
y = df[TARGET]

categorical = X.select_dtypes(include=["object"]).columns.tolist()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=RANDOM_STATE
)

model = CatBoostRegressor(
    iterations=700,
    depth=7,
    learning_rate=0.05,
    loss_function="RMSE",
    random_seed=RANDOM_STATE,
    verbose=False,
    thread_count=-1,
)

model.fit(X_train, y_train, cat_features=categorical)
pred = model.predict(X_test)

metrics = {
    "model": "CatBoostRegressor",
    "target": TARGET,
    "features": list(X.columns),
    "categorical_features": categorical,
    "train_rows": len(X_train),
    "test_rows": len(X_test),
    "mae": float(mean_absolute_error(y_test, pred)),
    "rmse": float(mean_squared_error(y_test, pred) ** 0.5),
    "r2": float(r2_score(y_test, pred)),
    "random_state": RANDOM_STATE,
    "iterations": 700,
    "depth": 7,
    "learning_rate": 0.05,
}

joblib.dump(model, MODEL_PATH, compress=3)
METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

print(json.dumps(metrics, indent=2))
print(f"Saved model to {MODEL_PATH}")
