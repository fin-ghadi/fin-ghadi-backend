from datetime import datetime
from typing import Dict
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

class UserInter(BaseModel):
    gender: str  # Gender of the user
    age: int  # Age of the user

class FetchSuggestedActivities(BaseModel):
    user: UserInter  # The user data (gender, age) as a dictionaryweather: Weather
    timestamp: datetime  # Fixed to use datetime type for timestamp
    location: Location
    weather : Weather
    radius: int


from typing import List
import copy  # Import the copy module

@router.post("/get_suggested_activities")
async def get_suggested_activities(request: FetchSuggestedActivities):
    # Step 1: Fetch activities based on location and radius
    activities = await fetch_all_activities(request.location.latitude, request.location.longitude, request.radius)
    
    # Create a deep copy of the activities to preserve the original list
    copy_activities = copy.deepcopy(activities)
    
    # Step 2: Preprocess activities (remove duplicates, null, low rating activities)
    activities_preprocessed = await activities_preprocessing(copy_activities)
    
    # Step 3: Fetch the recommended activities using the AI model
    most_suggested_activities_v = await most_suggested_activities(activities_preprocessed, request.weather, request.user, request.timestamp)
    
    # Step 4: Map MostSuggestedActivities with OriginalActivities using the ID
    suggested_activities = []
    for suggested_activity in most_suggested_activities_v:
        activity_id = suggested_activity["id"]
        
        # Find the corresponding activity in the original list (using the deep copy to avoid changing the original)
        original_activity = next((act for act in activities if act['id'] == activity_id), None)
        
        if original_activity:
            # Convert the original activity to a dictionary (if it's not already)
            activity = original_activity.dict() if hasattr(original_activity, 'dict') else original_activity
            
            # Merge the original activity with the AI-suggested properties
            merged_activity = {**activity, **{
                'description': suggested_activity.get("description", ""),
                'constructions': suggested_activity.get("constructions", ""),
                'rating_ai': suggested_activity.get("rating_ai", "")
            }}
            
            # Append the merged activity to the suggested activities list
            suggested_activities.append(merged_activity)
            
    # Step 5: Return the enriched activities as the response
    return suggested_activities
