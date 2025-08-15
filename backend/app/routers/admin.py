from fastapi import APIRouter, Depends
from typing import List
from .. import models, schemas, security

# Create a new router for admin-only endpoints.
# The `dependencies` parameter ensures that all routes defined in this file
# are protected by the `require_role("admin")` dependency.
router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(security.require_role("admin"))]
)

@router.get("/users", response_model=List[schemas.UserPublic])
async def get_all_users():
    """
    Admin endpoint to get a list of all users in the database.
    """
    all_users = await models.User.find_all().to_list()
    # Convert each user document to the public schema to avoid exposing sensitive data
    return [schemas.UserPublic(id=str(user.id), email=user.email, full_name=user.full_name, role=user.role) for user in all_users]

@router.get("/login-history", response_model=List[models.LoginHistory])
async def get_login_history():
    """
    Admin endpoint to get the 20 most recent login events.
    """
    # Fetch the last 20 login records, sorted by timestamp in descending order
    login_history = await models.LoginHistory.find().sort(-models.LoginHistory.timestamp).limit(20).to_list()
    return login_history
