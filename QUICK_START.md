# Quick Start Guide

## Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Docker & Docker Compose (optional)

## Local Development Setup

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations (when ready)
python -m alembic upgrade head

# Start FastAPI server
uvicorn app.main:app --reload
# API docs at http://localhost:8000/docs
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
# Opens at http://localhost:5173 (Vite default)
```

### 3. Database Setup (Local PostgreSQL)

```bash
# Create database
createdb student_tracker

# Or via Docker:
docker run --name student_tracker_db \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:14
```

---

## Quick Docker Compose (All-in-one)

```bash
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- FastAPI backend (port 8000)
- React frontend (port 5173)

---

## Project Structure Summary

```
backend/          → FastAPI API
├── app/
│   ├── routes/   → API endpoints
│   ├── models/   → Database models
│   ├── schemas/  → Request/response validation
│   ├── services/ → Business logic
│   └── ml_model/ → ML code
frontend/         → React UI
├── src/
│   ├── components/ → Reusable components
│   ├── pages/      → Page components
│   └── services/   → API client
```

---

## API Endpoints (Initial)

```
POST   /api/auth/register          - Create account
POST   /api/auth/login             - Login
GET    /api/students               - List students
POST   /api/students               - Add student
GET    /api/students/{id}          - Get student
PUT    /api/students/{id}          - Update student
POST   /api/students/{id}/metrics  - Add metrics
GET    /api/students/{id}/metrics  - Get metrics
POST   /api/predictions/predict    - Generate prediction
GET    /api/health                 - Health check
```

---

## Common Commands

### Backend
```bash
cd backend

# Run server
uvicorn app.main:app --reload

# Run tests
pytest

# Format code
black app/

# Lint
flake8 app/

# Train ML model
python -m app.ml_model.train
```

### Frontend
```bash
cd frontend

npm run dev       # Development server
npm run build     # Production build
npm run preview   # Preview build
npm run lint      # ESLint
```

---

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/student_tracker
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api
```

---

## Testing the API

```bash
# Using curl
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"teacher1","email":"t@example.com","password":"pass123"}'

# Or use Swagger UI at http://localhost:8000/docs
```

---

## Next Steps

1. **Week 1**: Set up backend & database
2. **Week 2**: Implement authentication
3. **Week 3-4**: Student CRUD + metrics endpoints
4. **Week 5-6**: ML model training & prediction
5. **Week 7-8**: Frontend scaffolding & pages
6. **Week 9-10**: Connect frontend to backend
7. **Week 11-12**: Testing, polish, deployment

See `PROJECT_PLAN.md` for detailed timeline.
