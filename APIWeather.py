import requests
import csv
import datetime
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Set your Solcast API key
api_key = "w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"

# Specify the location (latitude and longitude)
latitude = 50.9254992
longitude = 5.3932811




def get_sample_data_pv():
    try:
        with open("sampleData/solar_data_year.csv", "r") as file:
            sample_data = file.read()
            return sample_data
    except Exception as e:
        print(f"Error reading sample data: {e}")
        return None

# TODO change to automatic one year end date
def get_solar_data_openmeteo(latitude, longitude, start_date):
    try:
        raise Exception("openmeteo api doesnt work yet")
    
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)
        
        start_date = pd.to_datetime(start_date, "%Y-%m-%d")
        
        # Calculate end date one year further
        end_date = start_date + datetime.timedelta(days=365)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": ["temperature_2m", "shortwave_radiation", "diffuse_radiation", "direct_normal_irradiance"]
        }
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_shortwave_radiation = hourly.Variables(1).ValuesAsNumpy()
        hourly_diffuse_radiation = hourly.Variables(2).ValuesAsNumpy()
        hourly_direct_normal_irradiance = hourly.Variables(3).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["shortwave_radiation"] = hourly_shortwave_radiation
        hourly_data["diffuse_radiation"] = hourly_diffuse_radiation
        hourly_data["direct_normal_irradiance"] = hourly_direct_normal_irradiance

        hourly_dataframe = pd.DataFrame(data = hourly_data)
        print(hourly_dataframe)
    
    except Exception as e:
        print(f"Error: {e}")
        return get_sample_data_pv()
    
    
def get_solar_data_solcast(latitude, longitude, start_date):
    try:
        # Solcast API endpoint for Global Horizontal Irradiance (GHI) forecast
        #if(type == "radiation"):
        #    endpoint = "https://api.solcast.com.au/weather_sites/f0c1-3849-a865-4bca/estimated_actuals?format=csvapi_key=w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"
        #    print("trying to retrieve radiation")
        #elif(type == "pv"):
        #    endpoint = "https://api.solcast.com.au/rooftop_sites/2232-a658-4143-f02f/estimated_actuals?format=csv&api_key=w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"
        #    print("trying to retrieve rooftop pv")
        
        #end_date = start_date + datetime.timedelta(days=365)
        
        # Convert to datetime object
        start_date_object = datetime.datetime.strptime(start_date, "%Y-%m-%d")

        # Convert to desired format
        formatted_start_date = start_date_object.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        endpoint2 = "https://api.solcast.com.au/rooftop_sites/2232-a658-4143-f02f/estimated_actuals?format=csv&api_key=w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"
        #endpoint = f"https://api.solcast.com.au/data/historic/rooftop_pv_power?latitude={latitude}&longitude={longitude}&period=PT30M&output_parameters=pv_power_rooftop&capacity=1&install_date=2020-12-30&format=json&start={start_date}&end={end_date}&api_key=w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"

        payload={}
        headers = {}

        response = requests.request("GET", endpoint2, headers=headers, data=payload)
        #print(response.text)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}, {response.text}")
            # Load sample data from file pv_data.css
            return get_sample_data_pv()

    except Exception as e:
        print(f"Error: {e}")
        return get_sample_data_pv()


# #Example usage
# forecast_data = get_solar_data_openmeteo(55.1, 5.5, "2023-01-01")
# if forecast_data:
#    print("Solar Radiation Data:")
#    print(forecast_data)
# else:
#    print("Failed to retrieve solar radiation forecast.")