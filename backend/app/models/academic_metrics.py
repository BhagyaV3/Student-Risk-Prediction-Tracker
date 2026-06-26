from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.db import Base

class AcademicMetrics(Base):
    __tablename__ = "academic_metrics"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    attendance_percentage = Column(Float, nullable=False)  # 0-100
    gpa = Column(Float, nullable=False)  # 0-4.0
    assignment_completion_percentage = Column(Float, nullable=False)  # 0-100
    test_score_average = Column(Float, nullable=False)  # 0-100
    behavior_score = Column(Float, nullable=False)  # 0-100
    recorded_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to Student
    student = relationship("Student", back_populates="metrics")

    def __repr__(self):
        return f"<AcademicMetrics(id={self.id}, student_id={self.student_id}, gpa={self.gpa})>"