import datetime
import requests
from datetime import datetime, timedelta
from retry_requests import retry

# Function to get sample PV data from a CSV file
def get_sample_data_pv():
    try:
        # Open the sample data file
        with open("sampleData/solar_data_year.csv", "r") as file:
            sample_data = file.read()
            print("Sample weather data used")
            return sample_data
    except Exception as e:
        # Print an error message if reading fails
        print(f"Error reading sample data: {e}")
        return None

# Function to fetch weather data from the Open-Meteo API
def fetch_weather_data(latitude, longitude, start_date, end_date):
    base_url = "https://archive-api.open-meteo.com/v1/archive"
    # Set the parameters for the API request
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'start_date': start_date,
        'end_date': end_date,
        'hourly': 'temperature_2m,shortwave_radiation,diffuse_radiation,direct_normal_irradiance'
    }
    # Make the API request
    response = requests.get(base_url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        # Raise an exception if the request failed
        response.raise_for_status()

# Function to format the fetched weather data
def format_weather_data(data):
    hourly_data = data.get('hourly', {})
    periods = hourly_data.get('time', [])
    temperatures = hourly_data.get('temperature_2m', [])
    GHIs = hourly_data.get('shortwave_radiation', [])
    DHIs = hourly_data.get('diffuse_radiation', [])
    DNIs = hourly_data.get('direct_normal_irradiance', [])

    # Create a CSV formatted string from the weather data
    formatted_data = "period_end,temp,GHI,DHI,DNI\n"
    for period, temp, ghi, dhi, dni in zip(periods, temperatures, GHIs, DHIs, DNIs):
        formatted_data += f"{period},{temp},{ghi},{dhi},{dni}\n"

    return formatted_data.strip()  # Remove the last newline character

# Function to get solar data from Open-Meteo
def get_solar_data_openmeteo(latitude, longitude, start_date):
    try:
        # Parse the start date
        date_obj = datetime.strptime(start_date, "%Y-%m-%d")

        # Add 364 days to the start date to get the end date
        new_date_obj = date_obj + timedelta(days=364)

        # Convert the datetime object back to a string
        end_date = new_date_obj.strftime("%Y-%m-%d")

        # Fetch weather data using the fetch_weather_data function
        weather_data = fetch_weather_data(latitude, longitude, start_date, end_date)

        # Format the fetched weather data
        formatted_weather_data = format_weather_data(weather_data)

        print("Open-Meteo weather data used")

        return formatted_weather_data

    except Exception as e:
        # Print an error message if any exception occurs
        print(f"Error: {e}")
        return get_sample_data_pv()
