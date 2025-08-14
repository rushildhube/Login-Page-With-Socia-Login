from typing import Optional
from beanie import Document, Indexed
from pydantic import EmailStr, Field
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(Document):
    email: Indexed(EmailStr, unique=True)
    full_name: Optional[str] = None
    hashed_password: Optional[str] = None
    refresh_token: Optional[str] = None
    role: UserRole = Field(default=UserRole.USER)
    is_verified: bool = Field(default=False)
    verification_token: Optional[str] = Field(default=None, index=True)

    class Settings:
        name = "users"

# --- NEW MODEL FOR ADMIN DASHBOARD ---
class LoginHistory(Document):
    """
    Represents a login event in the database.
    This collection will store a record for each successful login.
    """
    user_email: Indexed(EmailStr)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    login_type: str # e.g., "password", "google", "github"

    class Settings:
        name = "login_history"
# --- END NEW MODEL ---
