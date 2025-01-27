from fastapi import APIRouter, HTTPException, Depends, status
from beanie import PydanticObjectId
from app.models.models import Activity
from app.models.models import User
# from app.utils import get_current_user

router = APIRouter(prefix="/activities", tags=["activities"])

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

