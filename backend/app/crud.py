from typing import Optional
from .models import User, LoginHistory, UserRole
from .schemas import UserCreate
from .security import get_password_hash

async def get_user_by_email(email: str) -> Optional[User]:
    """
    Asynchronously finds a user by email and ensures a default role exists.
    """
    user = await User.find_one(User.email == email)
    
    # --- THIS IS THE CRITICAL CHANGE ---
    # This is a "lazy migration". If an old user document is found without a role,
    # this code assigns the default 'user' role and saves it back to the database.
    if user and user.role is None:
        user.role = UserRole.USER
        await user.save()
    # --- END OF CHANGE ---
        
    return user

async def create_user(user: UserCreate) -> User:
    """
    Creates a new user in the database with a hashed password.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    await db_user.insert()
    return db_user

async def create_social_user(email: str, name: str) -> User:
    """
    Creates a new user in the database for social logins.
    """
    db_user = User(email=email, full_name=name)
    await db_user.insert()
    return db_user

async def create_login_record(email: str, login_type: str, ip_address: str, user_agent: str):
    """
    Creates a new login history record in the database with additional details.
    """
    login_record = LoginHistory(
        user_email=email, 
        login_type=login_type,
        ip_address=ip_address,
        user_agent=user_agent
    )
    await login_record.insert()
