from pydantic import BaseModel
from datetime import datetime
from typing import Dict

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
    risk_level: str
    risk_score: float
    confidence: float
    feature_importance: Dict[str, float]
    created_at: datetime

    class Config:
        from_attributes = True