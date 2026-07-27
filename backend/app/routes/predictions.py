from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.user import User
from app.models.student import Student
from app.models.academic_metrics import AcademicMetrics
from app.models.prediction import Prediction
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.dependencies import get_current_user
from app.ml_model.ml_service import ml_service

router = APIRouter(prefix="/api/predictions", tags=["predictions"])


def get_student_or_403(student_id: int, current_user: User, db: Session):
    """Get student if owned by current teacher, else raise 403."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    if student.teacher_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return student


@router.post("/predict", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
def predict(
    request: PredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Run a risk prediction for a student using their latest recorded metrics."""
    student = get_student_or_403(request.student_id, current_user, db)

    latest_metrics = (
        db.query(AcademicMetrics)
        .filter_by(student_id=student.id)
        .order_by(AcademicMetrics.recorded_date.desc())
        .first()
    )
    if not latest_metrics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No metrics found for this student. Record metrics first."
        )

    metrics_dict = {
        "attendance_percentage":          latest_metrics.attendance_percentage,
        "gpa":                            latest_metrics.gpa,
        "assignment_completion_percentage": latest_metrics.assignment_completion_percentage,
        "test_score_average":             latest_metrics.test_score_average,
        "behavior_score":                 latest_metrics.behavior_score,
    }

    result = ml_service.predict(metrics_dict)

    prediction = Prediction(
        student_id=student.id,
        risk_level=result["prediction_label"],
        risk_score=result["prediction_score"],
        confidence=result["confidence"],
        feature_importance=result["feature_importance"],
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return {
        "id": prediction.id,
        "student_id": prediction.student_id,
        "prediction_label": result["prediction_label"],
        "prediction_score": result["prediction_score"],
        "confidence": prediction.confidence,
        "feature_importance": prediction.feature_importance,
        "created_at": prediction.created_at,
        "risk_level": prediction.risk_level,
        "risk_score": prediction.risk_score,
    }