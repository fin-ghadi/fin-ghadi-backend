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
 
    fullName: str
    email: str
    password: str
    gender: str
    age: int

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
# location Model

class Location(BaseModel):
    latitude: float
    longitude: float
    
    
class Quote(Document):
    quote: str
    author: str
    
    class Settings:
        name = "quotes"
    
    
    
# Activity Model
class Activity(Document):
    name: str
    address: str
    location: Location  # Update to dictionary to match the sample
    type: str
    rating: Optional[float] = None  # Rating field added
    distance: Optional[float] = None  # Distance field added
    website: Optional[str] = None  # Website field added
    phone: Optional[str] = None  # Phone field added
    opening_hours: Optional[str] = None  # Opening hours field added
    description: Optional[str] = None  # Description field added
    constructions: Optional[str] = None 
    class Settings:
        name = "activities"

# UserActivity Model
class UserActivity(Document):
    user: Link[User]
    activity: Link[Activity]
    timestamp: datetime = datetime.utcnow()
    user_rating: Optional[float] = None 
    class Settings:
        name = "user_activities"

# Weather Model
class Weather(Document):
    city: str
    country: str
    temperature: float
    description: str
    main: str
    humidity: int
    wind_speed: float
    

    class Settings:
        name = "weather"    
        
        
