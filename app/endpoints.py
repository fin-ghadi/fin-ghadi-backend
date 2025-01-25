from fastapi import APIRouter

router = APIRouter()

@router.get("/weather")
def get_weather():
    return {"message": "Fetch weather data here."}

@router.get("/activities")
def get_activities():
    return {"message": "Suggest activities here based on weather and location."}
