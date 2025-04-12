import requests
import pandas as pd
from datetime import datetime
from config import WEATHER_API_URL, WEATHER_API_KEY, LOCATIONS

def fetch_weather_data():
    """Fetch current weather data from API for all configured locations"""
    all_data = []
    
    for location in LOCATIONS:
        params = {
            'lat': location['lat'],
            'lon': location['lon'],
            'appid': WEATHER_API_KEY,
            'units': 'metric'  
        }
        
        response = requests.get(WEATHER_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            for entry in data['list']:
                record = {
                    'date_time': datetime.fromtimestamp(entry['dt']),
                    'location': location['name'],
                    'temperature': entry['main']['temp'],
                    'humidity': entry['main']['humidity'],
                    'wind_speed': entry['wind']['speed'],
                    'wind_direction': entry['wind']['deg'],
                    'pressure': entry['main']['pressure'],
                    'precipitation': entry.get('rain', {}).get('3h', 0),
                    'cloud_coverage': entry['clouds']['all'],
                    'weather_condition': entry['weather'][0]['main']
                }
                all_data.append(record)
    
    return pd.DataFrame(all_data)

def save_raw_data(df, filename=None):
    """Save raw data to disk with timestamp"""
    if filename is None:
        filename = f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    df.to_csv(f"data/raw/{filename}", index=False)