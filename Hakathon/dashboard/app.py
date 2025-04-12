import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import supabase
import os




# Initialize Supabase client
client = supabase.create_client(
    weather_url = st.secrets["url"],
    api_key = st.secrets["key"]
)

def get_weather_data(location, days=7):
    """Fetch weather data from Supabase"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    response = client.table('weather_data').select("*").eq('location', location).gte('date_time', start_date.isoformat()).lte('date_time', end_date.isoformat()).execute()
    
    return pd.DataFrame(response.data)

def get_predictions(location):
    """Fetch predictions from Supabase"""
    response = client.table('weather_predictions').select("*").eq('location', location).order('prediction_date', desc=True).limit(24).execute()
    
    return pd.DataFrame(response.data)

def create_dashboard():
    st.title("Weather Forecasting Dashboard")
    
    # Location selector
    locations = ["New York", "London", "Tokyo"]  
    selected_location = st.selectbox("Select Location", locations)
    
    # Date range selector
    days_to_show = st.slider("Days to show", 1, 30, 7)
    
    weather_data = get_weather_data(selected_location, days_to_show)
    predictions = get_predictions(selected_location)
    
    # Convert date columns
    weather_data['date_time'] = pd.to_datetime(weather_data['date_time'])
    predictions['prediction_date'] = pd.to_datetime(predictions['prediction_date'])
    
    # Temperature plot
    st.subheader("Temperature Forecast")
    fig = px.line(weather_data, x='date_time', y='temperature', title='Historical Temperature')
    fig.add_scatter(x=predictions['prediction_date'], y=predictions['forecast_value'], mode='lines', name='Forecast')
    st.plotly_chart(fig)
    
    # Metrics display
    col1, col2, col3 = st.columns(3)
    latest_temp = weather_data['temperature'].iloc[-1]
    forecast_temp = predictions['forecast_value'].iloc[0]
    
    col1.metric("Current Temperature", f"{latest_temp:.1f}°C")
    col2.metric("Forecast Temperature", f"{forecast_temp:.1f}°C")
    col3.metric("Difference", f"{(forecast_temp - latest_temp):.1f}°C", delta_color="inverse")
    
    # Additional weather metrics
    st.subheader("Weather Conditions")
    tab1, tab2, tab3 = st.tabs(["Humidity", "Wind", "Precipitation"])
    
    with tab1:
        fig = px.line(weather_data, x='date_time', y='humidity', title='Humidity (%)')
        st.plotly_chart(fig)
    
    with tab2:
        fig = px.scatter(weather_data, x='date_time', y='wind_speed', color='wind_direction',
                         title='Wind Speed and Direction', 
                         hover_data=['wind_direction'])
        st.plotly_chart(fig)
    
    with tab3:
        fig = px.bar(weather_data, x='date_time', y='precipitation', title='Precipitation (mm)')
        st.plotly_chart(fig)

if __name__ == "__main__":
    create_dashboard()