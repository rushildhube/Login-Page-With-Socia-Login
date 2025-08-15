from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from .app.security import settings
from .app.database import init_db
# --- THIS IS THE CRITICAL CHANGE ---
# Make sure 'admin' is imported from the routers.
from .app.routers import auth, users, admin
# --- END OF CHANGE ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="Enhanced Auth API",
    description="A secure authentication service with social login and RBAC.",
    version="1.0.0",
    lifespan=lifespan
)

# Critical for OAuth state via cookies on localhost redirects
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.JWT_SECRET_KEY,
    same_site="lax",      # allows cookie on external redirect back to localhost
    https_only=False,     # True only behind HTTPS (prod)
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
# --- THIS IS THE CRITICAL CHANGE ---
# Make sure the admin router is included in the application.
app.include_router(admin.router)
# --- END OF CHANGE ---

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Full-Featured Custom Login API"}
