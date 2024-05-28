import csv
import datetime
import openmeteo_requests
import pandas as pd
import requests
import requests_cache
from datetime import datetime, timedelta
from retry_requests import retry


def get_sample_data_pv():
    try:
        with open("sampleData/solar_data_year.csv", "r") as file:
            sample_data = file.read()
            print("sample weather data used")
            return sample_data
    except Exception as e:
        print(f"Error reading sample data: {e}")
        return None


def fetch_weather_data(latitude, longitude, start_date, end_date):
    base_url = "https://archive-api.open-meteo.com/v1/archive"
    params = {'latitude': latitude, 'longitude': longitude, 'start_date': start_date, 'end_date': end_date,
        'hourly': 'temperature_2m,shortwave_radiation,diffuse_radiation,direct_normal_irradiance'}

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def format_weather_data(data):
    hourly_data = data.get('hourly', {})
    periods = hourly_data.get('time', [])
    temperatures = hourly_data.get('temperature_2m', [])
    GHIs = hourly_data.get('shortwave_radiation', [])
    DHIs = hourly_data.get('diffuse_radiation', [])
    DNIs = hourly_data.get('direct_normal_irradiance', [])

    formatted_data = "period_end,temp,GHI,DHI,DNI\n"
    for period, temp, ghi, dhi, dni in zip(periods, temperatures, GHIs, DHIs, DNIs):
        formatted_data += f"{period},{temp},{ghi},{dhi},{dni}\n"

    return formatted_data.strip()  # Remove the last newline character


def get_solar_data_openmeteo(latitude, longitude, start_date):
    try:

        date_obj = datetime.strptime(start_date, "%Y-%m-%d")

        # Add the specified number of days
        new_date_obj = date_obj + timedelta(days=364)

        # Convert the datetime object back to a string
        end_date = new_date_obj.strftime("%Y-%m-%d")

        # Fetch weather data
        weather_data = fetch_weather_data(latitude, longitude, start_date, end_date)

        # Format the data
        formatted_weather_data = format_weather_data(weather_data)

        print("openmeteo weather data used")

        return formatted_weather_data

    except Exception as e:
        print(f"Error: {e}")
        return get_sample_data_pv()
