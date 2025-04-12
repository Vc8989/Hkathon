import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from config import FEATURE_COLUMNS, TARGET_COLUMN

def clean_weather_data(df):
    """Clean and preprocess weather data"""
    # Handle missing values
    df = df.dropna(subset=FEATURE_COLUMNS + [TARGET_COLUMN])
    
    # Convert weather condition to categorical
    df['weather_condition'] = df['weather_condition'].astype('category')
    
    # Feature engineering
    df['hour_of_day'] = df['date_time'].dt.hour
    df['day_of_year'] = df['date_time'].dt.dayofyear
    
    return df

def prepare_training_data(df):
    """Prepare features and target for model training"""
    df = df.sort_values('date_time')
    
    for lag in [1, 2, 3, 24]:
        for feature in FEATURE_COLUMNS:
            df[f'{feature}_lag_{lag}'] = df[feature].shift(lag)
    
    df = df.dropna()
    
    X = df.drop(columns=[TARGET_COLUMN, 'date_time', 'weather_condition', 'location'])
    y = df[TARGET_COLUMN]
    
    # Train-test split with time-based validation
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False)
    
    # Scale numerical features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler