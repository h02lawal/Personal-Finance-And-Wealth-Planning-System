import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, precision_score, recall_score, f1_score, brier_score_loss
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibrationDisplay

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "financial_risk_model.joblib"
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

DATA_PATH = PROJECT_ROOT / "data" / "synthetic_financial_data.csv"

df = pd.read_csv(DATA_PATH)
data = df[["income","expense","savings","debt"]]
label = df["label"].map({"Yes":1, "No":0})

data_train, data_test, label_train, label_test = train_test_split(data, label, test_size=0.2, random_state=42, stratify=label)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, random_state=42))
model.fit(data_train, label_train)

prediction_test = model.predict(data_test)
prediction_proba = model.predict_proba(data_test)[:, 1]

random_forest = RandomForestClassifier(n_estimators=150, max_depth=12, min_samples_leaf=5, random_state=42, n_jobs=-1)
random_forest.fit(data_train, label_train)

rf_pred = random_forest.predict(data_test)
rf_prob = random_forest.predict_proba(data_test)[:, 1]

logistic_brier = brier_score_loss(label_test, prediction_proba)
forest_brier = brier_score_loss(label_test, rf_prob)

thresholds = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]

print("Random Forest Results: ")
print("\nRandom Forest Threshold Comparison")
print("Threshold | Precision | Recall | F1")

for threshold in thresholds:
    predictions = (rf_prob >= threshold).astype(int)

    precision = precision_score(label_test, predictions, zero_division=0)
    recall = recall_score(label_test, predictions, zero_division=0)
    f1 = f1_score(label_test, predictions, zero_division=0)

    print(
        f"{threshold:.2f}      | "
        f"{precision:.3f}     | "
        f"{recall:.3f} | "
        f"{f1:.3f}"
    )



print("\nRandom Forest Classification Report:")
print(classification_report(label_test, rf_pred))

print("\nRandom Forest Confusion Matrix:")
print(confusion_matrix(label_test, rf_pred))

print("\nRandom Forest ROC-AUC:")
print(roc_auc_score(label_test, rf_prob))


print("\n\nLogistic Regression Results::")
print("Classification Report:")
print(classification_report(label_test, prediction_test))

print("\nConfusion Matrix:")
print(confusion_matrix(label_test, prediction_test))

print("\nROC-AUC Score:")
print(roc_auc_score(label_test, prediction_proba))

print("\nProbability Evaluation:")
print(f"Logistic Regression Brier Score: {logistic_brier:.4f}")
print(f"Random Forest Brier Score: {forest_brier:.4f}")

fig, ax = plt.subplots(figsize=(8, 6))

CalibrationDisplay.from_predictions(label_test, prediction_proba, n_bins=10, name="Logistic Regression", ax=ax)
CalibrationDisplay.from_predictions(label_test, rf_prob, n_bins=10, name="Random Forest", ax=ax)
ax.plot([0, 1], [0, 1], "k--", label="Perfect Calibration")
ax.set_title("Financial Shortfall Probability Calibration")
ax.legend()

plt.show()

joblib.dump(model, MODEL_PATH)


