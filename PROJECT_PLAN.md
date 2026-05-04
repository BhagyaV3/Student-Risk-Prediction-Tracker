# Student Risk Prediction Web Application - Project Plan

## 1. Folder Structure

```
student-performance-tracker/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── config.py               # Configuration
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── student.py          # SQLAlchemy models
│   │   │   ├── prediction.py
│   │   │   └── attendance.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── student.py          # Pydantic schemas
│   │   │   ├── prediction.py
│   │   │   └── common.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── students.py         # Student CRUD endpoints
│   │   │   ├── predictions.py      # Prediction endpoints
│   │   │   ├── auth.py             # Login/register
│   │   │   └── health.py           # Health check
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ml_service.py       # ML model operations
│   │   │   ├── student_service.py  # Business logic
│   │   │   └── auth_service.py
│   │   ├── ml_model/
│   │   │   ├── __init__.py
│   │   │   ├── model.pkl           # Trained model (gitignored)
│   │   │   ├── scaler.pkl          # Feature scaler
│   │   │   ├── train.py            # Model training script
│   │   │   └── utils.py            # Feature engineering
│   │   └── database/
│   │       ├── __init__.py
│   │       └── db.py               # Database connection
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_routes.py
│   │   ├── test_services.py
│   │   └── test_ml.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── StudentList.jsx
│   │   │   ├── StudentForm.jsx
│   │   │   ├── RiskCard.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Header.jsx
│   │   │   └── LoginForm.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Students.jsx
│   │   │   ├── StudentDetail.jsx
│   │   │   └── NotFound.jsx
│   │   ├── services/
│   │   │   ├── api.js             # API client
│   │   │   └── auth.js
│   │   ├── hooks/
│   │   │   ├── useStudents.js
│   │   │   ├── usePredictions.js
│   │   │   └── useAuth.js
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   ├── styles/
│   │   │   ├── App.css
│   │   │   └── components.css
│   │   ├── App.jsx
│   │   ├── index.jsx
│   │   └── .env.example
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   ├── .gitignore
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 2. Database Schema

```sql
-- Users/Teachers
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    student_id VARCHAR(50),
    enrollment_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, student_id)
);

-- Student Academic Metrics (captured at regular intervals)
CREATE TABLE academic_metrics (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    attendance_rate FLOAT,  -- 0-100
    gpa FLOAT,              -- 0-4.0
    assignment_completion_rate FLOAT,  -- 0-100
    test_score_average FLOAT,  -- 0-100
    behavioral_score FLOAT,    -- subjective or quantitative
    recorded_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Risk Predictions
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    risk_level VARCHAR(20) NOT NULL,  -- 'LOW', 'MEDIUM', 'HIGH'
    risk_score FLOAT NOT NULL,         -- 0-1
    model_version VARCHAR(50),
    contributing_factors JSONB,        -- JSON: {"attendance": 0.8, "gpa": -0.3, ...}
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Action Log (interventions, notes)
CREATE TABLE action_logs (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    action_type VARCHAR(50),  -- 'intervention', 'note', 'follow_up'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id)
);

-- Indexes for performance
CREATE INDEX idx_students_user_id ON students(user_id);
CREATE INDEX idx_academic_metrics_student_id ON academic_metrics(student_id);
CREATE INDEX idx_academic_metrics_date ON academic_metrics(recorded_date);
CREATE INDEX idx_predictions_student_id ON predictions(student_id);
CREATE INDEX idx_predictions_date ON predictions(predicted_at);
CREATE INDEX idx_action_logs_student_id ON action_logs(student_id);
```

---

## 3. API Routes

### Authentication
- `POST /api/auth/register` - Register teacher account
- `POST /api/auth/login` - Login (returns JWT)
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

### Students
- `GET /api/students` - List all students (with pagination)
- `POST /api/students` - Add new student
- `GET /api/students/{id}` - Get student details
- `PUT /api/students/{id}` - Update student info
- `DELETE /api/students/{id}` - Delete student

### Academic Metrics
- `POST /api/students/{id}/metrics` - Record academic metrics
- `GET /api/students/{id}/metrics` - Get metrics history (paginated)
- `GET /api/students/{id}/metrics/latest` - Get latest metrics

### Predictions
- `POST /api/predictions/predict` - Trigger prediction for student(s)
- `GET /api/students/{id}/predictions` - Get prediction history
- `GET /api/students/{id}/predictions/latest` - Get latest prediction

### Dashboard
- `GET /api/dashboard/summary` - Get overall statistics
  - Total students, avg risk score, students by risk level
- `GET /api/dashboard/at-risk` - Get high-risk students
- `GET /api/dashboard/trends` - Get trends over time

### Action Logs
- `POST /api/students/{id}/actions` - Log an action/intervention
- `GET /api/students/{id}/actions` - Get action history

### Health
- `GET /api/health` - Health check endpoint

---

## 4. MVP Features

### Phase 1 (Weeks 1-3): Foundation
- User authentication (teacher login/register)
- Student CRUD operations
- Simple database setup
- Basic API structure

### Phase 2 (Weeks 4-6): Data & ML
- Academic metrics input form
- Initial ML model (predict risk based on current metrics)
- Prediction endpoint
- Model training script

### Phase 3 (Weeks 7-9): Frontend
- Login page
- Student list view
- Student detail page with metrics
- Risk visualization (color coding, risk score)
- Add/edit student form

### Phase 4 (Weeks 10-12): Polish & Deploy
- Dashboard with summary stats
- At-risk students view
- Action logging & intervention tracking
- Containerization (Docker)
- Basic testing
- Deployment

### Key MVP Features:
✅ Authentication (teacher accounts)
✅ Student management
✅ Academic metrics tracking
✅ Risk prediction (binary/multi-class: LOW, MEDIUM, HIGH)
✅ Simple visualization
✅ Action logging
❌ Historical trend analysis (post-MVP)
❌ Advanced ML features (post-MVP)
❌ Mobile app (post-MVP)

---

## 5. ML Model Approach (Scikit-learn)

### Training Dataset
- Use synthetic or sample data initially
- Features: attendance, GPA, assignment completion, test scores, behavior
- Target: risk_level (0=low, 1=medium, 2=high) or risk_score (0-1)

### Model Pipeline
```python
# Simple but effective for MVP
RandomForestClassifier or LogisticRegression
└── With StandardScaler preprocessing
└── Feature importance tracking
```

### Making Predictions
```
Input: Latest academic metrics for a student
Process: 
  1. Load trained model & scaler
  2. Preprocess metrics
  3. Get prediction + confidence
