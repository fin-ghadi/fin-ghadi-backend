from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from beanie import PydanticObjectId
from pydantic import BaseModel
from app.models.models import Activity, Location, Weather
from app.models.models import User
# from app.utils import get_current_user
from app.utils.fetch_all_activities import fetch_all_activities
from app.utils.activities_preprocessing import activities_preprocessing
from app.utils.most_suggested_activities import most_suggested_activities


router = APIRouter()

# Create Activity Endpoint
@router.post("/", response_model=Activity)
async def create_activity(activity: Activity):
    """
    Create a new activity.
    """
    # Insert the activity into the database
    await activity.insert()
    return activity

# Get All Activities Endpoint
@router.get("/", response_model=list[Activity])
async def get_activities():
    """
    Get a list of all activities.
    """
    activities = await Activity.find_all().to_list()
    return activities

# Get Activity by ID Endpoint
@router.get("/{activity_id}", response_model=Activity)
async def get_activity_by_id(activity_id: PydanticObjectId):
    """
    Get an activity by its ID.
    """
    activity = await Activity.get(activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )
    return activity


class FetchActivitiesRequest(BaseModel):
    location: Location
    radius: int

# endpoint to test the app.utls.fetch_all_activities that fetches activities from the 
# Overpass API taking latitude and longitude and radius as arguments 
@router.post("/fetch_all_activities_location")
async def fetch_all_activities2(request: FetchActivitiesRequest):
    lat = request.location.latitude
    lon = request.location.longitude
    radius = request.radius
    print(lat, lon, radius)
    activities = await fetch_all_activities(lat, lon, radius)
    activities_Preprocessed = await activities_preprocessing(activities)

    return activities_Preprocessed
# to test this endpoint, you can use the following curl command:
# curl -X 'GET' \
#   'http://localhost:8000/activities/fetch_all_activities?lat=37.7749&lon=-122.4194&radius=1000' \



class FetchSuggestedActivities(BaseModel):
    user: User
    weather: Weather
    timestamp: datetime  # Fixed to use datetime type for timestamp
    location: Location
    radius: int


@router.post("/get_suggested_activities")
async def get_suggested_activities(request: FetchSuggestedActivities):
    
    activities = await fetch_all_activities(request.location.latitude,request.location.longitude, request.radius)
    
    # remove dupplicated , null , low rating activities 
    activities_Preprocessed = activities_preprocessing(activities)
    
    # fetch the recommended activities usig the AI model 
    most_suggested_activities_v = most_suggested_activities(activities_Preprocessed,request.weather ,request.user, request.timestamp)
    
    # fetch the activies from the activities array using the ids returned by most_suggested_activities
     
    
    return most_suggested_activities_v
    
    





