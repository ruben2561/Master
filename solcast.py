import requests
import csv

# Set your Solcast API key
api_key = "w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"

# Specify the location (latitude and longitude)
latitude = 50.9254992
longitude = 5.3932811

def get_sample_data():
    try:
        with open("pv_data.csv", "r") as file:
            sample_data = file.read()
            return sample_data
    except Exception as e:
        print(f"Error reading sample data: {e}")
        return None

def get_solar_radiation_forecast(type, time):
    try:
        # Solcast API endpoint for Global Horizontal Irradiance (GHI) forecast
        #if(type == "radiation"):
        #    endpoint = "https://api.solcast.com.au/weather_sites/f0c1-3849-a865-4bca/estimated_actuals?format=csvapi_key=w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"
        #    print("trying to retrieve radiation")
        #elif(type == "pv"):
        #    endpoint = "https://api.solcast.com.au/rooftop_sites/2232-a658-4143-f02f/estimated_actuals?format=csv&api_key=w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"
        #    print("trying to retrieve rooftop pv")

        endpoint = "https://api.solcast.com.au/rooftop_sites/2232-a658-4143-f02f/estimated_actuals?format=csv&api_key=w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"

        payload={}
        headers = {}

        response = requests.request("GET", endpoint, headers=headers, data=payload)
        print(response.text)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}, {response.text}")
            # Load sample data from file pv_data.css
            return get_sample_data()

    except Exception as e:
        print(f"Error: {e}")
        return get_sample_data()


# Example usage
#forecast_data = get_solar_radiation_forecast(time)
#if forecast_data:
#    print("Solar Radiation Data:")
#    print(forecast_data)
#else:
#    print("Failed to retrieve solar radiation forecast.")
    




# Specify the time for the forecast (in UTC)
# forecast_time = "2023-11-13T12:00:00Z"  # Replace with your desired time

# # Solcast API endpoint for Global Horizontal Irradiance (GHI) forecast
# endpoint = f"https://api.solcast.com.au/data/forecast/radiation_and_weather?latitude=-33.856784&longitude=151.215297&api_key=w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"
# endpoint2 = f"https://api.solcast.com.au/data/forecast/radiation_and_weather?latitude={latitude}&longitude={longitude}&api_key={api_key}"
# endpoint3 = f"https://api.solcast.com.au/data/forecast/radiation_and_weather?latitude=-33.856784&longitude=151.215297&output_parameters=air_temp,dni,ghi&format=json&api_key={api_key}"
# endpoint4 = f"https://api.solcast.com.au/data/historic/radiation_and_weather?latitude=-33.856784&longitude=151.215297&azimuth=44&tilt=90&start=2023-10-25T14:45:00.000Z&duration=P31D&format=csv&time_zone=utc&api_key={api_key}"
# endpoint5 = "https://api.solcast.com.au/data/historic_forecast/radiation_and_weather?latitude=48.30783&longitude=-105.1017&azimuth=44&tilt=90&start=2022-10-25T14:45:00.000Z&duration=P31D&format=csv&time_zone=utc&lead_time=PT1H"
# endpoint6 = "https://api.solcast.com.au/rooftop_sites/2232-a658-4143-f02f/estimated_actuals?format=csv&api_key=w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"
# endpoint7 = "https://api.solcast.com.au/weather_sites/f0c1-3849-a865-4bca/estimated_actuals?format=json&api_key=w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"

# url = endpoint6

# print(url + "\r\r")
# try:

#     payload={}
#     headers = {}

#     response = requests.request("GET", url, headers=headers, data=payload)

#     # Check if the request was successful (status code 200)
#     print(response.text)
#     if response.status_code == 200:
#         data = response.json()
#         print("Solar Radiation Data:")
#         print(data)
#     else:
#         print(f"Error: {response.status_code}, {response.text}")

# except Exception as e:
#     print(f"Error: {e}")