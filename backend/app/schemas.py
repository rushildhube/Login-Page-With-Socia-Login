from pydantic import BaseModel, EmailStr
from typing import Optional
from .models import UserRole

# ===================================================================
# Schemas for User Operations
# ===================================================================

class UserCreate(BaseModel):
    """
    Schema for creating a new user (request model).
    This defines the data required in the request body for the /signup endpoint.
    """
    email: EmailStr
    password: str
    full_name: str

class UserPublic(BaseModel):
    """
    Schema for public user data (response model).
    This defines the data that is safe to send back to the client.
    It explicitly excludes sensitive information like the hashed password.
    """
    id: str  # MongoDB IDs are typically strings
    email: EmailStr
    full_name: Optional[str] = None
    role: UserRole

# ===================================================================
# Schemas for Token Operations
# ===================================================================

class Token(BaseModel):
    """
    Base schema for an access token response.
    """
    access_token: str
    token_type: str

class TokenResponse(Token):
    """
    Schema for the full token response, including the refresh token.
    This is returned to the client upon successful login.
    """
    refresh_token: str

class RefreshTokenRequest(BaseModel):
    """
    Schema for the refresh token request body.
    This defines the data required to request a new access token.
    """
    refresh_token: str
