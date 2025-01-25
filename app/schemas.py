from pydantic import BaseModel

class WeatherRequest(BaseModel):
    location: str

class ActivityResponse(BaseModel):
    name: str
    description: str
