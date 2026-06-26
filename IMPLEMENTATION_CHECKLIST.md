# Implementation Checklist

## Week 1-2: Backend Setup & Authentication

### Infrastructure
- [x] Set up FastAPI project structure
- [x] Create virtual environment and install dependencies
- [x] Set up PostgreSQL database (local or Docker)
- [x] Create `.env` file with database credentials

### Database & Models
- [x] Design database schema
- [x] Create SQLAlchemy models for User, Student
- [ ] Set up Alembic migrations (deferred to Phase 2)
- [ ] Run initial migration (deferred to Phase 2)

### Authentication
- [x] Implement JWT token generation/validation
- [x] Create password hashing (bcrypt)
- [x] Build `POST /api/auth/register` endpoint
- [x] Build `POST /api/auth/login` endpoint
- [x] Add JWT middleware/dependency injection
- [x] Test authentication flow (manual or pytest)

### Project Structure
- [x] Organize code into app/routes, app/schemas, app/services
- [x] Add basic error handling
- [x] Set up logging
- [x] Add CORS configuration for frontend

### Basic Endpoints
- [x] `GET /api/health` - health check
- [x] `GET /api/auth/me` - get current user
- [x] Test all endpoints work

---

## Week 3-4: Student Management & Metrics

### Student CRUD
- [x] Create Student SQLAlchemy model
- [x] Build `POST /api/students` (add student)
- [x] Build `GET /api/students` (list students with pagination)
- [x] Build `GET /api/students/{id}` (view single student)
- [x] Build `PUT /api/students/{id}` (update student)
- [x] Build `DELETE /api/students/{id}` (delete student)
- [x] Add validation with Pydantic schemas
- [x] Add authorization (teacher can only see their own students)

### Academic Metrics
- [x] Create AcademicMetrics SQLAlchemy model
- [x] Build `POST /api/students/{id}/metrics` (record metrics)
- [x] Build `GET /api/students/{id}/metrics` (list metrics with pagination)
- [x] Build `GET /api/students/{id}/metrics/latest` (get most recent)
- [x] Add validation (0-100 for percentages, 0-4.0 for GPA, etc.)

### Testing
- [x] Write pytest tests for student endpoints
- [x] Write pytest tests for metrics endpoints
- [x] Test authorization (ensure only teacher can access their data)
- [x] Achieve >80% code coverage

### Documentation
- [x] Add docstrings to all functions
- [x] Document API endpoint behavior
- [x] Verify Swagger docs at `/docs` are clear

---

## Week 5-6: ML Model & Predictions

### Data Preparation
- [ ] Create sample/synthetic training data (if needed)
- [ ] Define features: attendance, GPA, assignment completion, test scores, behavior
- [ ] Define target: risk_level (0=low, 1=medium, 2=high) or risk_score (0-1)
- [ ] Create train/test split (80/20 or similar)

### Model Development
- [ ] Explore data with pandas
- [ ] Build feature engineering pipeline
- [ ] Train Random Forest classifier (baseline)
- [ ] Evaluate model (accuracy, precision, recall, F1)
- [ ] Save model and scaler as `.pkl` files
- [ ] Create `train.py` script for reproducibility

### ML Service Integration
- [ ] Create `ml_service.py` to load and use model
- [ ] Implement feature extraction from student metrics
- [ ] Implement prediction function
- [ ] Handle edge cases (missing data, new students)
- [ ] Add confidence scores

### Prediction Endpoints
- [ ] Build `POST /api/predictions/predict` (predict for student(s))
- [ ] Build `GET /api/students/{id}/predictions` (prediction history)
- [ ] Build `GET /api/students/{id}/predictions/latest` (most recent)
- [ ] Store predictions in database with timestamp
- [ ] Store feature contributions (SHAP or feature importance)

### Testing & Validation
- [ ] Write tests for ML service
- [ ] Validate predictions make sense
- [ ] Test edge cases (missing data, extreme values)
- [ ] Document model assumptions

---

## Week 7-8: Frontend - Core Pages

### Project Setup
- [ ] Create React app with Vite
- [ ] Set up routing (react-router-dom)
- [ ] Create basic layout/header component
- [ ] Add CSS/styling (Tailwind or basic CSS)

### Authentication UI
- [ ] Build login form component
- [ ] Build register form component
- [ ] Build login page
- [ ] Implement authentication context/state management
- [ ] Store JWT token (localStorage)
- [ ] Add protected routes (redirect to login if not authenticated)

### API Client
- [ ] Create axios wrapper/service for API calls
- [ ] Handle authentication headers (JWT)
- [ ] Handle error responses
- [ ] Add request/response interceptors

