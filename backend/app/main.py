from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.db import engine, Base
from app.config import settings
from app.routes.auth import router as auth_router

# Create all database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Student Performance Tracker",
    description="ML-powered student risk prediction API",
    version="1.0.0"
)

# Add CORS middleware (allows frontend to communicate with backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

# Include auth routes
app.include_router(auth_router)

# Startup event
@app.on_event("startup")
async def startup_event():
    print("✅ FastAPI server started")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    print("👋 FastAPI server shutting down")