
    #TODO aanpassen met heatpomp max power want alleen aaan uit dus staat altijd op max power, 
    #snacht temp checken dus voor tussen bepaalde uren niet opwarmen maar bij berekeken hoeveel binnen temp word door loss, en dan vananf bepaald uur weer beginnen opwarmen
    
def calculate_needed_power(area, COP_base, temp_in_desired, temp_in, U, temp_out):
    
    if(area == 0 or COP_base == 0 or temp_in == 0):
        return 0
    
    k = 0.025
    
    Q = (1.225 * 1005 * area * 2.4 * abs(temp_in_desired - temp_in)) / 3600 # 2.4 = standard ceiling height
    Q_loss = U * area * abs(temp_out - temp_in)
    
    COP = COP_base - k * (temp_in - temp_out) if (temp_in - temp_out) <= 15 else max(COP_base / 2, 2)  # Ensuring COP doesn't go unrealistically low
    print(str(COP))
    
    power_needed = ((Q + Q_loss) / COP)/1000 # * 3600 nodig?
    
    return power_needed

def calculate_indoor_temperature(temp_out, temp_in_initial, U, area, timestep=0.1):
    """
    Calculates the indoor temperature over a given time period without heating.
    
    Parameters:
        temp_out (float): Outdoor temperature in degrees Celsius.
        temp_in_initial (float): Initial indoor temperature in degrees Celsius.
        U (float): Overall heat transfer coefficient in W/(m²K).
        area (float): Surface area through which heat is being lost (in m²).
        volume (float): Volume of the indoor space (in m³).
        time_hours (float): Total time over which to calculate the temperature change (in hours).
        timestep (float): Time step for the Euler method (in hours).
    
    Returns:
        float: New indoor temperature in degrees Celsius after the specified time.
    """
    # Constants
    rho_air = 1.225  # Density of air (kg/m³)
    c_p = 1005       # Specific heat capacity of air (J/(kg·K))
    
    # Calculate the mass of air in the room
    mass_air = rho_air * area * 2.4
    
    # Initial indoor temperature
    temp_in = temp_in_initial
    
    # Convert time to seconds for the calculations
    total_seconds = 3600
    timestep_seconds = timestep * 3600
    
    # Simulation loop
    for t in range(0, int(total_seconds), int(timestep_seconds)):
        # Calculate heat loss rate (W)
        Q_loss = U * area * (temp_out - temp_in)
        
        # Calculate the rate of temperature change (dT/dt)
        dT_dt = Q_loss / (mass_air * c_p)
        
        # Update the indoor temperature
        temp_in -= dT_dt * timestep_seconds
        
    return temp_in

def process_heat_pump_data(data_points, area, cop, temp_desired, building):
    building_U_values = {
        "new": 0.175,
        "+-2010": 0.25,
        "+-2000": 0.375,
        "-1995": 0.525
    }
    
    U = building_U_values.get(building, 0.3)  # Default U value if building type not found

        
    #TODO toevoegen temp verlies snacht 
    # alleen doen if time = overdag
    # anders globale variabele van temp in bijhouden 
        
    temp_in_current = temp_desired
    for i in range(len(data_points) - 1):
        if data_points[i]["time_value"].hour >= 7 and data_points[i]["time_value"].hour <= 22:
            heat_pump_value = calculate_needed_power(area, cop, temp_desired, temp_in_current, U, data_points[i]["temperature_out"])
            temp_in_current = temp_desired
            data_points[i]["heat_pump_value"] = float(heat_pump_value)
        else:
            temp_in_current = calculate_indoor_temperature(data_points[i]["temperature_out"], temp_in_current, U, area)
            #print(str(temp_in_current))
            data_points[i]["heat_pump_value"] = 0
        
    return data_points