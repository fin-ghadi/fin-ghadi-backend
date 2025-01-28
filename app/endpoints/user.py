from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from beanie import PydanticObjectId
from pydantic import BaseModel
from app.models.models import User
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the secret key
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



router = APIRouter()

# Define a Pydantic model for the request body
class LoginRequest(BaseModel):
    username: str
    password: str

# Helper function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Helper function to create JWT tokens
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# User Registration Endpoint
@router.post("/register", response_model=User)
async def register(user: User):
    """
    Register a new user.
    """
    # Validate input
    if not user.email or not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required",
        )
    if not user.fullName:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Full name is required",
        )
    if not user.age:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Age is required",
        )
    if not user.gender:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Gender is required",
        )

    # Check if the email is already registered
    existing_user = await User.find_one(User.email == user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Hash the password before saving
    user.password = hash_password(user.password)

    # Save the user to the database
    try:
        await user.insert()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return user


@router.post("/login")
async def login(form_data: LoginRequest):
    """
    Log in a user and return a JWT token.
    """
    # Treat the `username` field as the email
    print(form_data.username)
    print(form_data.password)
    user = await User.find_one(User.email == form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    # Generate a JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "fullName": user.fullName,
            "gender":user.gender,
            'age':user.age
        },
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