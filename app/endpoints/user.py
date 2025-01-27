from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from beanie import PydanticObjectId
from app.models.models import User


router = APIRouter(prefix="/users", tags=["users"])

# User Registration Endpoint
@router.post("/register", response_model=User)
async def register(user: User):
    """
    Register a new user.
    """
    # Check if the email is already registered
    existing_user = await User.find_one(User.email == user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Insert the new user into the database
    await user.insert()
    return user

# User Login Endpoint
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Log in a user and return a JWT token.
    """
    # Find the user by email
    user = await User.find_one(User.email == form_data.username)
    if not user or user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    
    # Generate and return a JWT token
    return {
        "access_token": user.generate_jwt(),
        "token_type": "bearer",
    }



# Get User by ID Endpoint
@router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: PydanticObjectId):
    """
    Get a user by their ID.
    """
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