### Student List Page
- [ ] Create student list component
- [ ] Fetch students from backend
- [ ] Display in table/card format
- [ ] Add pagination
- [ ] Add search/filter by name
- [ ] Add delete functionality

### Student Detail Page
- [ ] Create student detail component
- [ ] Show student info
- [ ] Show recent metrics
- [ ] Show latest prediction (risk level, score)
- [ ] Show risk contributing factors
- [ ] Add edit button to go to edit form

### Testing & Polish
- [ ] Test all components load correctly
- [ ] Check responsive design (mobile/tablet)
- [ ] Fix any console errors
- [ ] Add loading states

---

## Week 9-10: Frontend - Features & Integration

### Student Form
- [ ] Create add student form
- [ ] Create edit student form
- [ ] Form validation (required fields, email format)
- [ ] Success/error messages
- [ ] Redirect after save

### Metrics Form
- [ ] Create form to input academic metrics
- [ ] Validate inputs (0-100 for percentages, etc.)
- [ ] Show recent metric history below form
- [ ] Success message after save

### Prediction Trigger
- [ ] Add button to generate/refresh prediction
- [ ] Show loading state during prediction
- [ ] Display risk level with color coding (red=high, yellow=medium, green=low)
- [ ] Show risk score (percentage)
- [ ] Display contributing factors

### Dashboard Page
- [ ] Show summary statistics
  - [ ] Total students
  - [ ] Students by risk level
  - [ ] Average risk score
- [ ] Show list of at-risk students (HIGH risk)
- [ ] Add filters (show MEDIUM too, date range)
- [ ] Add export functionality (optional)

### Navigation & UX
- [ ] Add navigation menu/sidebar
- [ ] Add logout button
- [ ] Add breadcrumbs
- [ ] Add confirmation dialogs for delete actions
- [ ] Add empty states (no students, etc.)

### Testing & Polish
- [ ] Test all forms work end-to-end
- [ ] Check error handling (network errors, validation)
- [ ] Test on different browsers
- [ ] Optimize images/assets
- [ ] Add loading skeletons

---

## Week 11-12: Polish, Testing & Deployment

### Backend Improvements
- [ ] Add comprehensive error handling
- [ ] Add logging
- [ ] Add request validation
- [ ] Add rate limiting (optional)
- [ ] Write integration tests
- [ ] Add database migrations guide

### Frontend Improvements
- [ ] Add error boundaries
- [ ] Add global loading/notification system
- [ ] Add confirmation dialogs
- [ ] Optimize bundle size
- [ ] Add PWA features (optional)
- [ ] Add accessibility features (alt text, ARIA labels)

### Testing
- [ ] Backend: pytest for all endpoints
- [ ] Frontend: Jest/React Testing Library (basic tests)
- [ ] Manual testing of full user flow
- [ ] Test in multiple browsers

### Documentation
- [ ] Add API documentation (auto via Swagger at `/docs`)
- [ ] Add README with setup instructions
- [ ] Add deployment guide
- [ ] Document database schema
- [ ] Document API endpoints

### Docker & Deployment
- [ ] Verify Docker setup works
- [ ] `docker-compose up -d` starts all services
- [ ] All containers healthy
- [ ] Test full application flow in Docker

### Deployment Options
- [ ] **Backend**: Heroku, Railway, or Render (free tier)
- [ ] **Frontend**: Vercel or Netlify (free tier)
- [ ] **Database**: PostgreSQL on Heroku, Railway, or AWS RDS (free tier)
- [ ] Deploy and verify everything works

### Final Checks
- [ ] All features working
- [ ] No console errors
- [ ] Tests passing
- [ ] Code formatted (black, eslint)
- [ ] Documentation complete
- [ ] Git history clean with good commit messages

---

## Bonus/Post-MVP Features

- [ ] Historical trend analysis
- [ ] Predictive trends (will this student be at risk next month?)
- [ ] Export student data to CSV
- [ ] Multi-class classification (detailed risk categories)
- [ ] Automated email alerts for at-risk students
- [ ] Teacher dashboard with insights
- [ ] Student self-service view (with permissions)
- [ ] Mobile app
- [ ] Advanced ML (ensemble models, XGBoost)

---

## Progress Tracker

### Week 1-2 Progress: 40/100
### Week 3-4 Progress: ___/100
### Week 5-6 Progress: ___/100
### Week 7-8 Progress: ___/100
### Week 9-10 Progress: ___/100
### Week 11-12 Progress: ___/100

**Overall Completion**: ___/100%

---

## Notes

- Keep commits focused and descriptive
- Test as you build (don't leave testing for the end)
- Get feedback early from potential users
- Document as you go
- It's okay if not everything is perfect - prioritize core features
- Have fun and learn as you build! 🚀
