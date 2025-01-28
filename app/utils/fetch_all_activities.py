import random
import requests
from typing import List, Dict
from geopy.distance import geodesic

async def fetch_all_activities(lat: float, lon: float, radius: int) -> List[Dict]:
    """
    Fetches ALL activities within a given radius of a latitude and longitude using the Overpass API,
    including entertainment activities, beaches beyond the radius, and activities like bowling, gaming, and cycling.

    Args:
        lat (float): Latitude of the center point.
        lon (float): Longitude of the center point.
        radius (int): Radius in meters to search for activities.

    Returns:
        List[Dict]: A list of activity objects with details like name, address, coordinates, etc.

    Raises:
        Exception: If there is an error fetching data from the Overpass API.
    """
    
    # Overpass API query to fetch ALL activities (amenities, tourism, leisure, etc.)
    query = f"""
    [out:json];
    (
        node["amenity"](around:{radius},{lat},{lon});
        node["tourism"](around:{radius},{lat},{lon});
        node["leisure"](around:{radius},{lat},{lon});
        node["historic"](around:{radius},{lat},{lon});
        node["shop"](around:{radius},{lat},{lon});
        node["sport"](around:{radius},{lat},{lon});
        node["leisure"="bowling_alley"](around:{radius},{lat},{lon});
        node["leisure"="video_arcade"](around:{radius},{lat},{lon});
        node["amenity"="bicycle_rental"](around:{radius},{lat},{lon});
        node["amenity"="cinema"](around:{radius},{lat},{lon});
        node["amenity"="theatre"](around:{radius},{lat},{lon});
        node["amenity"="nightclub"](around:{radius},{lat},{lon});
        node["amenity"="concert_hall"](around:{radius},{lat},{lon});
        node["tourism"="theme_park"](around:{radius},{lat},{lon});
        node["amenity"="casino"](around:{radius},{lat},{lon});
    );
    out body;
    >;
    out skel qt;
    """

    # Overpass API endpoint
    url = "https://overpass-api.de/api/interpreter"
    
    try:
        # Send the query to the Overpass API
        response = requests.post(url, data=query)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        data = response.json()
        
        # Process the response and extract activity details
        activities = []
    
        for element in data.get("elements", []):
            activity = {
                "name": element.get("tags", {}).get("name", "Unknown"),
                "address": f"{element.get('tags', {}).get('addr:street', '')} {element.get('tags', {}).get('addr:housenumber', '')}".strip(),
                "location" :
                   {
                    "latitude": element.get("lat"),
                    "longitude": element.get("lon"),
                   },
                "type": element.get("tags", {}).get("amenity") or 
                        element.get("tags", {}).get("tourism") or 
                        element.get("tags", {}).get("leisure") or 
                        element.get("tags", {}).get("historic") or 
                        element.get("tags", {}).get("shop") or 
                        element.get("tags", {}).get("sport", "Unknown"),
                "rating": None,  # Overpass API does not provide ratings
                "distance": None,  # You can calculate this if needed
                "website": element.get("tags", {}).get("website"),
                "phone": element.get("tags", {}).get("phone"),
                "opening_hours": element.get("tags", {}).get("opening_hours")
            }
            
            # Skip unwanted activity types (case insensitive comparison)
            unwanted_activity_types = [
                "unknown", "toilets", "bench", "waste_basket", "recycling", "vending_machine",'post_office',"dentist" , "car_repair",
                "atm", "post_box", "telephone", "shelter", "drinking_water", "bicycle_parking", "mobile_phone",
                'bank', 'pharmacy', 'fast food', 'fuel', 'parking', 'supermarket', 'marketplace', 'taxi','police',
                'bakery', 'butcher', 'greengrocer', 'convenience store','school', 'kindergarten','supermarket','clinic', 'car_rental', 'police', 'cafe'
            ]  
            if activity["type"].lower() in unwanted_activity_types:
                continue
            
            # Calculate the distance from the center point
            origin = (lat, lon)
            destination = (activity["location"]["latitude"], activity["location"]["longitude"])
            activity["distance"] = round(geodesic(origin, destination).meters, 2)
            
            # Add a random rating for each activity
            activity["rating"] = round(random.uniform(1, 5), 1)
            
            # Append the activity if it has a valid name and type
            if activity["name"] != "Unknown" and activity["type"] != "Unknown":
                activities.append(activity)
        
        # Fetch beaches beyond the radius (use a smaller radius for beaches)
        beaches_query = f"""
        [out:json];
        node["natural"="beach"](around:50000,{lat},{lon});
        out body;
        >;
        out skel qt;
        """
        beaches_response = requests.post(url, data=beaches_query)
        beaches_response.raise_for_status()
        beaches_data = beaches_response.json()
        
        # Process beaches and add the closest 2-3
        beaches = []
        for element in beaches_data.get("elements", []):
            beach = {
                "name": element.get("tags", {}).get("name", "Unknown"),
                "address": f"{element.get('tags', {}).get('addr:street', '')} {element.get('tags', {}).get('addr:housenumber', '')}".strip(),
                "latitude": element.get("lat"),
                "longitude": element.get("lon"),
                "type": "beach",
                "rating": None,
                "distance": None,
                "website": element.get("tags", {}).get("website"),
                "phone": element.get("tags", {}).get("phone"),
                "opening_hours": element.get("tags", {}).get("opening_hours")
            }
            
            # Calculate distance to the beach
            origin = (lat, lon)
            destination = (beach["latitude"], beach["longitude"])
            beach["distance"] = round(geodesic(origin, destination).meters, 2)
            
            # Add a random rating for the beach
            beach["rating"] = round(random.uniform(1, 5), 1)
            
            if beach["name"] != "Unknown":
                beaches.append(beach)
        
        # Sort beaches by distance and take the closest 2-3
        beaches.sort(key=lambda x: x["distance"])
        activities.extend(beaches[:3])
        
        for i in range (len(activities)) :
            activities[i]['id'] = i+1
        return activities
    
    except requests.exceptions.RequestException as e:
        # Throw an error with a descriptive message
        raise Exception(f"Error fetching activities from Overpass API: {e}")
