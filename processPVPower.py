
import csv
import datetime
from datetime import datetime
import json
import math
import numpy as np
import pandas as pd
import pvlib
from datetime import datetime


from APIWeather import get_solar_data_openmeteo

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
    
def calculate_pv_power3(forecast_list, latitude, longitude, number_of_panels, area, azimuth, tilt, efficiency_panels, efficiency_invertor):
    temperature_coefficient = -0.004  # per degree Celsius

    # Extract data from forecast_list
    temps = np.array([float(data_point["temp"]) for data_point in forecast_list])
    dnies = np.array([float(data_point["DNI"]) for data_point in forecast_list])
    ghies = np.array([float(data_point["GHI"]) for data_point in forecast_list])
    dhies = np.array([float(data_point["DHI"]) for data_point in forecast_list])
    times = pd.to_datetime([data_point["period_end"] for data_point in forecast_list])

    # Create DataFrame for weather data
    weather_data = pd.DataFrame({
        'temp_air': temps,
        'dni': dnies,
        'ghi': ghies,
        'dhi': dhies,
        'time': times
    })
    weather_data = weather_data.set_index('time')

    # Location object
    location = pvlib.location.Location(latitude, longitude)

    # Calculate solar position
    solar_position = location.get_solarposition(times)

    # PV system parameters
    system = {
        'surface_tilt': tilt,
        'surface_azimuth': azimuth,
        'module_parameters': {
            'pdc0': area * efficiency_panels * 1000,  # convert efficiency to W
            'gamma_pdc': temperature_coefficient
        },
        'inverter_parameters': {
            'pdc0': number_of_panels * area * efficiency_panels * 1000 * efficiency_invertor  # total system DC capacity
        }
    }

    # Calculate the POA (plane of array) irradiance
    aoi = pvlib.irradiance.aoi(system['surface_tilt'], system['surface_azimuth'],
                               solar_position['zenith'], solar_position['azimuth'])
    poa_sky_diffuse = pvlib.irradiance.haydavies(system['surface_tilt'], system['surface_azimuth'],
                                                 weather_data['dhi'], weather_data['dni'],
                                                 solar_position['zenith'], solar_position['azimuth'])
    poa_ground_diffuse = pvlib.irradiance.get_ground_diffuse(system['surface_tilt'], weather_data['ghi'])
    poa_direct = pvlib.irradiance.beam_component(system['surface_tilt'], system['surface_azimuth'],
                                                 solar_position['zenith'], solar_position['azimuth'],
                                                 weather_data['dni'])
    poa_global = poa_direct + poa_sky_diffuse + poa_ground_diffuse

    # Create a ModelChain object
    mc = pvlib.pvsystem.ModelChain(pvlib.pvsystem.PVSystem(surface_tilt=tilt,
                                                            surface_azimuth=azimuth,
                                                            module_parameters=system['module_parameters'],
                                                            inverter_parameters=system['inverter_parameters']),
                                   location)
    
    # Use ModelChain to calculate AC power output
    mc.run_model(times=weather_data.index, weather=weather_data)
    ac_power = mc.results.ac

    # Create DataFrame to save results
    data = {
        'time_value': weather_data.index,
        'temperature_out': temps,
        'DNI': dnies,
        'GHI': ghies,
        'DHI': dhies,
        'solar_zenith': solar_position['zenith'],
        'solar_azimuth': solar_position['azimuth'],
        'angle_of_incidence': aoi,
        'poa_global': poa_global,
        'ac_power': ac_power
    }

    df = pd.DataFrame(data)
    df.to_csv('pv_power_debug.csv', index=False)

    # Create a list of results for return
    pv_list = []
    for i in range(len(forecast_list)):
        pv_list.append({
            "pv_power_value": ac_power[i],
            "temperature_out": temps[i],
            "time_value": times[i],
        })

    return pv_list
    
    
