def process_point_optimized(time_difference_hours, time_value, pv_power_values, power_usage_values,
                            offtake_price_values, injection_price_values, heat_pump_values, temp_out_values, soc_value, battery,
                            ev_battery, OPEX, temp_desired):
    grid_injection = 0
    grid_offtake = 0
    charge_value = 0
    discharge_value = 0
    ev_charged = 0

    ##############################
    ### Guide ####################
    #
    # Battery Functions:
    #
    # battery.charge(power, time):
    #   Simulate battery charging while considering limitations.
    #   Parameters:
    #     power: Charging power in kW
    #     time: Charging time in hours
    #   Returns:
    #     charged: Amount of energy charged in kWh
    #     residue_to_much_energy: Remaining energy that could not be stored in the battery due to capacity limits in kWh
    # 
    # battery.discharge(power, time):
    #   Simulate battery discharging while considering limitations.
    #   Parameters:
    #     power: Discharging power in kW
    #     time: Discharging time in hours
    #   Returns:
    #     discharged: Amount of energy discharged in kWh
    #     residue_to_little_energy: Remaining energy needed from the grid to fulfill demand due to capacity limits in kWh
    # 
    # battery.get_soc() --- Get the current State of Charge (SoC) of the battery in kWh. 
    # battery.is_full() --- Check if the battery is fully charged.
    # battery.get_max_charge() --- Get the maximum charging power of the battery in kW.
    # battery.get_max_discharge() --- Get the maximum discharging power of the battery in kW.
    # battery.get_max_discharge() --- Get the maximum capacity of the battery in kWh
    #
    ##################################################################################################################################
    #
    # For every parameter this function will recieve a list of the current value and 23 hour ahead, simulation day ahead values
    # Function Parameters:
    #
    # time_difference_hours: Time difference between consecutive data points in hours
    # time_value: Date and time of current state formatted like: "YYYY-MM-DD HH:MM:SS"
    # pv_power_values: Power generated by solar panels in kilowatt-hours (kWh) of the current and next 23 hours
    # power_usage_values: Power consumed by household in kilowatt-hours (kWh) of the current and next 23 hours
    # offtake_price_values: Price for extracting energy from the grid in (€/MWh) of the current and next 23 hours
    # injection_price_values: Price for injecting excess energy into the grid in (€/MWh) of the current and next 23 hours
    # heat_pump_value: Power consumed to keep house at desired temp (kWh) of the current and next 23 hours
    # temp_out: Temperature outside in (°C) of the current and next 23 hours
    # soc_value: Current State of Charge (SoC) of the battery in kilowatt-hours (kWh) 
    # battery: Battery instance used for simulation
    # ev_battery: Ev_battery instance used for simulation
    # OPEX: Price for a full cycle of the battery (€/MWh) 
    # temp_desired: Temperature the hosue needs to be kept at (°C)
    # 
    ###################################################################################################################################
    #
    # Returns:
    # grid_injection: Amount of energy injected into the grid in kWh
    # grid_offtake: Amount of energy extracted from the grid in kWh
    # charge_value: Amount of energy charged into the battery in kWh
    # discharge_value: Amount of energy discharged from the battery in kWh

    ###############################################################
    ### Algoritm code begins here #################################
    ###############################################################

    if time_value.hour > 17 or time_value.hour < 8:
        ev_charged, ev_residue = ev_battery.charge(ev_battery.get_max_charge(), time_difference_hours)
        charge_discharge_battery = pv_power_values[0] - power_usage_values[0] - heat_pump_values[0] - ev_charged
    else:
        charge_discharge_battery = pv_power_values[0] - power_usage_values[0] - heat_pump_values[0]

    if charge_discharge_battery > 0:
        charged, residue_to_much_energy = battery.charge(charge_discharge_battery, time_difference_hours)
        grid_injection = residue_to_much_energy
        charge_value = charged

    elif charge_discharge_battery < 0:
        discharged, residue_to_little_energy = battery.discharge(
            abs(charge_discharge_battery), time_difference_hours
        )
        grid_offtake = residue_to_little_energy
        discharge_value = discharged
        ev_charge_value = ev_charged

    if time_value.hour > 17 or time_value.hour < 8:
        if offtake_price_values[0] <= 40:
            charged, residue_to_much_energy = battery.charge(battery.get_max_charge(), time_difference_hours)
            charge_value += charged
            grid_offtake += charged

    ###############################################################
    ### Algoritm code ends here ###################################
    ###############################################################
    
    price_battery_usage = ((OPEX / 2000) * charge_value) + ((OPEX / 2000) * discharge_value)

    return grid_injection, grid_offtake, charge_value, discharge_value, ev_charged, price_battery_usage


def process_data(data_points, battery, ev_battery, ev_total_distance, OPEX, temp_desired):
    for i in range(len(data_points) - 1):
        current_point = data_points[i]
        data_points_copy = data_points + data_points[0:24]
        current_points = data_points_copy[i:i + 24]

        pv_power_values = [point.get("pv_power_value", 0) for point in current_points]
        power_usage_values = [point.get("power_usage_value", 0) for point in current_points]
        offtake_price_values = [point.get("price_offtake", 0) for point in current_points]
        injection_price_values = [point.get("price_injection", 0) for point in current_points]
        heat_pump_values = [point.get("heat_pump_value", 0) for point in current_points]
        temp_out_values = [point.get("temperature_out", 0) for point in current_points]
        ev_charge_values = [point.get("ev_charge_value", 0) for point in current_points]
        time_value = current_points[0].get("time_value")
        soc_value = battery.get_soc()
        next_time = current_points[1].get("time_value")

        # if time is 12:00 discharge the car an average amount to simulate car usage
        if time_value.hour == 12 and time_value.minute == 0:
            ev_battery.discharge(ev_charge_values[0], 1)
            current_point["ev_charge_value"] = 0

        if time_value and next_time:
            time_difference_hours = (next_time - time_value).total_seconds() / 3600

            grid_injection, grid_offtake, charge_value, discharge_value, ev_charged, price_battery_usage = process_point_optimized(
                        time_difference_hours, time_value, pv_power_values, power_usage_values,
                        offtake_price_values, injection_price_values, heat_pump_values, temp_out_values, soc_value, battery,
                        ev_battery, OPEX, temp_desired)

            current_point["soc_value"] = soc_value
            current_point["grid_injection"] = grid_injection
            current_point["grid_offtake"] = grid_offtake
            current_point["charge_value"] = charge_value
            current_point["discharge_value"] = discharge_value
            current_point["ev_charge_value"] = ev_charged
            current_point["price_battery_use"] = price_battery_usage

    return data_points