Output: {"risk_level": "HIGH", "risk_score": 0.87, "factors": {...}}
```

---

## 6. Implementation Order (Recommended Timeline)

### Week 1-2: Backend Setup & Auth
- [ ] Set up FastAPI project structure
- [ ] PostgreSQL database setup
- [ ] User authentication (JWT-based)
- [ ] Database models & migrations
- [ ] Basic CRUD endpoints for students

### Week 3-4: Student Management & Metrics
- [ ] Complete student management endpoints
- [ ] Academic metrics endpoints
- [ ] Input validation with Pydantic
- [ ] Database queries optimized

### Week 5-6: ML Model
- [ ] Create training dataset (synthetic or sample)
- [ ] Train initial ML model
- [ ] Model serialization (save/load)
- [ ] Prediction endpoint
- [ ] Feature engineering utilities

### Week 7-8: Frontend - Core Pages
- [ ] React project setup
- [ ] Authentication flow (login/register)
- [ ] API client (axios/fetch wrapper)
- [ ] Student list page
- [ ] Student detail page

### Week 9-10: Frontend - Features
- [ ] Student form (add/edit)
- [ ] Metrics input form
- [ ] Risk visualization
- [ ] Dashboard with summary stats

### Week 11-12: Polish & Deployment
- [ ] Docker setup (backend, frontend, postgres)
- [ ] Basic unit tests
- [ ] Error handling & validation
- [ ] Documentation
- [ ] Docker Compose orchestration
- [ ] Deploy to cloud (optional: Heroku, Railway, etc.)

---

## 7. Technology Choices Explained

| Tech | Why | Notes |
|------|-----|-------|
| FastAPI | Fast, modern, auto-docs, great for APIs | Built-in OpenAPI docs at `/docs` |
| React | Industry standard, component-based | Vite or Create React App for setup |
| PostgreSQL | Relational, reliable, free | Perfect for structured data |
| scikit-learn | Simple, mature, great for tabular data | No overkill with TensorFlow for MVP |
| Docker | Reproducible environments | Makes deployment consistent |

---

## 8. Key Simplicity Decisions

✅ **JWT authentication** (not OAuth) - simpler for solo project
✅ **REST API** (not GraphQL) - easier to implement/test
✅ **Pydantic for validation** - minimal config
✅ **SQLAlchemy ORM** - handles database complexity
✅ **Random Forest model** - interpretable, good baseline
✅ **No microservices** - monolithic backend
✅ **Docker Compose** (not Kubernetes) - simpler deployment
✅ **Sqlite in dev, PostgreSQL in prod** - flexibility

---

## 9. Development Tips

- Use `.env` files for secrets (not in git)
- Test locally before committing
- Start with mock data; add real data input later
- Version your ML models (model_v1, model_v2)
- Use git commits regularly
- Document as you go (docstrings, API comments)

---

## 10. Success Metrics for MVP

- ✅ Teachers can create accounts and log in
- ✅ Add/view/edit students
- ✅ Input academic metrics
- ✅ System predicts risk level for each student
- ✅ See risk predictions on dashboard
- ✅ Log interventions
- ✅ All containerized and runnable via Docker

**You do NOT need for MVP:**
- ❌ Mobile app
- ❌ Multi-tenant support
- ❌ Advanced analytics
- ❌ Real-time updates
- ❌ 99.9% uptime SLA
