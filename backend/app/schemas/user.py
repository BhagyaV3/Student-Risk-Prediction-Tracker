from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserRegister(BaseModel):
    """Schema for user registration"""
    username: str
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "teacher_jane",
                "email": "jane@example.com",
                "password": "securepassword123"
            }
        }

class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "teacher_jane",
                "password": "securepassword123"
            }
        }

class UserResponse(BaseModel):
    """Schema for user response (what we send back)"""
    id: int
    username: str
    email: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model

class TokenResponse(BaseModel):
    """Schema for login response"""
    access_token: str
    token_type: str = "bearer"

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }