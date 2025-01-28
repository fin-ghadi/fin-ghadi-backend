from fastapi import APIRouter, HTTPException, status
from beanie import PydanticObjectId
from app.models.models import Weather, User, Location
from typing import Optional
from dotenv import load_dotenv
import os
from app.utils.get_weather_data import get_weather_data  # Import the function from utils

# Load environment variables from .env file
load_dotenv()

router = APIRouter()

@router.post("/get_weather", response_model=Weather)
async def get_weather(location: Location):
    """
    Get the weather based on the provided latitude and longitude.
    """
    # Fetch weather data using the provided latitude and longitude
    lat = location.latitude
    lon = location.longitude
    weather_data = await get_weather_data(lat,lon)
    if not weather_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weather data not found",
        )
 
    # interface WeatherResponse {
    #   city: string;
    #   country: string;
    #   temperature: number;
    #   description: string;
    #   main: string;
    #   humidity: number;
    #   wind_speed: number;
    # }

    # Create a Weather document and save it to the database
    weather = Weather(
        city=weather_data["city"],
        country=weather_data["country"],
        temperature=weather_data["temperature"],
        description=weather_data["description"],
        main=weather_data["main"],
        humidity=weather_data["humidity"],
        wind_speed=weather_data["wind_speed"],
    )
    await weather.insert()

    return weather

@router.get("/test_weather")
async def test_weather(location: Location):
    """
    Test the weather endpoint with custom latitude and longitude.
    """
    lat = location.latitude
    lon = location.longitude
    print(lat, lon)
    weather_data = await get_weather_data(lat, lon)
    if not weather_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weather data not found",
        )

    return weather_data


# to test this endpoint, you can use the following curl command:
# curl -X 'GET' \
#   'http://localhost:8000/weather/test_weather?lat=37.7749&lon=-122.4194' \
