import os
from beanie import Document, Link
import jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
# User Model
class User(Document):
    name: str
    email: str
    password: str

    class Settings:
        name = "users"

    def generate_jwt(self) -> str:
        payload = {
            "sub": str(self.id),
            "exp": datetime.utcnow() + timedelta(hours=1),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @classmethod
    def verify_jwt(cls, token: str) -> Optional["User"]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("sub")
            if user_id:
                return cls.get(user_id)
        except jwt.ExpiredSignatureError:
            print("Token has expired")
        except jwt.InvalidTokenError:
            print("Invalid token")
        return None

# Activity Model
class Activity(Document):
    name: str
    description: Optional[str] = None
    category: str
    location: Optional[str] = None
    opening_hours: Optional[str] = None
    creator: Link[User]

    class Settings:
        name = "activities"

# UserActivity Model
class UserActivity(Document):
    user: Link[User]
    activity: Link[Activity]
    timestamp: datetime = datetime.utcnow()

    class Settings:
        name = "user_activities"

# Weather Model
class Weather(Document):
    location_name: str
    latitude: float
    longitude: float
    temperature: float
    description: str
    humidity: Optional[int] = None
    wind_speed: Optional[float] = None
    timestamp: datetime = datetime.utcnow()

    class Settings:
        name = "weather"
        
        
# location Model

class Location(BaseModel):
    latitude: float
    longitude: float
    
    
    