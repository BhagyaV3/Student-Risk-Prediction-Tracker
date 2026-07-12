"""
Model Assumptions & Design Decisions
======================================

Algorithm
---------
Random Forest classifier (sklearn RandomForestClassifier).
  - 100 estimators, max_depth=10, class_weight="balanced", random_state=42.
  - "balanced" weighting compensates for the class imbalance in training data
    (50% low / 30% medium / 20% high).

Training data
-------------
Synthetic data generated with np.random.seed(42), N=500 students.
Features are drawn from overlapping uniform distributions per risk class:

  Feature                          Low risk      Medium risk   High risk
  ─────────────────────────────────────────────────────────────────────
  attendance_percentage            80–100        60–85         0–65
  gpa (0.0–4.0 scale)              2.8–4.0       1.8–3.0       0.0–2.0
  assignment_completion_percentage 80–100        60–85         0–65
  test_score_average               75–100        55–78         0–60
  behavior_score                   75–100        55–80         0–60

The overlap between adjacent classes is intentional — it reflects
real-world ambiguity at the boundaries between risk levels.

Pre-processing
--------------
All five features are standardised with StandardScaler (zero mean, unit
variance) fitted on the training split only.  The fitted scaler is saved
alongside the model and must be applied identically at inference time.

Target variable
---------------
  0 → "low"    (≈50% of training samples)
  1 → "medium" (≈30%)
  2 → "high"   (≈20%)

Outputs (from ml_service.predict)
----------------------------------
  risk_level        : str  – predicted class label ("low" / "medium" / "high")
  risk_score        : float [0, 1] – P(high risk); used for ranking/sorting
  confidence        : float [0, 1] – P(predicted class); model certainty
  feature_importance: dict – global Gini importances from the forest (sum ≈ 1)

Limitations
-----------
- Trained entirely on synthetic data; real-world performance may differ.
- Importance values are global (forest-level), not per-student explanations.
- Model does not handle temporal trends; each prediction is stateless.
- Features outside the training distribution will be extrapolated by the
  forest but may produce less reliable results.
- Retraining is required when score scales or grading policies change.
"""

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