# Function to calculate the power needed for heating based on given parameters
def calculate_needed_power(area, COP_base, temp_in_desired, temp_in, U, temp_out):
    # If any essential parameter is zero, return zero power needed
    if area == 0 or COP_base == 0 or temp_in_desired == 0:
        return 0

    k = 0.025  # Degradation factor for COP

    # Calculate the heating load (Q) required to achieve the desired indoor temperature
    Q = (1.225 * 1005 * area * 2.4 * abs(temp_in_desired - temp_in)) / 3600  # 2.4 = standard ceiling height
    # Calculate heat loss (Q_loss) through the building envelope
    Q_loss = U * area * abs(temp_out - temp_in)

    # Calculate the COP of the heat pump, ensuring it doesn't drop unrealistically low
    COP = COP_base - k * (temp_in - temp_out) if (temp_in - temp_out) <= 15 else max(COP_base / 2, 2)

    # Calculate the power needed for heating in kW
    power_needed = ((Q + Q_loss) / COP) / 1000

    return power_needed

# Function to calculate the indoor temperature over a given time period without heating
def calculate_indoor_temperature(temp_out, temp_in, U, area):
    """
    Calculates the indoor temperature over a given time period without heating.

    Parameters:
        temp_out (float): Outdoor temperature in degrees Celsius.
        temp_in (float): Initial indoor temperature in degrees Celsius.
        U (float): Overall heat transfer coefficient in W/(m²K).
        area (float): Surface area through which heat is being lost (in m²).

    Returns:
        float: New indoor temperature in degrees Celsius after the specified time.
    """

    # If area is zero, return zero temperature change
    if area == 0:
        return 0

    # Constants
    rho_air = 1.225  # Density of air (kg/m³)
    c_p = 1005  # Specific heat capacity of air (J/(kg·K))

    # Calculate the mass of air in the room
    mass_air = rho_air * area * 2.4

    # Calculate heat loss rate (W)
    Q_loss = U * area * (temp_out - temp_in) * 3600

    # Update the indoor temperature based on heat loss
    temp_in_new = temp_in + (Q_loss / (mass_air * c_p))

    return temp_in_new

# Function to process heat pump data points
def process_heat_pump_data(data_points, area, cop, temp_desired, certificate):
    # U values based on building energy certificate ratings
    certificate_U_values = {"A+": 0.15, "A": 0.25, "B": 0.35, "C": 0.5, "D": 0.7, "E": 0.9, "F": 1}

    # Get U value from certificate rating, default to 0.3 if not found
    U = certificate_U_values.get(certificate, 0.3)

    # Initialize current indoor temperature to the desired temperature
    temp_in_current = temp_desired

    # Loop through data points to calculate heat pump usage
    for i in range(len(data_points) - 1):
        # Check if within heating hours and current temp is below desired temp
        if 7 <= data_points[i]["time_value"].hour <= 22 and temp_in_current <= temp_desired:
            # Calculate needed power and set current temperature to desired
            heat_pump_value = calculate_needed_power(area, cop, temp_desired, temp_in_current, U, data_points[i]["temperature_out"])
            temp_in_current = temp_desired
            data_points[i]["heat_pump_value"] = float(heat_pump_value)
        else:
            # Calculate new indoor temperature without heating
            temp_in_current = calculate_indoor_temperature(data_points[i]["temperature_out"], temp_in_current, U, area)
            data_points[i]["heat_pump_value"] = 0

    return data_points
