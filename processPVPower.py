
import csv
import datetime
import json
import math
import numpy as np
import pandas as pd
import pvlib
from datetime import datetime


from APIWeather import get_solar_data_solcast

def get_sample_data_pv():
    try:
        with open("sampleData/solar_data_year_processed.csv", "r") as file:
            sample_data = file.read()
            reader = csv.DictReader(sample_data.splitlines())
            values_list = list(reader)
            pv_list = []
            for point in values_list:
                period_end = datetime.strptime(
                    point["time_value"], "%Y-%m-%dT%H:%M:%S"
                )  # Convert string to datetime
                pv_list.append({
                    "pv_power_value": float(point["pv_power_value"]),
                    "time_value": period_end,
                })
                
            return pv_list
    except Exception as e:
        print(f"Error reading sample data: {e}")
        return None

def calculate_pv_power(forecast_list, latitude, longitude, number_of_panels, area, azimuth, tilt, efficiency_panels, efficiency_invertor):
    pv_list = []

    if efficiency_panels > 1:
        efficiency_panels /= 100
    if efficiency_invertor > 1:
        efficiency_invertor /= 100

    solar_positions = pvlib.solarposition.get_solarposition(
        pd.to_datetime([data_point["period_end"] for data_point in forecast_list]),
        latitude, longitude
    )

    dnies = np.array([float(data_point["DNI"]) for data_point in forecast_list])
    ghies = np.array([float(data_point["GHI"]) for data_point in forecast_list])
    dhies = np.array([float(data_point["DHI"]) for data_point in forecast_list])
    poa_globals = pvlib.irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=azimuth,
        dni=dnies,
        ghi=ghies,
        dhi=dhies,
        solar_zenith=solar_positions['zenith'].values,
        solar_azimuth=solar_positions['azimuth'].values
    )['poa_global']

    pv_estimates = (poa_globals * area * number_of_panels * efficiency_panels * efficiency_invertor) / 1000

    for i, data_point in enumerate(forecast_list):
        pv_list.append({
            "pv_power_value": pv_estimates[i],
            "time_value": datetime.strptime(data_point["period_end"], "%Y-%m-%dT%H:%M"),
        })

    return pv_list
        
def read_pv_list_from_file(filename):
    try:
        with open(filename, 'r') as file:
            pv_list = json.load(file)
        print(f"PV list loaded from {filename}")
        return pv_list
    except Exception as e:
        print(f"Error reading PV list from file: {e}")
        return None

def process_solar_data(latitude, longitude, start_date, number_of_panels, area, azimuth, tilt, efficiency_panels, efficiency_invertor, use_api):

    # Calculate end date one year further
    #end_date = start_date + pd.DateOffset(days=365)
    #TODO fix end date
    forecast_data = get_solar_data_solcast(
        latitude, longitude, start_date
    )
    
    reader = csv.DictReader(forecast_data.splitlines())
    forecast_list = list(reader)
    
    pv_list = calculate_pv_power(forecast_list, latitude, longitude, number_of_panels, area, azimuth, tilt, efficiency_panels, efficiency_invertor)
    #pv_list = get_sample_data_pv()

    # Initialize list to store data for plotting as tuples of (pv_power_value, time_value)
    data_points = []

    # Iterate over the forecast data
    for data_point in pv_list:
        # Store data point as a dictionary
        #TODO fix /2
        data_points.append(
            {
                "pv_power_value": data_point['pv_power_value']/2,
                "time_value": data_point['time_value'],
                "soc_value": 0,
                "charge_value": 0,
                "discharge_value": 0,
                "grid_injection": 0,
                "grid_offtake": 0,
                "power_usage_value": 0,
                "price_injection": 0,
                "price_offtake": 0,
                "ev_charge_value": 0,
            }
        )

    return data_points









# # Example usage
# latitude = 50.9254992  # Example latitude (San Francisco)
# longitude = 5.3932811  # Example longitude (San Francisco)
# capacity_kw = 5  # Capacity of the PV system in kW
# number_of_panels = 24
# azimuth = 80  # Azimuth angle (orientation) of the PV panels (in degrees)
# tilt = 45  # Tilt angle of the PV panels (in degrees)
# efficiency_panels = 0.90  # Efficiency of the PV system
# efficiency_invertor = 0.96
# dni = 191  # Direct Normal Irradiance in W/m^2
# ghi = 141  # Global Horizontal Irradiance in W/m^2
# air_temperature = 17
# specific_time = "2023-01-05T20:00:00Z"
# area = 1
# forecast_list = [{'air_temp': '9', 'dni': '300', 'ghi': '190', 'period_end': '2023-01-03T13:00:00Z', 'period': 'PT60M'}, {'air_temp': '9', 'dni': '300', 'ghi': '190', 'period_end': '2023-01-03T13:00:00Z', 'period': 'PT60M'}]

# pv_power_kw = calculate_pv_power(forecast_list, latitude, longitude, number_of_panels, area, azimuth, tilt, efficiency_panels, efficiency_invertor)
# print("PV Power Output:", pv_power_kw, "kW")