def calculate_pv_power2(forecast_list, latitude, longitude, number_of_panels, area, azimuth, tilt, efficiency_panels, efficiency_invertor):
    temperature_coefficient = -0.004  # per degree Celsius
    
    temps = np.array([float(data_point["temp"]) for data_point in forecast_list])
    dnies = np.array([float(data_point["DNI"]) for data_point in forecast_list])
    ghies = np.array([float(data_point["GHI"]) for data_point in forecast_list])
    dhies = np.array([float(data_point["DHI"]) for data_point in forecast_list])
    times = pd.to_datetime([data_point["period_end"] for data_point in forecast_list])

    # Calculate solar position
    solar_positions = pvlib.solarposition.get_solarposition(
        pd.to_datetime([times for data_point in forecast_list]),
        latitude, longitude
    )
    
    #############
    # Ensure angles are in radians for numpy trig functions
    tilt_rad = np.radians(tilt)
    azimuth_rad = np.radians(azimuth)
    solar_zenith_rad = np.radians(solar_positions['zenith'].values)
    solar_azimuth_rad = np.radians(solar_positions['azimuth'].values)

    # Calculate angle of incidence
    angle_of_incidences = (
        np.cos(solar_zenith_rad) * np.cos(tilt_rad) +
        np.sin(solar_zenith_rad) * np.sin(tilt_rad) * np.cos(solar_azimuth_rad - azimuth_rad)
    )

    # Ensure angle_of_incidences is not negative
    angle_of_incidences = np.clip(angle_of_incidences, 0, 1)

    # Calculate incident solar radiation on the panels
    incident_solar_radiations = dnies * angle_of_incidences + dhies

    # Adjust panel efficiency for temperature
    adjusted_efficiency = efficiency_panels * (1 + temperature_coefficient * (temps - 25))

    # Calculate power output per panel
    power_outputs = area * incident_solar_radiations * adjusted_efficiency * efficiency_invertor

    # Calculate total power output for all panels
    pv_estimates = power_outputs * number_of_panels
    
    # Create a DataFrame to save results
    data = {
        "time_value": [datetime.strptime(data_point["period_end"], "%Y-%m-%dT%H:%M") for data_point in forecast_list],
        "temperature_out": temps,
        "DNI": dnies,
        "GHI": ghies,
        "DHI": dhies,
        "solar_zenith": solar_positions['zenith'].values,
        "solar_azimuth": solar_positions['azimuth'].values,
        "angle_of_incidence": angle_of_incidences,
        "incident_solar_radiation": incident_solar_radiations,
        "adjusted_efficiency": adjusted_efficiency,
        "power_output_per_panel": power_outputs,
        "pv_power_value": pv_estimates
    }

    df = pd.DataFrame(data)
    df.to_csv('pv_power_debug.csv', index=False)
    
    #############

    pv_list = []

    for i, data_point in enumerate(forecast_list):
        pv_list.append({
            "pv_power_value": pv_estimates[i],
            "temperature_out": float(data_point["temp"]),
            "time_value": datetime.strptime(data_point["period_end"], "%Y-%m-%dT%H:%M"),
        })

    return pv_list

def calculate_pv_power(forecast_list, latitude, longitude, number_of_panels, area, azimuth, tilt, efficiency_panels, efficiency_invertor, capacity_panels, capacity_invertor):
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
    
    # Apply max panel power limit
    max_panel_power_total = capacity_panels * number_of_panels
    pv_estimates = np.minimum(pv_estimates, max_panel_power_total)

    # Apply max inverter power limit
    pv_estimates = np.minimum(pv_estimates, capacity_invertor)
    

    for i, data_point in enumerate(forecast_list):
        pv_list.append({
            "pv_power_value": pv_estimates[i],
            "temperature_out": float(data_point["temp"]),
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
    forecast_data = get_solar_data_openmeteo(
        latitude, longitude, start_date
    )
    
    reader = csv.DictReader(forecast_data.splitlines())
    forecast_list = list(reader)
    
    pv_list = calculate_pv_power(forecast_list, latitude, longitude, number_of_panels, area, azimuth, tilt, efficiency_panels, efficiency_invertor, 5, 5)

    # Initialize list to store data for plotting as tuples of (pv_power_value, time_value)
    data_points = []

    # Iterate over the forecast data
    for data_point in pv_list:
        # Store data point as a dictionary
        #TODO fix /2
        data_points.append(
            {
                "pv_power_value": data_point['pv_power_value'],
                "temperature_out": data_point["temperature_out"], 
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
                "heat_pump_value": 0,
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
