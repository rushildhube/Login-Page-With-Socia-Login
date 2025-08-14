from typing import Optional
from typing import Optional
from beanie import Document, Indexed
from pydantic import EmailStr, Field
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(Document):
    email: Indexed(EmailStr, unique=True)
    full_name: Optional[str] = None
    hashed_password: Optional[str] = None
    refresh_token: Optional[str] = None
    role: UserRole = Field(default=UserRole.USER)
    # --- NEW FIELDS ---
    is_verified: bool = Field(default=False)
    verification_token: Optional[str] = Field(default=None, index=True)
    # --- END OF NEW FIELDS ---

    class Settings:
        name = "users"
from .models import User, LoginHistory # Add LoginHistory
from .schemas import UserCreate
from .security import get_password_hash

# --- Functions for User model remain the same ---
async def get_user_by_email(email: str) -> Optional[User]:
    """
    Asynchronously finds a user in the database by their email address.

    Args:
        email: The email of the user to find.

    Returns:
        The User document if found, otherwise None.
    """
    return await User.find_one(User.email == email)

async def create_user(user: UserCreate) -> User:
    """
    Creates a new user in the database with a hashed password.
    This is used for traditional email/password signup.

    Args:
        user: A UserCreate schema object containing the new user's details.

    Returns:
        The newly created User document.
    """
    # Hash the user's password before storing it
    hashed_password = get_password_hash(user.password)
    
    # Create a new User document instance
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    
    # Insert the new user document into the database
    await db_user.insert()
    return db_user

async def create_social_user(email: str, name: str) -> User:
    """
    Creates a new user in the database for social logins.
    These users do not have a password.

    Args:
        email: The email address provided by the social provider.
        name: The full name provided by the social provider.

    Returns:
        The newly created User document.
    """
    db_user = User(email=email, full_name=name)
    await db_user.insert()
    return db_user

# --- NEW FUNCTION ---
async def create_login_record(email: str, login_type: str):
    """
    Creates a new login history record in the database.
    """
    login_record = LoginHistory(user_email=email, login_type=login_type)
    await login_record.insert()
# --- END NEW FUNCTION ---
