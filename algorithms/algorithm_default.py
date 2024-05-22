def process_data(data_points, battery, ev_battery, ev_total_distance, OPEX):
    for i in range(len(data_points) - 1):
        current_point = data_points[i]
        next_point = data_points[i + 1]

        pv_power_value = current_point.get("pv_power_value", 0)
        power_usage_value = current_point.get("power_usage_value")
        time_value = current_point.get("time_value")
        next_time = next_point.get("time_value")
        ev_charge_value = current_point.get("ev_charge_value")
        heat_pump_value = current_point.get("heat_pump_value")

        #if time is 12:00 discharge the car an average amount to simulate car usage
        if time_value.hour == 12 and time_value.minute == 0:
            ev_battery.discharge(ev_charge_value, 1)
            current_point["ev_charge_value"] = 0

        if time_value and next_time:
            # Calculate time difference in hours

            time_difference_hours = (next_time - time_value).total_seconds() / 3600
            # Charge the battery based on the time difference
            
            ev_charged = 0
            
            #check if car is home so it can charge
            if(time_value.hour > 17 or time_value.hour < 8):
                ev_charged, ev_residue = ev_battery.charge(ev_battery.get_max_charge(), time_difference_hours)
                charge_discharge_battery = pv_power_value - power_usage_value - heat_pump_value - ev_charged
            else:
                charge_discharge_battery = pv_power_value - power_usage_value - heat_pump_value

            current_point["soc_value"] = battery.get_soc()

            if charge_discharge_battery > 0:
                charged, residue_to_much_energy = battery.charge(
                    charge_discharge_battery, time_difference_hours
                )
                current_point["grid_injection"] = residue_to_much_energy
                current_point["grid_offtake"] = 0
                current_point["charge_value"] = charged
                current_point["discharge_value"] = 0
                current_point["ev_charge_value"] = ev_charged
                price_battery_usage = (OPEX/2000) * charged

            elif charge_discharge_battery < 0:
                discharged, residue_to_little_energy = battery.discharge(
                    abs(charge_discharge_battery), time_difference_hours
                )
                current_point["grid_injection"] = 0
                current_point["grid_offtake"] = residue_to_little_energy
                current_point["charge_value"] = 0
                current_point["discharge_value"] = discharged
                current_point["ev_charge_value"] = ev_charged
                price_battery_usage = (OPEX/2000) * discharged

            else:
                current_point["grid_injection"] = 0
                current_point["grid_offtake"] = 0
                current_point["charge_value"] = 0
                current_point["discharge_value"] = 0
                current_point["ev_charge_value"] = ev_charged
                
            
                
            current_point["price_battery_use"] = price_battery_usage

    return data_points