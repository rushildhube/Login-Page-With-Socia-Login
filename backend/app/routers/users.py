from fastapi import APIRouter, Depends
from typing import List
from .. import models, schemas, security

# Create a new router object for user-related endpoints
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me", response_model=schemas.UserPublic)
async def read_users_me(current_user: models.User = Depends(security.get_current_user)):
    """
    Endpoint to get the profile of the currently authenticated user.
    The `get_current_user` dependency ensures that this route is protected
    and only accessible with a valid access token.
    """
    # The dependency returns the full user model, which we convert to a
    # public-safe schema before returning it to the client.
    return schemas.UserPublic(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role
    )

@router.get("/all", response_model=List[schemas.UserPublic], dependencies=[Depends(security.require_role("admin"))])
async def read_all_users():
    """
    Admin-only endpoint to get a list of all users in the database.
    The `require_role("admin")` dependency protects this route, ensuring
    only users with the 'admin' role can access it.
    """
    # Fetch all user documents from the database
    all_users = await models.User.find_all().to_list()
    
    # Convert each user document to the public schema to avoid exposing sensitive data
    return [schemas.UserPublic(id=str(user.id), email=user.email, full_name=user.full_name, role=user.role) for user in all_users]
