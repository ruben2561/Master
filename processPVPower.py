import csv
import datetime
import json
import numpy as np
import pandas as pd
import pvlib
from datetime import datetime

from APIWeather import get_solar_data_openmeteo

# Function to get sample PV data from a CSV file
def get_sample_data_pv():
    try:
        with open("sampleData/solar_data_year_processed.csv", "r") as file:
            sample_data = file.read()
            reader = csv.DictReader(sample_data.splitlines())
            values_list = list(reader)
            pv_list = []
            for point in values_list:
                # Convert string to datetime
                period_end = datetime.strptime(point["time_value"], "%Y-%m-%dT%H:%M:%S")
                pv_list.append({
                    "pv_power_value": float(point["pv_power_value"]),
                    "time_value": period_end,
                })
            return pv_list
    except Exception as e:
        print(f"Error reading sample data: {e}")
        return None

# Function to calculate PV power output based on forecast data and system parameters
def calculate_pv_power(forecast_list, latitude, longitude, number_of_panels, area, azimuth, tilt, efficiency_panels,
                       efficiency_invertor, capacity_panels, capacity_invertor):
    pv_list = []

    # Ensure efficiencies are in decimal form
    if efficiency_panels > 1:
        efficiency_panels /= 100
    if efficiency_invertor > 1:
        efficiency_invertor /= 100

    # Get solar positions for the forecast periods
    solar_positions = pvlib.solarposition.get_solarposition(
        pd.to_datetime([data_point["period_end"] for data_point in forecast_list]), latitude, longitude)

    # Extract DNI, GHI, and DHI values from forecast data
    dnies = np.array([float(data_point["DNI"]) for data_point in forecast_list])
    ghies = np.array([float(data_point["GHI"]) for data_point in forecast_list])
    dhies = np.array([float(data_point["DHI"]) for data_point in forecast_list])

    # Calculate plane of array (POA) global irradiance
    poa_globals = pvlib.irradiance.get_total_irradiance(
        surface_tilt=tilt, surface_azimuth=azimuth, dni=dnies, ghi=ghies, dhi=dhies,
        solar_zenith=solar_positions['zenith'].values, solar_azimuth=solar_positions['azimuth'].values)['poa_global']

    # Estimate PV power output
    pv_estimates = (poa_globals * area * number_of_panels * efficiency_panels * efficiency_invertor) / 1000

    # Apply max panel power limit
    max_panel_power_total = capacity_panels * number_of_panels
    pv_estimates = np.minimum(pv_estimates, max_panel_power_total)

    # Apply max inverter power limit
    pv_estimates = np.minimum(pv_estimates, capacity_invertor)

    # Compile PV power data into a list
    for i, data_point in enumerate(forecast_list):
        pv_list.append({
            "pv_power_value": pv_estimates[i],
            "temperature_out": float(data_point["temp"]),
            "time_value": datetime.strptime(data_point["period_end"], "%Y-%m-%dT%H:%M"),
        })

    return pv_list

# Function to read PV data from a JSON file
def read_pv_list_from_file(filename):
    try:
        with open(filename, 'r') as file:
            pv_list = json.load(file)
        print(f"PV list loaded from {filename}")
        return pv_list
    except Exception as e:
        print(f"Error reading PV list from file: {e}")
        return None

# Function to process solar data and generate data points for PV power output
def process_solar_data(latitude, longitude, start_date, number_of_panels, area, azimuth, tilt, efficiency_panels,
                       efficiency_invertor, cap, inv_cap, use_api):
    # Get forecast data from the API
    forecast_data = get_solar_data_openmeteo(latitude, longitude, start_date)

    # Read forecast data into a list
    reader = csv.DictReader(forecast_data.splitlines())
    forecast_list = list(reader)

    # Calculate PV power output based on forecast data
    pv_list = calculate_pv_power(forecast_list, latitude, longitude, number_of_panels, area, azimuth, tilt,
                                 efficiency_panels, efficiency_invertor, cap, inv_cap)

    # Initialize list to store data for plotting as dictionaries
    data_points = []

    # Iterate over the forecast data and populate data points
    for data_point in pv_list:
        data_points.append({
            "pv_power_value": data_point['pv_power_value'],
            "temperature_out": data_point["temperature_out"],
            "time_value": data_point['time_value'],
            "soc_value": 0,
            "charge_value": 0,
            "discharge_value": 0,
            "price_battery_use": 0,
            "grid_injection": 0,
            "grid_offtake": 0,
            "power_usage_value": 0,
            "price_injection": 0,
            "price_offtake": 0,
            "ev_charge_value": 0,
            "heat_pump_value": 0,
        })

    return data_points