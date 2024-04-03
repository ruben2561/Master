import requests
import csv
import datetime

# Set your Solcast API key
api_key = "w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"

# Specify the location (latitude and longitude)
latitude = 50.9254992
longitude = 5.3932811




def get_sample_data_pv():
    try:
        with open("sampleData/pv_data_year.csv", "r") as file:
            sample_data = file.read()
            return sample_data
    except Exception as e:
        print(f"Error reading sample data: {e}")
        return None

def get_solar_data(latitude, longitude, start_date, end_date):
    try:

        # Solcast API endpoint for Global Horizontal Irradiance (GHI) forecast
        #if(type == "radiation"):
        #    endpoint = "https://api.solcast.com.au/weather_sites/f0c1-3849-a865-4bca/estimated_actuals?format=csvapi_key=w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"
        #    print("trying to retrieve radiation")
        #elif(type == "pv"):
        #    endpoint = "https://api.solcast.com.au/rooftop_sites/2232-a658-4143-f02f/estimated_actuals?format=csv&api_key=w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"
        #    print("trying to retrieve rooftop pv")
        
        # Convert to datetime object
        start_date_object = datetime.strptime(start_date, "%d/%m/%Y")

        # Convert to desired format
        formatted_start_date = start_date_object.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        endpoint2 = "https://api.solcast.com.au/rooftop_sites/2232-a658-4143-f02f/estimated_actuals?format=csv&api_key=w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"
        endpoint = f"https://api.solcast.com.au/data/historic/rooftop_pv_power?latitude={latitude}&longitude={longitude}&period=PT30M&output_parameters=pv_power_rooftop&capacity=1&install_date=2020-12-30&format=json&start={start_date}&end={end_date}&api_key=w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"

        payload={}
        headers = {}

        response = requests.request("GET", endpoint, headers=headers, data=payload)
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


# Example usage
#forecast_data = get_solar_radiation_forecast(time)
#if forecast_data:
#    print("Solar Radiation Data:")
#    print(forecast_data)
#else:
#    print("Failed to retrieve solar radiation forecast.")