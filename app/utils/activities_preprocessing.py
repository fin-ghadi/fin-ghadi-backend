

 
from typing import List, Dict, Any
import asyncio

async def activities_preprocessing(activities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
   The activities_preprocessing function processes a list of activities by:
        -Removing duplicates (based on id).
        -Filtering out activities with:
            Null values in required fields (name, type).
            Low ratings (rating < 3.0).
        -Limiting activities per type to a maximum of 20, prioritizing higher ratings and shorter distances.
        -Removing unwanted fields:
            address
            location
            website
            phone
            description
            constructions
        -The final activity structure includes:
            id
            name
            type
            rating
            distance
            opening_hours
    """
    if not activities:
        return []

    print('preprocessing started ....')
    
    # Step 1: Remove duplicates based on activity ID
    unique_activities = {activity['id']: activity for activity in activities}.values()

    # Step 2: Filter out activities with null values or low ratings (assuming low rating is < 3.0)
    filtered_activities = [
        activity for activity in unique_activities
        if activity.get('rating', 0) >= 3.0 and all(activity.get(field) is not None for field in ['name', 'type'])
    ]

    # Step 3: Group activities by type
    activities_by_type: Dict[str, List[Dict[str, Any]]] = {}
    for activity in filtered_activities:
        activity_type = activity['type']
        if activity_type not in activities_by_type:
            activities_by_type[activity_type] = []
        activities_by_type[activity_type].append(activity)

    # Step 4: Sort activities within each type by rating (descending) and distance (ascending)
    for activity_type in activities_by_type:
        activities_by_type[activity_type].sort(
            key=lambda x: (-x.get('rating', 0), x.get('distance', float('inf')))
        )

    # Step 5: Limit the number of activities per type to 20
    final_activities = []
    for activity_type in activities_by_type:
        final_activities.extend(activities_by_type[activity_type][:10])

    # Step 6: Remove unwanted fields
    for activity in final_activities:
        for field in ['address', 'location', 'website', 'phone', 'constructions', 'description']:
            activity.pop(field, None)

    return final_activities