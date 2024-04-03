
import csv
import datetime
import pvlib

from APISolcast import get_solar_data

def calculate_pv_power(forecast_list, latitude, longitude, capacity_kW, number_of_panels, azimuth, tilt, efficiency_panels, efficiency_invertor):
    """
    Calculate PV power output in kW using pvlib.

    Parameters:
        latitude (float): Latitude of the location in decimal degrees.
        longitude (float): Longitude of the location in decimal degrees.
        azimuth (float): Azimuth angle of the panels in degrees (0° - 360°).
        tilt (float): Tilt angle of the panels from horizontal in degrees (0° - 90°).
        efficiency (float): Efficiency of the PV system (0 - 1).
        air_temperature (float): Air temperature in Celsius.
        DNI (float): Direct Normal Irradiance in W/m^2.
        GHI (float): Global Horizontal Irradiance in W/m^2.

    Returns:
        float: PV power output in kW.
    """
    # # Calculate solar position
    # solar_position = pvlib.solarposition.get_solarposition(specific_time, latitude, longitude)

    # # Calculate AOI
    # aoi = pvlib.irradiance.aoi(tilt, azimuth, solar_position['apparent_zenith'], solar_position['azimuth'])

    # # Calculate PV power using SAPM (Sandia Array Performance Model)
    # effective_irradiance = pvlib.pvsystem.sapm_effective_irradiance(aoi, DNI, GHI, solar_position['apparent_zenith'], solar_position['azimuth'])
    # pv_system = {
    #     'surface_azimuth': azimuth,
    #     'surface_tilt': tilt,
    #     'albedo': 0.2,
    #     'module_parameters': pvlib.pvsystem.retrieve_sam('SandiaMod')
    # }
    # pv_power = pvlib.pvsystem.sapm(effective_irradiance, air_temperature, **pv_system)['p_mp']
    
    pv_list = []
    
    for data_point in forecast_list:
        pv_estimate = float(data_point["PvEstimate"])
        # print(data_point["PeriodEnd"])
        period_end = datetime.datetime.strptime(
            data_point["PeriodEnd"], "%Y-%m-%dT%H:%M:%SZ"
        )  # Convert string to datetime
        
        pv_list.append({
            "pv_power_value": pv_estimate,
            "time_value": period_end,
        })
    
    
    return pv_list


def process_solar_data(latitude, longitude, start_date, end_date):
    forecast_data = get_solar_data(
        latitude, longitude, start_date, end_date
    )
    
    reader = csv.DictReader(forecast_data.splitlines())
    forecast_list = list(reader)
    
    #pv_data = calculate_pv_power(forecast_list, latitude, longitude, capacity_kW, number_of_panels, azimuth, tilt, efficiency_panels, efficiency_invertor)
    pv_list = calculate_pv_power(forecast_list, latitude, longitude, 5, 24, 120, 45, 0.9, 0.9)


    # Initialize list to store data for plotting as tuples of (pv_power_value, time_value)
    data_points = []

    # Iterate over the forecast data
    for data_point in pv_list:
        # Store data point as a dictionary
        data_points.append(
            {
                "pv_power_value": data_point['pv_power_value'],
                "time_value": data_point['time_value'],
                "soc_value": 0,
                "charge_value": 0,
                "discharge_value": 0,
                "grid_injection": 0,
                "grid_extraction": 0,
                "power_usage_value": 0,
                "price_injection": 0,
                "price_extraction": 0,
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

# pv_power_kw = calculate_pv_power(latitude, longitude, capacity_kw, number_of_panels, azimuth, tilt, efficiency_panels, efficiency_invertor, dni, ghi, air_temperature, specific_time)
# print("PV Power Output:", pv_power_kw, "kW")
