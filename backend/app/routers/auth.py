# backend/app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from authlib.integrations.starlette_client import OAuthError
import secrets
from urllib.parse import urlencode
from datetime import datetime, timedelta

# --- MODIFIED: Added email_utils import ---
from .. import crud, models, schemas, security, email_utils

router = APIRouter(prefix="/auth", tags=["Authentication"])

FRONTEND_SUCCESS_URL = security.settings.FRONTEND_SUCCESS_URL
FRONTEND_ERROR_URL   = security.settings.FRONTEND_ERROR_URL

# In-memory store for rate limiting (for production, use Redis)
failed_attempts = {}
RATE_LIMIT_ATTEMPTS = 5
RATE_LIMIT_TIMEFRAME = timedelta(minutes=15)

def _success_url(params: dict) -> str:
    """Helper to build the success URL with query parameters."""
    return f"{FRONTEND_SUCCESS_URL}?{urlencode(params)}"

def _error_url(reason: str) -> str:
    """Helper to build the error URL with a reason."""
    return f"{FRONTEND_ERROR_URL}?error={reason}"

def create_public_user(user: models.User) -> schemas.UserPublic:
    """Helper to convert a User model to a public-safe schema."""
    return schemas.UserPublic(
        id=str(user.id), 
        email=user.email, 
        full_name=user.full_name, 
        role=user.role
    )

@router.post("/signup", response_model=schemas.UserPublic)
async def signup(user: schemas.UserCreate, background_tasks: BackgroundTasks):
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = await crud.create_user(user=user)
    
    verification_token = security.create_verification_token({"sub": new_user.email})
    new_user.verification_token = verification_token
    await new_user.save()
    
    verification_link = f"http://127.0.0.1:5500/frontend/verify.html?token={verification_token}"
    
    # --- FIXED: Send email in the background instead of printing ---
    email_subject = "Verify Your Email Address"
    email_body = f"""
    <h1>Welcome to Sniperthink!</h1>
    <p>Thanks for signing up. Please click the link below to verify your email address:</p>
    <a href="{verification_link}" style="display:inline-block; padding:10px 20px; background-color:#007bff; color:white; text-decoration:none; border-radius:5px;">Verify Email</a>
    <p>If you did not create an account, you can safely ignore this email.</p>
    """
    background_tasks.add_task(
        email_utils.send_email,
        to_email=new_user.email,
        subject=email_subject,
        body=email_body
    )
    # --- END FIX ---
    
    return create_public_user(new_user)

