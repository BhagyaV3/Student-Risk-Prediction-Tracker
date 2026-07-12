"""
Tests for app/ml_model/ml_service.py

Coverage:
- Output structure (required keys, types, value ranges)
- Prediction sanity (good metrics → low risk, bad metrics → high risk)
- Edge cases (missing features, extreme values, extra keys)
- Model lazy-loading and missing-file error handling
"""

import pytest
import numpy as np
from unittest.mock import patch

from app.ml_model.ml_service import MLService, FEATURE_NAMES, RISK_LABELS

# ── Sample metrics ────────────────────────────────────────────────────────────

LOW_RISK_METRICS = {
    "attendance_percentage": 95.0,
    "gpa": 3.8,
    "assignment_completion_percentage": 96.0,
    "test_score_average": 92.0,
    "behavior_score": 94.0,
}

MEDIUM_RISK_METRICS = {
    "attendance_percentage": 72.0,
    "gpa": 2.4,
    "assignment_completion_percentage": 68.0,
    "test_score_average": 63.0,
    "behavior_score": 65.0,
}

HIGH_RISK_METRICS = {
    "attendance_percentage": 30.0,
    "gpa": 0.8,
    "assignment_completion_percentage": 28.0,
    "test_score_average": 25.0,
    "behavior_score": 22.0,
}

# ── Fixture: real trained service (uses the saved model.pkl / scaler.pkl) ─────

@pytest.fixture(scope="module")
def service():
    """MLService loaded from the saved pkl files."""
    svc = MLService()
    svc._load()
    return svc


# ── Output structure ──────────────────────────────────────────────────────────

class TestOutputStructure:
    def test_returns_all_required_keys(self, service):
        result = service.predict(LOW_RISK_METRICS)
        assert set(result.keys()) == {"risk_level", "risk_score", "confidence", "feature_importance"}

    def test_risk_level_is_valid_label(self, service):
        for metrics in [LOW_RISK_METRICS, MEDIUM_RISK_METRICS, HIGH_RISK_METRICS]:
            assert service.predict(metrics)["risk_level"] in RISK_LABELS.values()

    def test_risk_score_in_valid_range(self, service):
        for metrics in [LOW_RISK_METRICS, MEDIUM_RISK_METRICS, HIGH_RISK_METRICS]:
            score = service.predict(metrics)["risk_score"]
            assert 0.0 <= score <= 1.0

    def test_confidence_in_valid_range(self, service):
        for metrics in [LOW_RISK_METRICS, MEDIUM_RISK_METRICS, HIGH_RISK_METRICS]:
            conf = service.predict(metrics)["confidence"]
            assert 0.0 <= conf <= 1.0

    def test_feature_importance_has_all_features(self, service):
        result = service.predict(LOW_RISK_METRICS)
        assert set(result["feature_importance"].keys()) == set(FEATURE_NAMES)

    def test_feature_importance_sums_to_one(self, service):
        result = service.predict(LOW_RISK_METRICS)
        total = sum(result["feature_importance"].values())
        assert abs(total - 1.0) < 0.01  # rounding tolerance across 5 features

    def test_risk_score_is_float(self, service):
        result = service.predict(LOW_RISK_METRICS)
        assert isinstance(result["risk_score"], float)

    def test_confidence_is_float(self, service):
        result = service.predict(LOW_RISK_METRICS)
        assert isinstance(result["confidence"], float)


# ── Prediction sanity ─────────────────────────────────────────────────────────

class TestPredictionSanity:
    def test_excellent_metrics_predict_low_risk(self, service):
        result = service.predict(LOW_RISK_METRICS)
        assert result["risk_level"] == "low"

    def test_poor_metrics_predict_high_risk(self, service):
        result = service.predict(HIGH_RISK_METRICS)
        assert result["risk_level"] == "high"

    def test_low_risk_score_lower_than_high_risk_score(self, service):
        low_score  = service.predict(LOW_RISK_METRICS)["risk_score"]
        high_score = service.predict(HIGH_RISK_METRICS)["risk_score"]
        assert low_score < high_score

    def test_high_risk_student_risk_score_above_half(self, service):
        result = service.predict(HIGH_RISK_METRICS)
        assert result["risk_score"] >= 0.5

    def test_low_risk_student_risk_score_below_half(self, service):
        result = service.predict(LOW_RISK_METRICS)
        assert result["risk_score"] < 0.5

    def test_deterministic_output(self, service):
        """Same inputs should always produce the same output."""
        result_a = service.predict(MEDIUM_RISK_METRICS)
        result_b = service.predict(MEDIUM_RISK_METRICS)
        assert result_a == result_b


# ── Edge cases ────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_missing_feature_raises_value_error(self, service):
        incomplete = {k: v for k, v in LOW_RISK_METRICS.items() if k != "gpa"}
        with pytest.raises(ValueError, match="Missing required metric"):
            service.predict(incomplete)

    def test_extra_keys_in_metrics_are_ignored(self, service):
        metrics_with_extra = {**LOW_RISK_METRICS, "unknown_field": 999}
        result = service.predict(metrics_with_extra)
        assert result["risk_level"] in RISK_LABELS.values()

    def test_zero_values_predict_high_risk(self, service):
        zero_metrics = {f: 0.0 for f in FEATURE_NAMES}
        result = service.predict(zero_metrics)
        assert result["risk_level"] == "high"

    def test_maximum_values_predict_low_risk(self, service):
        max_metrics = {
            "attendance_percentage": 100.0,
            "gpa": 4.0,
            "assignment_completion_percentage": 100.0,
            "test_score_average": 100.0,
            "behavior_score": 100.0,
        }
        result = service.predict(max_metrics)
        assert result["risk_level"] == "low"

    def test_empty_dict_raises_value_error(self, service):
        with pytest.raises(ValueError, match="Missing required metric"):
            service.predict({})


# ── Lazy-loading & error handling ─────────────────────────────────────────────

class TestModelLoading:
    def test_model_is_none_before_first_predict(self):
        svc = MLService()
        assert svc.model is None
        assert svc.scaler is None

    def test_lazy_load_called_on_first_predict(self):
        """predict() should invoke _load() when model is not yet loaded."""
        svc = MLService()
        with patch.object(svc, "_load") as mock_load:
            mock_load.side_effect = RuntimeError("no model")
            with pytest.raises(RuntimeError):
                svc.predict(LOW_RISK_METRICS)
            mock_load.assert_called_once()

    def test_missing_model_files_raise_runtime_error(self, tmp_path, monkeypatch):
        import app.ml_model.ml_service as svc_module
        monkeypatch.setattr(svc_module, "MODEL_PATH",  str(tmp_path / "missing_model.pkl"))
        monkeypatch.setattr(svc_module, "SCALER_PATH", str(tmp_path / "missing_scaler.pkl"))
        svc = MLService()
        with pytest.raises(RuntimeError, match="ML model not found"):
            svc._load()
