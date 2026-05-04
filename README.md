# Student Risk Prediction Tracker

A web application that predicts student academic risk based on performance metrics, enabling teachers to identify at-risk students early and take targeted interventions.

## 📋 Project Overview

**Tech Stack**: React | FastAPI | PostgreSQL | scikit-learn | Docker

**Timeline**: 4 months (12 weeks)

**Scope**: Solo student project with internship-level complexity

## 🎯 MVP Features

- 👤 Teacher authentication (login/register)
- 📚 Student management (CRUD operations)
- 📊 Academic metrics tracking (attendance, GPA, assignments, test scores)
- 🤖 AI-powered risk prediction (LOW, MEDIUM, HIGH)
- 📈 Dashboard with at-risk student list
- 🔍 Risk visualization & contributing factors
- 📝 Intervention logging & follow-up tracking

## 📁 Project Structure

```
backend/              # FastAPI backend
├── app/
│   ├── routes/       # API endpoints
│   ├── models/       # Database models
│   ├── schemas/      # Request validation
│   ├── services/     # Business logic
│   └── ml_model/     # ML training/inference
├── tests/            # Unit tests
├── requirements.txt
└── Dockerfile

frontend/             # React UI
├── src/
│   ├── components/   # Reusable components
│   ├── pages/        # Page components
│   ├── services/     # API client
│   └── hooks/        # Custom hooks
├── package.json
└── Dockerfile

docker-compose.yml    # Orchestration
```

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
docker-compose up -d
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

See [QUICK_START.md](./QUICK_START.md) for detailed setup.

## 📅 Implementation Timeline

| Week | Phase | Focus |
|------|-------|-------|
| 1-2 | Setup | Backend structure, authentication, database |
| 3-4 | CRUD | Student management, metrics endpoints |
| 5-6 | ML | Model training, prediction service |
| 7-8 | Frontend | Login, student list, detail pages |
| 9-10 | Integration | Connect frontend to backend, UI polish |
| 11-12 | Polish | Testing, documentation, deployment |

See [PROJECT_PLAN.md](./PROJECT_PLAN.md) for detailed breakdown.

## 🗄️ Database Schema

**Key Tables:**
- `users` - Teacher accounts
- `students` - Student data
- `academic_metrics` - Performance records (attendance, GPA, etc.)
- `predictions` - Risk predictions with scores
- `action_logs` - Intervention tracking

See [PROJECT_PLAN.md](./PROJECT_PLAN.md) for full schema.

## 🔌 API Endpoints

**Authentication:**
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Login

**Students:**
- `GET/POST /api/students` - List/create students
- `GET/PUT/DELETE /api/students/{id}` - View/update/delete student

**Metrics & Predictions:**
- `POST /api/students/{id}/metrics` - Record metrics
- `GET /api/students/{id}/metrics` - View metrics history
- `POST /api/predictions/predict` - Generate prediction
- `GET /api/students/{id}/predictions/latest` - Get latest prediction

**Dashboard:**
- `GET /api/dashboard/summary` - Overall statistics
- `GET /api/dashboard/at-risk` - High-risk students

See [PROJECT_PLAN.md](./PROJECT_PLAN.md) for full API reference.

## 🤖 ML Model

**Approach**: scikit-learn Random Forest Classifier

**Features**:
- Attendance rate
- GPA
- Assignment completion rate
- Test score average
- Behavioral score

**Output**: Risk level (LOW, MEDIUM, HIGH) + confidence score

**Usage**:
```python
from app.ml_model import predict_risk
risk = predict_risk(metrics)  # {"risk_level": "HIGH", "risk_score": 0.87}
```

## 🛠️ Development Workflow

```bash
# Backend
cd backend
black app/                    # Format
flake8 app/                   # Lint
pytest                        # Test
python -m app.ml_model.train # Train model

# Frontend
cd frontend
npm run lint                  # ESLint
npm run build                 # Production build
```

## 📝 Key Design Decisions

✅ **Simple architecture** - Monolithic backend, no microservices
✅ **JWT authentication** - Lightweight, stateless
✅ **PostgreSQL** - Structured data, great for schemas
✅ **scikit-learn** - Interpretable, no overkill with deep learning
✅ **Docker Compose** - Easy local dev and deployment
✅ **REST API** - Standard, easy to test
✅ **Pydantic** - Minimal validation overhead

## 🧪 Testing

```bash
cd backend
pytest tests/                 # Run all tests
pytest tests/test_routes.py  # Run specific test file
pytest -v                     # Verbose output
```

## 📚 Documentation

- [PROJECT_PLAN.md](./PROJECT_PLAN.md) - Complete project plan with schema, routes, timeline
- [QUICK_START.md](./QUICK_START.md) - Setup and development commands

## 🚢 Deployment

**Development**: `docker-compose up -d`

**Production**: 
- Deploy backend to Heroku/Railway/Render
- Deploy frontend to Vercel/Netlify
- Use managed PostgreSQL (AWS RDS, etc.)

See [QUICK_START.md](./QUICK_START.md) for more.

## 📖 Technology Rationale

| Tech | Why | Docs |
|------|-----|------|
| FastAPI | Modern, async, auto-docs | [fastapi.tiangolo.com](https://fastapi.tiangolo.com) |
| React | Component-based, industry standard | [react.dev](https://react.dev) |
| PostgreSQL | Relational, reliable, free tier available | [postgresql.org](https://postgresql.org) |
| scikit-learn | Simple, interpretable ML | [scikit-learn.org](https://scikit-learn.org) |
| Docker | Reproducible, consistent environments | [docker.com](https://docker.com) |

## ⚠️ Not in MVP (Future Enhancements)

- Mobile app
- Real-time notifications
- Advanced ML features (deep learning)
- Multi-institution support
- Automated interventions
- Detailed analytics dashboard

## 💡 Tips for Success

1. **Start small** - Get authentication working first
2. **Test early** - Write tests as you build
3. **Commit often** - Use git to track progress
4. **Document** - Add docstrings and comments
5. **Iterate** - Get feedback and adjust

## 📞 Getting Help

- **FastAPI Docs**: http://localhost:8000/docs (interactive API explorer)
- **React Docs**: [react.dev](https://react.dev)
- **PostgreSQL**: [postgresql.org/docs](https://postgresql.org/docs)
- **Stack Overflow**: Tag questions with your tech stack

## 📄 License

Solo student project - No license specified

---

**Remember**: This is a realistic internship-level project. Focus on core features, write clean code, and learn as you go. You've got this! 🚀
