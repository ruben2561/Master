
import pvlib

def calculate_pv_power(latitude, longitude, capacity_kW, number_of_panels, azimuth, tilt, efficiency_panels, efficiency_invertor, DNI, GHI, air_temperature, time):
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
    # Calculate solar position
    solar_position = pvlib.solarposition.get_solarposition(specific_time, latitude, longitude)

    # Calculate AOI
    aoi = pvlib.irradiance.aoi(tilt, azimuth, solar_position['apparent_zenith'], solar_position['azimuth'])

    # Calculate PV power using SAPM (Sandia Array Performance Model)
    effective_irradiance = pvlib.pvsystem.sapm_effective_irradiance(aoi, DNI, GHI, solar_position['apparent_zenith'], solar_position['azimuth'])
    pv_system = {
        'surface_azimuth': azimuth,
        'surface_tilt': tilt,
        'albedo': 0.2,
        'module_parameters': pvlib.pvsystem.retrieve_sam('SandiaMod')
    }
    pv_power = pvlib.pvsystem.sapm(effective_irradiance, air_temperature, **pv_system)['p_mp']
    
    # Multiply by efficiency and return PV power in kW
    return pv_power * efficiency_panels

# Example usage
latitude = 50.9254992  # Example latitude (San Francisco)
longitude = 5.3932811  # Example longitude (San Francisco)
capacity_kw = 5  # Capacity of the PV system in kW
number_of_panels = 24
azimuth = 80  # Azimuth angle (orientation) of the PV panels (in degrees)
tilt = 45  # Tilt angle of the PV panels (in degrees)
efficiency_panels = 0.90  # Efficiency of the PV system
efficiency_invertor = 0.96
dni = 191  # Direct Normal Irradiance in W/m^2
ghi = 141  # Global Horizontal Irradiance in W/m^2
air_temperature = 17
specific_time = "2023-01-05T20:00:00Z"

pv_power_kw = calculate_pv_power(latitude, longitude, capacity_kw, number_of_panels, azimuth, tilt, efficiency_panels, efficiency_invertor, dni, ghi, air_temperature, specific_time)
print("PV Power Output:", pv_power_kw, "kW")
