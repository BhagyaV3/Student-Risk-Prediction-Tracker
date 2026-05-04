# Starter Code Templates

Quick reference for the first critical files to create. Copy and adapt these templates.

---

## Backend: app/main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, students, predictions
from app.database import db

app = FastAPI(
    title="Student Risk Prediction API",
    description="ML-powered student risk prediction system",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(students.router, prefix="/api/students", tags=["students"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["predictions"])

@app.get("/api/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## Backend: app/config.py

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/student_tracker"
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## Backend: app/models/student.py

```python
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100))
    student_id = Column(String(50))
    enrollment_date = Column(Date, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="students")
    metrics = relationship("AcademicMetric", back_populates="student", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="student", cascade="all, delete-orphan")

class AcademicMetric(Base):
    __tablename__ = "academic_metrics"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    attendance_rate = Column(Float)  # 0-100
    gpa = Column(Float)               # 0-4.0
    assignment_completion_rate = Column(Float)  # 0-100
    test_score_average = Column(Float)  # 0-100
    behavioral_score = Column(Float)
    recorded_date = Column(Date, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="metrics")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    risk_level = Column(String(20))  # LOW, MEDIUM, HIGH
    risk_score = Column(Float)        # 0-1
    model_version = Column(String(50))
    contributing_factors = Column(String)  # JSON string
    predicted_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="predictions")
```

---

## Backend: app/schemas/student.py

```python
from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    student_id: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    user_id: int
    enrollment_date: date
    created_at: datetime

    class Config:
        from_attributes = True

class AcademicMetricBase(BaseModel):
    attendance_rate: float = None
    gpa: float = None
    assignment_completion_rate: float = None
    test_score_average: float = None
    behavioral_score: float = None

class AcademicMetricCreate(AcademicMetricBase):
    pass

class AcademicMetricResponse(AcademicMetricBase):
    id: int
    student_id: int
    recorded_date: date
    created_at: datetime

    class Config:
        from_attributes = True

class PredictionResponse(BaseModel):
    id: int
    student_id: int
    risk_level: str
    risk_score: float
    model_version: Optional[str]
    contributing_factors: Optional[dict]
    predicted_at: datetime

    class Config:
        from_attributes = True
```

---

## Backend: app/routes/students.py (Example)

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.student import StudentCreate, StudentResponse, AcademicMetricCreate, AcademicMetricResponse
from app.models.student import Student, AcademicMetric
from app.database import get_db
from app.routes.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[StudentResponse])
async def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all students for current user with pagination"""
    students = db.query(Student).filter(
        Student.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return students

@router.post("/", response_model=StudentResponse)
async def create_student(
    student: StudentCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new student"""
    db_student = Student(**student.dict(), user_id=current_user.id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific student"""
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.user_id == current_user.id
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/{student_id}/metrics", response_model=AcademicMetricResponse)
async def record_metrics(
    student_id: int,
    metrics: AcademicMetricCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record academic metrics for a student"""
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.user_id == current_user.id
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db_metric = AcademicMetric(**metrics.dict(), student_id=student_id)
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@router.get("/{student_id}/metrics", response_model=List[AcademicMetricResponse])
async def get_metrics(
    student_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get metrics history for a student"""
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.user_id == current_user.id
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    metrics = db.query(AcademicMetric).filter(
        AcademicMetric.student_id == student_id
    ).order_by(AcademicMetric.recorded_date.desc()).offset(skip).limit(limit).all()
    return metrics
```

---

## Frontend: src/services/api.js

```javascript
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth endpoints
export const authAPI = {
  register: (username, email, password) =>
    api.post('/auth/register', { username, email, password }),
  login: (username, password) =>
    api.post('/auth/login', { username, password }),
  getCurrentUser: () => api.get('/auth/me'),
};

// Student endpoints
export const studentsAPI = {
  list: (skip = 0, limit = 10) =>
    api.get('/students', { params: { skip, limit } }),
  get: (id) => api.get(`/students/${id}`),
  create: (student) => api.post('/students', student),
  update: (id, student) => api.put(`/students/${id}`, student),
  delete: (id) => api.delete(`/students/${id}`),
};

// Metrics endpoints
export const metricsAPI = {
  record: (studentId, metrics) =>
    api.post(`/students/${studentId}/metrics`, metrics),
  list: (studentId, skip = 0, limit = 10) =>
    api.get(`/students/${studentId}/metrics`, { params: { skip, limit } }),
  getLatest: (studentId) =>
    api.get(`/students/${studentId}/metrics/latest`),
};

// Prediction endpoints
export const predictionsAPI = {
  predict: (studentIds) =>
    api.post('/predictions/predict', { student_ids: studentIds }),
  list: (studentId, skip = 0, limit = 10) =>
    api.get(`/students/${studentId}/predictions`, { params: { skip, limit } }),
  getLatest: (studentId) =>
    api.get(`/students/${studentId}/predictions/latest`),
};

export default api;
```

---

## Frontend: src/context/AuthContext.jsx

```javascript
import React, { createContext, useState, useContext, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Check if user is already logged in
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const response = await authAPI.getCurrentUser();
          setUser(response.data);
        } catch (err) {
          localStorage.removeItem('access_token');
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (username, password) => {
    try {
      setError(null);
      const response = await authAPI.login(username, password);
      localStorage.setItem('access_token', response.data.access_token);
      setUser(response.data.user);
      return true;
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
      return false;
    }
  };

  const register = async (username, email, password) => {
    try {
      setError(null);
      const response = await authAPI.register(username, email, password);
      localStorage.setItem('access_token', response.data.access_token);
      setUser(response.data.user);
      return true;
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, error, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

---

## Frontend: src/App.jsx

```javascript
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import LoginPage from './pages/LoginPage';
import StudentsPage from './pages/StudentsPage';
import StudentDetailPage from './pages/StudentDetailPage';

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) return <div>Loading...</div>;
  if (!user) return <Navigate to="/login" />;

  return children;
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/students"
            element={
              <ProtectedRoute>
                <StudentsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/students/:id"
            element={
              <ProtectedRoute>
                <StudentDetailPage />
              </ProtectedRoute>
            }
          />
          <Route path="/" element={<Navigate to="/students" />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
```

---

## Backend: app/ml_model/train.py (Simple Example)

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Create sample training data
data = {
    'attendance_rate': [95, 75, 60, 85, 70, 90, 55, 88],
    'gpa': [3.8, 3.2, 2.5, 3.5, 2.8, 3.9, 2.0, 3.6],
    'assignment_completion_rate': [100, 80, 60, 90, 75, 95, 50, 85],
    'test_score_average': [92, 78, 65, 85, 72, 90, 58, 88],
    'behavioral_score': [85, 75, 55, 80, 65, 90, 45, 85],
    'risk_level': [0, 0, 2, 0, 1, 0, 2, 0],  # 0=low, 1=medium, 2=high
}

df = pd.DataFrame(data)

# Features and target
X = df[['attendance_rate', 'gpa', 'assignment_completion_rate', 'test_score_average', 'behavioral_score']]
y = df['risk_level']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocess
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
score = model.score(X_test_scaled, y_test)
print(f"Model accuracy: {score:.2f}")

# Save
model_dir = os.path.dirname(__file__)
joblib.dump(model, os.path.join(model_dir, 'model.pkl'))
joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))
print("Model saved!")
```

---

## Notes

- These are **templates** - adapt to your needs
- Start with auth first, then students, then predictions
- Test as you build
- Keep it simple - add features incrementally
- Use the checklist to track progress

Good luck! 🚀
