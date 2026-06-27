import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import joblib
import os

# ── 1. Generate synthetic training data ──────────────────────────────────────

np.random.seed(42)
N = 500

def generate_students(n):
    data = []
    for _ in range(n):
        # Randomly assign a risk level: 0=low, 1=medium, 2=high
        risk = np.random.choice([0, 1, 2], p=[0.5, 0.3, 0.2])

        if risk == 0:  # Low risk: good metrics
            attendance    = np.random.uniform(80, 100)
            gpa           = np.random.uniform(2.8, 4.0)
            assignments   = np.random.uniform(80, 100)
            test_score    = np.random.uniform(75, 100)
            behavior      = np.random.uniform(75, 100)
        elif risk == 1:  # Medium risk: average metrics
            attendance    = np.random.uniform(60, 85)
            gpa           = np.random.uniform(1.8, 3.0)
            assignments   = np.random.uniform(60, 85)
            test_score    = np.random.uniform(55, 78)
            behavior      = np.random.uniform(55, 80)
        else:  # High risk: poor metrics
            attendance    = np.random.uniform(0, 65)
            gpa           = np.random.uniform(0, 2.0)
            assignments   = np.random.uniform(0, 65)
            test_score    = np.random.uniform(0, 60)
            behavior      = np.random.uniform(0, 60)

        data.append([attendance, gpa, assignments, test_score, behavior, risk])

    return pd.DataFrame(data, columns=[
        "attendance_percentage",
        "gpa",
        "assignment_completion_percentage",
        "test_score_average",
        "behavior_score",
        "risk_level"
    ])

df = generate_students(N)
print(f"Generated {len(df)} student records")
print(df["risk_level"].value_counts().sort_index()
      .rename({0: "Low", 1: "Medium", 2: "High"}))

# ── 2. Split features and target ─────────────────────────────────────────────

X = df.drop("risk_level", axis=1)
y = df["risk_level"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── 3. Scale features ────────────────────────────────────────────────────────

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ── 4. Train Random Forest ───────────────────────────────────────────────────

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight="balanced"
)
model.fit(X_train_scaled, y_train)

# ── 5. Evaluate ──────────────────────────────────────────────────────────────

y_pred = model.predict(X_test_scaled)
print("\n===== Model Evaluation =====")
print(classification_report(y_test, y_pred,
      target_names=["Low Risk", "Medium Risk", "High Risk"]))

# ── 6. Save model and scaler ─────────────────────────────────────────────────

output_dir = os.path.dirname(__file__)
joblib.dump(model,  os.path.join(output_dir, "model.pkl"))
joblib.dump(scaler, os.path.join(output_dir, "scaler.pkl"))
print("✅ model.pkl and scaler.pkl saved to", output_dir)