from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.user import User
from app.models.student import Student
from app.models.academic_metrics import AcademicMetrics
from app.schemas.student import (
    StudentCreate, StudentUpdate, StudentResponse, 
    AcademicMetricsCreate, AcademicMetricsResponse, StudentDetailResponse
)
from app.services.dependencies import get_current_user

router = APIRouter(prefix="/api/students", tags=["students"])

# Helper function to check authorization
def get_student_or_403(student_id: int, current_user: User, db: Session):
    """Get student if owned by current teacher, else raise 403"""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    if student.teacher_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return student

# Create Student
@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    student_data: StudentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new student for the current teacher"""
    # Check if email already exists
    existing_student = db.query(Student).filter(Student.email == student_data.email).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    new_student = Student(
        teacher_id=current_user.id,
        first_name=student_data.first_name,
        last_name=student_data.last_name,
        email=student_data.email
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# List Students
@router.get("", response_model=list[StudentResponse])
def list_students(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all students for the current teacher (with pagination)"""
    students = db.query(Student).filter(
        Student.teacher_id == current_user.id
    ).offset(skip).limit(limit).all()
    return students

# Get Single Student
@router.get("/{student_id}", response_model=StudentDetailResponse)
def get_student(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a single student (includes all metrics)"""
    student = get_student_or_403(student_id, current_user, db)
    return student

# Update Student
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a student"""
    student = get_student_or_403(student_id, current_user, db)
    
    # Update only provided fields
    if student_data.first_name is not None:
        student.first_name = student_data.first_name
    if student_data.last_name is not None:
        student.last_name = student_data.last_name
    if student_data.email is not None:
        # Check if new email is unique
        existing = db.query(Student).filter(
            Student.email == student_data.email,
            Student.id != student_id
        ).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        student.email = student_data.email
    
    db.commit()
    db.refresh(student)
    return student

# Delete Student
@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a student (also deletes all associated metrics)"""
    student = get_student_or_403(student_id, current_user, db)
    db.delete(student)
    db.commit()
    return None

# Record Academic Metrics
@router.post("/{student_id}/metrics", response_model=AcademicMetricsResponse, status_code=status.HTTP_201_CREATED)
def record_metrics(
    student_id: int,
    metrics_data: AcademicMetricsCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record academic metrics for a student"""
    student = get_student_or_403(student_id, current_user, db)
    
    new_metrics = AcademicMetrics(
        student_id=student_id,
        attendance_percentage=metrics_data.attendance_percentage,
        gpa=metrics_data.gpa,
        assignment_completion_percentage=metrics_data.assignment_completion_percentage,
        test_score_average=metrics_data.test_score_average,
        behavior_score=metrics_data.behavior_score
    )
    db.add(new_metrics)
    db.commit()
    db.refresh(new_metrics)
    return new_metrics

# List Student Metrics
@router.get("/{student_id}/metrics", response_model=list[AcademicMetricsResponse])
def list_metrics(
    student_id: int,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all metrics for a student"""
    student = get_student_or_403(student_id, current_user, db)
    metrics = db.query(AcademicMetrics).filter(
        AcademicMetrics.student_id == student_id
    ).offset(skip).limit(limit).all()
    return metrics

# Get Latest Metrics
@router.get("/{student_id}/metrics/latest", response_model=AcademicMetricsResponse)
def get_latest_metrics(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the most recent metrics for a student"""
    student = get_student_or_403(student_id, current_user, db)
    metrics = db.query(AcademicMetrics).filter(
        AcademicMetrics.student_id == student_id
    ).order_by(AcademicMetrics.recorded_date.desc()).first()
    
    if not metrics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No metrics found")
    
    return metrics