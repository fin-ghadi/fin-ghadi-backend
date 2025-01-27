from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.models import User, Activity, UserActivity, Weather  # Import all models
from app.endpoints.activity import router as activity_router
from app.endpoints.user import router as user_router
from app.endpoints.weather import router as weather_router
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Access the secret key
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set in environment variables")
# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await init_db()
    yield
    # Shutdown logic (optional)

app = FastAPI(
    title="FinGhadi API",
    description="API for personalized activity suggestions based on weather and location.",
    version="1.0.0",
    lifespan=lifespan,
)

# MongoDB connection setup
async def init_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(
        database=client["fin-ghadi"],
        document_models=[User, Activity, UserActivity, Weather],
    )

# Include routers
app.include_router(activity_router, prefix="/   ", tags=["activities"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(weather_router, prefix="/weather", tags=["weather"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FinGhadi API"}