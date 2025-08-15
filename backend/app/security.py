from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings
from authlib.integrations.starlette_client import OAuth
from pathlib import Path
from .models import User as UserModel

# Robust .env resolution
env_path = Path(__file__).parent.parent / ".env"

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    MONGO_URI: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    FRONTEND_SUCCESS_URL: str = "http://127.0.0.1:5500/frontend/dashboard.html"
    FRONTEND_ERROR_URL: str   = "http://127.0.0.1:5500/frontend/index.html"
    
    # --- NEW: Email Settings ---
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    # --- END NEW ---
    
    class Config:
        env_file = env_path

settings = Settings()
oauth = OAuth()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, hashed_password): return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password): return pwd_context.hash(password)

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
# --- NEW ---
VERIFICATION_TOKEN_EXPIRE_MINUTES = 15 # Token for email/password reset is valid for 15 mins
# --- END NEW ---
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + expires_delta})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(data: dict):  return create_token(data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
def create_refresh_token(data: dict): return create_token(data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

# --- NEW FUNCTION ---
def create_verification_token(data: dict):
    """Creates a short-lived token for email verification or password reset."""
    return create_token(data, timedelta(minutes=VERIFICATION_TOKEN_EXPIRE_MINUTES))
# --- END NEW FUNCTION ---

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    from . import crud
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise cred_exc
    except JWTError:
        raise cred_exc
    
    user = await crud.get_user_by_email(email=email)
    if not user:
        raise cred_exc
    return user

def require_role(required_role: str):
    def checker(current_user: UserModel = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(status_code=403, detail="You do not have permission to access this resource")
        return current_user
    return checker

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
oauth.register(
    name="github",
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)
