import json
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
import json
import re

def extract_json(text):
    """
    Extracts JSON data from a given string using regex and parses it into a Python dictionary.
    Args:
        text (str): The input string containing JSON data.
    Returns:
        list: A list of dictionaries representing the JSON data, or None if parsing fails.
    """
    try:
        # Use regex to extract the JSON array
        json_match = re.search(r'\[\s*{.*}\s*]', text, re.DOTALL)
        if json_match:
            json_string = json_match.group(0)
            # Parse the extracted JSON string
            return json.loads(json_string)
        else:
            print("No JSON array found in the text.")
            return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

     
# Configure the API key for Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")
 
# Ensure this function is async if you're handling async operations
async def most_suggested_activities(activities,weather, user,  timestamp):
    print('recomendation sys started ....')
    # Prepare your dynamic prompt
    prompt = f"""
    ### ROLE:
    You are an AI assistant tasked with recommending high-quality entertainment and leisure activities tailored to a user based on the following input criteria and preferences.

    ### INPUT:
    1- Activities: A list of objects, each containing:
    id: Unique identifier for the activity
    name (str): Name of the activity
    type (str): Type of activity (e.g., "entertainment," "tourist attraction," "restaurant," "café," "museum," "library")
    rating (Optional[float]): Rating of the activity (if available)
    distance (Optional[float]): Distance from the user (if available)
    opening_hours (Optional[str]): Opening hours of the activity

    {activities}

    2- User Profile:
    gender: {user.gender} (Gender of the user)
    age: {user.age} (Age of the user)

    3- Weather Conditions:
    main: {weather.main} (General weather type)
    description: {weather.description} (Specific weather description)
    temperature: {weather.temperature} (Temperature in Celsius)
    wind_speed: {weather.wind_speed} (Wind speed in km/h)
    humidity: {weather.humidity} (Humidity percentage)

    4- Timestamp: {timestamp} (Current time and date)

    ### TASK:
    1- Filter Activities:
        - Focus on high-quality entertainment, leisure, and fun activities only. Exclude low-rated activities (e.g., ratings below 2.0).
        - Avoid suggesting fast food restaurants or an overwhelming number of regular dining options. Prioritize unique or enjoyable experiences.
        - Exclude activities that are not related to fun, leisure, or entertainment, such as "office" or "work-related" activities.
        - Filter out activities that are closed during the provided timestamp (based on opening_hours).
        - Ensure the activity is within a reasonable proximity (distance) from the user.

    2- Recommend the Top 13 Activities:
        - Select the 13 best and most suitable activities based on the user’s age, gender, weather conditions, and activity ratings.
        - The activities should be **diverse** and **well-mixed**. Do not recommend too many activities of the same type (e.g., no more than 3 restaurants, 3 cinemas, etc.). Try to ensure that there are a variety of activity types (e.g., no more than 3 activities of any single type like "restaurant," "cinema," etc.).
        - Recommend activities based on the weather:
            + Avoid outdoor activities in extreme conditions like heavy rain, strong wind, or excessive heat.
            + Suggest indoor activities such as museums, libraries, or cafés during unfavorable weather conditions.
            + If the weather is favorable (mild, sunny), outdoor activities like parks or tourist attractions can be recommended.
        - Focus on logical, engaging activities that align with the current weather conditions and user demographics.

    3- Generate Detailed Suggestions for Each Activity:
    For each recommended activity, provide:
        - Construction Tips (and Advice):
            + Practical advice and tips for the user based on weather conditions and the activity type (e.g., bring an umbrella for rain, sunscreen for sunny weather, comfortable shoes for walking, etc.).
            + Additional advice that could enhance the experience (e.g., best times to visit, necessary items to bring, or how to dress based on weather conditions).
        - Personalized Description:
            + A detailed, engaging, and specific description of the activity tailored to the user's age, gender, and current weather. Highlight why the activity is enjoyable and suitable for the user in these particular weather conditions.
            + Include reasons why the activity aligns with the user’s interests and provide a vision of what they can expect to experience. Focus on how this experience will be enjoyable for them specifically.
        - AI-generated Rating (rating_ai):
            + Provide a new rating between 0 and 5 based on how well the activity aligns with the user's profile, weather conditions, and suitability.
            + Justify the rating based on the user's demographics and the context of the weather and activity. Explain why this activity was rated highly or not.

    ### OUTPUT:
    Return a list of objects representing the 13 recommended activities. Each object should have the following structure:
    [
      {{
        "id": <activity_id>,
        "constructions": "<Practical advice for the user, including recommendations, tips, and weather-specific advice>",
        "description": "<Detailed and personalized description of the activity tailored to the user’s profile and current weather conditions>",
        "rating_ai": <AI-generated rating for the activity>
      }}
    ]
    """



    # Call the Gemini API asynchronously
    response = model.generate_content(prompt)

    # Return the AI-generated suggestion
    
    final_result = extract_json(response.text)
    return final_result
