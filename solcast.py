import requests
from datetime import datetime

# Set your Solcast API key
api_key = "w58k5_UUO4JxNP3ykI-gsRn8w65hJQQQ"

# Specify the location (latitude and longitude)
latitude = 50.9254992
longitude = 5.3932811

# Specify the time for the forecast (in UTC)
forecast_time = "2023-11-13T12:00:00Z"  # Replace with your desired time

# Solcast API endpoint for Global Horizontal Irradiance (GHI) forecast
#endpoint = f"https://api.solcast.com.au/data/forecast/radiation_and_weather?latitude={latitude}&longitude={longitude}&api_key={api_key}"
url = f"https://api.solcast.com.au/data/forecast/radiation_and_weather?latitude=-33.856784&longitude=151.215297&output_parameters=air_temp,dni,ghi&format=json&api_key={api_key}"

try:
    
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    # Check if the request was successful (status code 200)
    print(response)
    if response.status_code == 200:
        data = response.json()
        print("Solar Radiation Data:")
        print(data)
    else:
        print(f"Error: {response.status_code}, {response.text}")

except Exception as e:
    print(f"Error: {e}")