@router.post("/token", response_model=schemas.TokenResponse)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    ip_address = request.client.host
    
    # Rate Limiting Check
    now = datetime.utcnow()
    if ip_address in failed_attempts:
        attempts = [t for t in failed_attempts[ip_address] if now - t < RATE_LIMIT_TIMEFRAME]
        if len(attempts) >= RATE_LIMIT_ATTEMPTS:
            raise HTTPException(status_code=429, detail="Too many failed login attempts. Please try again later.")
        failed_attempts[ip_address] = attempts

    user = await crud.get_user_by_email(email=form_data.username)
    if not user or not user.hashed_password or not security.verify_password(form_data.password, user.hashed_password):
        # Record failed attempt
        if ip_address not in failed_attempts:
            failed_attempts[ip_address] = []
        failed_attempts[ip_address].append(now)
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Email not verified.")
    
    # Clear failed attempts on successful login
    if ip_address in failed_attempts:
        del failed_attempts[ip_address]

    user_agent = request.headers.get("user-agent")
    await crud.create_login_record(
        email=user.email, 
        login_type="password",
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    access_token = security.create_access_token(data={"sub": user.email})
    refresh_token = security.create_refresh_token(data={"sub": user.email})
    user.refresh_token = refresh_token
    await user.save()
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@router.post("/refresh", response_model=schemas.Token)
async def refresh_access_token(body: schemas.RefreshTokenRequest):
    refresh_token = body.refresh_token
    try:
        payload = jwt.decode(refresh_token, security.settings.JWT_SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = await crud.get_user_by_email(email=email)
    if not user or user.refresh_token != refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    new_access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.post("/verify-email")
async def verify_email(token: str):
    try:
        payload = jwt.decode(token, security.settings.JWT_SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    user = await crud.get_user_by_email(email=email)
    if not user or user.verification_token != token:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
        
    user.is_verified = True
    user.verification_token = None
    await user.save()
    
    return {"message": "Email verified successfully."}

@router.post("/forgot-password")
async def forgot_password(email: str, background_tasks: BackgroundTasks):
    user = await crud.get_user_by_email(email=email)
    if user:
        password_reset_token = security.create_verification_token({"sub": user.email})
        user.verification_token = password_reset_token
        await user.save()
        
        reset_link = f"http://127.0.0.1:5500/frontend/reset-password.html?token={password_reset_token}"
        
        # --- FIXED: Send email in the background instead of printing ---
        email_subject = "Reset Your Password"
        email_body = f"""
        <h1>Password Reset Request</h1>
        <p>You requested a password reset. Click the link below to set a new password:</p>
        <a href="{reset_link}" style="display:inline-block; padding:10px 20px; background-color:#007bff; color:white; text-decoration:none; border-radius:5px;">Reset Password</a>
        <p>This link will expire in 1 hour.</p>
        <p>If you did not request a password reset, please ignore this email.</p>
        """
        background_tasks.add_task(
            email_utils.send_email,
            to_email=user.email,
            subject=email_subject,
            body=email_body
        )
        # --- END FIX ---
        
    return {"message": "If an account with that email exists, a password reset link has been sent."}

@router.post("/reset-password")
async def reset_password(token: str, new_password: str):
    try:
        payload = jwt.decode(token, security.settings.JWT_SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
        
    user = await crud.get_user_by_email(email=email)
    if not user or user.verification_token != token:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
        
    user.hashed_password = security.get_password_hash(new_password)
    user.verification_token = None
    await user.save()
    
    return {"message": "Password has been reset successfully."}

# --- Social Login Routes (Unchanged) ---
@router.get("/login/{provider}")
async def social_login(request: Request, provider: str):
    state = secrets.token_urlsafe(32)
    request.session["oauth_state"] = state
    redirect_uri = request.url_for("auth_callback", provider=provider)
    client = security.oauth.create_client(provider)
    return await client.authorize_redirect(request, redirect_uri, state=state)

@router.get("/callback/{provider}", name="auth_callback")
async def auth_callback(request: Request, provider: str):
    expected_state = request.session.pop("oauth_state", None)
    request_state = request.query_params.get("state")

    if not expected_state or not request_state or request_state != expected_state:
        return RedirectResponse(url=_error_url("csrf_state_mismatch"), status_code=303)

    client = security.oauth.create_client(provider)
    try:
        token = await client.authorize_access_token(request)
    except OAuthError as e:
        return RedirectResponse(url=_error_url(f"oauth_error_{e.error}"), status_code=303)
    
    user_info = token.get("userinfo")
    if not user_info and provider == "github":
        user_resp = await security.oauth.github.get("user", token=token)
        user_info = user_resp.json()
        if not user_info.get("email"):
            emails_resp = await security.oauth.github.get("user/emails", token=token)
            user_info["email"] = next((e["email"] for e in emails_resp.json() if e.get("primary")), None)

    user_email = user_info.get("email") if user_info else None
    if not user_email:
        return RedirectResponse(url=_error_url("email_unavailable"), status_code=303)

    user = await crud.get_user_by_email(email=user_email)
    if not user:
        name = user_info.get("name") or user_info.get("login") or user_email.split("@")[0]
        user = await crud.create_social_user(email=user_email, name=name)
    
    user.is_verified = True
    
    ip_address = request.client.host
    user_agent = request.headers.get("user-agent")
    await crud.create_login_record(
        email=user.email, 
        login_type=provider,
        ip_address=ip_address,
        user_agent=user_agent
    )

    access_token = security.create_access_token({"sub": user.email})
    refresh_token = security.create_refresh_token({"sub": user.email})
    user.refresh_token = refresh_token
    await user.save()

    return RedirectResponse(
        url=_success_url({"token": access_token, "refresh_token": refresh_token}),
        status_code=303
    )