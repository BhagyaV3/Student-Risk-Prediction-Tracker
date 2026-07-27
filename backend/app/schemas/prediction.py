from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional

class PredictionRequest(BaseModel):
    student_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "student_id": 1
            }
        }

class PredictionResponse(BaseModel):
    id: int
    student_id: int
    prediction_label: str
    prediction_score: float
    confidence: float
    feature_importance: Dict[str, float]
    created_at: datetime
    risk_level: Optional[str] = None
    risk_score: Optional[float] = None

    class Config:
        from_attributes = True