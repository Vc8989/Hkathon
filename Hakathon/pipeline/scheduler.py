import time
import schedule
from datetime import datetime
from pipeline.data_ingestion import fetch_weather_data, save_raw_data
from pipeline.data_processing import clean_weather_data
from models.model_training import train_weather_model, make_predictions
import pandas as pd
import joblib

def update_weather_data():
    """Scheduled task to fetch and process new weather data"""
    print(f"{datetime.now()}: Fetching new weather data...")
    
    new_data = fetch_weather_data()
    save_raw_data(new_data)
    
    cleaned_data = clean_weather_data(new_data)
    
    try:
        historical_data = pd.read_csv('data/processed/historical_weather.csv')
        updated_data = pd.concat([historical_data, cleaned_data]).drop_duplicates()
    except FileNotFoundError:
        updated_data = cleaned_data
    
    updated_data.to_csv('data/processed/historical_weather.csv', index=False)
    
    print(f"{datetime.now()}: Weather data updated successfully")

def update_model():
    """Scheduled task to retrain the model"""
    print(f"{datetime.now()}: Retraining weather model...")
    
    historical_data = pd.read_csv('data/processed/historical_weather.csv')
    
    # Train model
    model, scaler, mae = train_weather_model(historical_data)
    
    print(f"{datetime.now()}: Model retrained with MAE: {mae:.2f}")

def generate_predictions():
    """Scheduled task to generate new predictions"""
    print(f"{datetime.now()}: Generating new predictions...")
    
    # Load latest data
    latest_data = pd.read_csv('data/processed/historical_weather.csv')
    latest_data['date_time'] = pd.to_datetime(latest_data['date_time'])
    
    model = joblib.load('models/trained_models/weather_model.pkl')
    scaler = joblib.load('models/trained_models/scaler.pkl')
    
    # Generate predictions
    predictions = []
    for location in latest_data['location'].unique():
        loc_data = latest_data[latest_data['location'] == location]
        prediction = make_predictions(model, scaler, loc_data)
        predictions.append({
            'location': location,
            'prediction_date': datetime.now(),
            'forecast_value': prediction,
            'forecast_metric': 'temperature' 
        })
    
    # Save predictions 
    predictions_df = pd.DataFrame(predictions)
    predictions_df.to_csv('data/processed/latest_predictions.csv', index=False)
    
    print(f"{datetime.now()}: Predictions generated and saved")

def run_scheduler():
    """Run the scheduled tasks"""
    # Schedule tasks
    schedule.every().hour.do(update_weather_data)
    schedule.every().sunday.at("02:00").do(update_model)
    schedule.every().day.at("06:00").do(generate_predictions)
    
    print("Weather forecasting scheduler started...")
    while True:
        schedule.run_pending()
        time.sleep(60)