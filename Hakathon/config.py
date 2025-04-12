import os
from datetime import timedelta

# API Configuration
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/forecast"
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  

# Database Configuration
SUPABASE_URL = os.getenv("")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Model Configuration
MODEL_UPDATE_FREQUENCY = timedelta(days=7)  
FORECAST_HORIZON = 24  

# Data Collection Locations (latitude, longitude)
LOCATIONS = [
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "London", "lat": 51.5074, "lon": -0.1278},
]

# Feature columns used in model
FEATURE_COLUMNS = [
    'temperature', 'humidity', 'wind_speed', 
    'wind_direction', 'pressure', 'precipitation', 
    'cloud_coverage'
]

TARGET_COLUMN = 'temperature' 