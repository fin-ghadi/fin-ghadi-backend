import httpx
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

async def get_weather_data(lat: float, lon: float) -> Optional[dict]:
    """
    Fetch weather data based on latitude and longitude.
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.

    Returns:
        dict: Parsed weather data or None if the API call fails.
    """
  
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    # Access the variables
    OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
    
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "metric"  # Metric for Celsius; change to "imperial" for Fahrenheit.
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            # Extract relevant weather details
            weather_data = {
                "city": data["name"],  # City name
                "country": data["sys"]["country"],  # Country code (e.g., "US" for United States)
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "main": data["weather"][0]["main"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
            }
            return weather_data
    except httpx.RequestError as e:
        print(f"An error occurred while requesting weather data: {e}")
        return None
