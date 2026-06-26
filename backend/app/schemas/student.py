from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class StudentCreate(BaseModel):
    """Schema for creating a student"""
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com"
            }
        }

class StudentUpdate(BaseModel):
    """Schema for updating a student"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe"
            }
        }

class StudentResponse(BaseModel):
    """Schema for student response"""
    id: int
    teacher_id: int
    first_name: str
    last_name: str
    email: str
    enrollment_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class AcademicMetricsCreate(BaseModel):
    """Schema for recording academic metrics"""
    attendance_percentage: float  # 0-100
    gpa: float  # 0-4.0
    assignment_completion_percentage: float  # 0-100
    test_score_average: float  # 0-100
    behavior_score: float  # 0-100

    class Config:
        json_schema_extra = {
            "example": {
                "attendance_percentage": 92.5,
                "gpa": 3.8,
                "assignment_completion_percentage": 95.0,
                "test_score_average": 87.5,
                "behavior_score": 90.0
            }
        }

class AcademicMetricsResponse(BaseModel):
    """Schema for academic metrics response"""
    id: int
    student_id: int
    attendance_percentage: float
    gpa: float
    assignment_completion_percentage: float
    test_score_average: float
    behavior_score: float
    recorded_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class StudentDetailResponse(BaseModel):
    """Schema for detailed student response (includes metrics)"""
    id: int
    teacher_id: int
    first_name: str
    last_name: str
    email: str
    enrollment_date: datetime
    created_at: datetime
    metrics: List[AcademicMetricsResponse] = []

    class Config:
        from_attributes = True