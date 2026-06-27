import os
import joblib
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Paths to saved model files
MODEL_DIR = os.path.dirname(__file__)
MODEL_PATH  = os.path.join(MODEL_DIR, "model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")

RISK_LABELS = {0: "low", 1: "medium", 2: "high"}
FEATURE_NAMES = [
    "attendance_percentage",
    "gpa",
    "assignment_completion_percentage",
    "test_score_average",
    "behavior_score",
]

class MLService:
    def __init__(self):
        self.model  = None
        self.scaler = None
        self._load()

    def _load(self):
        """Load model and scaler from disk."""
        try:
            self.model  = joblib.load(MODEL_PATH)
            self.scaler = joblib.load(SCALER_PATH)
            logger.info("ML model and scaler loaded successfully")
        except FileNotFoundError as e:
            logger.error(f"Model files not found: {e}")
            raise RuntimeError(
                "ML model not found. Run: python -m app.ml_model.train"
            )

    def predict(self, metrics: dict) -> dict:
        """
        Predict risk level from student metrics.
        
        metrics: dict with keys matching FEATURE_NAMES
        returns: dict with risk_level (str), risk_score (float), 
                 confidence (float), feature_importance (dict)
        """
        # Extract features in correct order
        try:
            features = np.array([[metrics[f] for f in FEATURE_NAMES]])
        except KeyError as e:
            raise ValueError(f"Missing required metric: {e}")

        # Scale features using the same scaler from training
        features_scaled = self.scaler.transform(features)

        # Get prediction and probability scores
        risk_index  = int(self.model.predict(features_scaled)[0])
        probabilities = self.model.predict_proba(features_scaled)[0]

        risk_label  = RISK_LABELS[risk_index]
        confidence  = float(probabilities[risk_index])
        risk_score  = float(probabilities[2])  # probability of high risk (0.0–1.0)

        # Feature importance from the forest
        importances = self.model.feature_importances_
        feature_importance = {
            name: round(float(imp), 4)
            for name, imp in zip(FEATURE_NAMES, importances)
        }

        return {
            "risk_level":         risk_label,
            "risk_score":         round(risk_score, 4),
            "confidence":         round(confidence, 4),
            "feature_importance": feature_importance,
        }


# Single instance shared across the whole app
ml_service = MLService()