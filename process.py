from collections import defaultdict
import copy
import random
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from battery import Battery
from APIWeather import get_solar_data_solcast
import csv
import matplotlib.dates as mdates
import datetime
from datetime import datetime

def process_point_optimized(time_difference_hours, time_value, pv_power_values, power_usage_values, offtake_price_values, injection_price_values, soc_value, battery, ev_battery):
    
    grid_injection = 0
    grid_offtake = 0
    charge_value = 0
    discharge_value = 0
    
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
    #
    #
    # Function Parameters:
    # time_difference_hours: Time difference between consecutive data points in hours
    # time_value: Date and time of current state formatted like: "YYYY-MM-DD HH:MM:SS"
    # pv_power_values: Power generated by solar panels in kilowatt-hours (kWh) of the current and next 23 hours
    # power_usage_values: Power consumed by household in kilowatt-hours (kWh) of the current and next 23 hours
    # offtake_price_values: Price for extracting energy from the grid in (€/MWh) of the current and next 23 hours
    # injection_price_values: Price for injecting excess energy into the grid in (€/MWh) of the current and next 23 hours
    # soc_value: Current State of Charge (SoC) of the battery in kilowatt-hours (kWh)
    # battery: Battery instance used for simulation
    # 
    #
    # Returns:
    # grid_injection: Amount of energy injected into the grid in kWh
    # grid_offtake: Amount of energy extracted from the grid in kWh
    # charge_value: Amount of energy charged into the battery in kWh
    # discharge_value: Amount of energy discharged from the battery in kWh
    
    ###############################################################
    ### Algoritm code below #######################################
    ###############################################################
    
    algoritm_to_use = 2
    
    ##111111111####################################################
    if algoritm_to_use == 1:
        
        ev_charged = 0
            
        if(time_value.hour >= 17 or time_value.hour <= 8):
            ev_charged, ev_residue = ev_battery.charge(100, time_difference_hours)
            charge_discharge_battery = pv_power_values[0] - power_usage_values[0] - ev_charged
        else:
            charge_discharge_battery = pv_power_values[0] - power_usage_values[0]

        if charge_discharge_battery > 0:
            charged, residue_to_much_energy = battery.charge(charge_discharge_battery, time_difference_hours)
            grid_injection = residue_to_much_energy
            charge_value = charged

        elif charge_discharge_battery < 0:
            discharged, residue_to_little_energy = battery.discharge(abs(charge_discharge_battery), time_difference_hours)
            grid_offtake = residue_to_little_energy
            discharge_value = discharged
            
        if offtake_price_values[0] <= 50:
            charged, residue_to_much_energy = battery.charge(battery.get_max_charge(), time_difference_hours)
            charge_value += charged
            grid_offtake += charged
    ##1111111111####################################################
    
    ##2222222222####################################################
    elif algoritm_to_use == 2:
        
        ev_charged = 0
            
        if(time_value.hour >= 17 or time_value.hour <= 8):
            ev_charged, ev_residue = ev_battery.charge(100, time_difference_hours)
            charge_discharge_battery = pv_power_values[0] - power_usage_values[0] - ev_charged
        else:
            charge_discharge_battery = pv_power_values[0] - power_usage_values[0]

        if charge_discharge_battery > 0:
            charged, residue_to_much_energy = battery.charge(charge_discharge_battery, time_difference_hours)
            grid_injection = residue_to_much_energy
            charge_value = charged

        elif charge_discharge_battery < 0:
            discharged, residue_to_little_energy = battery.discharge(abs(charge_discharge_battery), time_difference_hours)
            grid_offtake = residue_to_little_energy
            discharge_value = discharged
        
        if offtake_price_values[0] <= 100 and sum(offtake_price_values[5:10])/len(offtake_price_values[5:10]) > 120 and sum(pv_power_values)/len(pv_power_values) < sum(power_usage_values)/len(power_usage_values):
                
            charged, residue_to_much_energy = battery.charge(battery.get_max_charge(), time_difference_hours)
            charge_value += charged
            grid_offtake += charged
    ##2222222222####################################################
        
    ################################################################
    ################################################################
    ################################################################

    return grid_injection, grid_offtake, charge_value, discharge_value, ev_charged


def process_data_optimized(data_points, battery, ev_battery, ev_total_distance):
    for i in range(len(data_points) - 1):
        current_point = data_points[i]
        data_points_copy = data_points + data_points[0:24]
        current_points = data_points_copy[i:i+24]

        pv_power_values = [point.get("pv_power_value", 0) for point in current_points]
        power_usage_values = [point.get("power_usage_value", 0) for point in current_points]
        offtake_price_values = [point.get("price_offtake", 0) for point in current_points]
        injection_price_values = [point.get("price_injection", 0) for point in current_points]
        time_value = current_points[0].get("time_value")
        soc_value = battery.get_soc()
        next_time = current_points[1].get("time_value")
        
        car_charge_day = ((ev_total_distance/100) * 15) / 365  #average car uses 15kWh/100km
        
        if time_value.hour == 0 and time_value.minute == 0:
            ev_battery.discharge(15, (car_charge_day / 15))

        if time_value and next_time:
            time_difference_hours = (next_time - time_value).total_seconds() / 3600
            
            grid_injection, grid_offtake, charge_value, discharge_value, ev_charged = process_point_optimized(time_difference_hours, time_value, pv_power_values, power_usage_values, offtake_price_values, injection_price_values, soc_value, battery, ev_battery)
            
            current_point["soc_value"] = soc_value
            current_point["grid_injection"] = grid_injection
            current_point["grid_offtake"] = grid_offtake
            current_point["charge_value"] = charge_value
            current_point["discharge_value"] = discharge_value
            current_point["ev_charge_value"] = ev_charged 

    return data_points

def process_data(data_points, battery, ev_battery, ev_total_distance):
    for i in range(len(data_points) - 1):
        current_point = data_points[i]
        next_point = data_points[i + 1]

        pv_power_value = current_point.get("pv_power_value", 0)
        power_usage_value = current_point.get("power_usage_value")
        time_value = current_point.get("time_value")
        next_time = next_point.get("time_value")
        
        car_charge_day = ((ev_total_distance/100) * 15) / 365  #average car uses 15kWh/100km
        
        if time_value.hour == 0 and time_value.minute == 0:
            ev_battery.discharge(15, (car_charge_day / 15))

        if time_value and next_time:
            # Calculate time difference in hours

            time_difference_hours = (next_time - time_value).total_seconds() / 3600
            # Charge the battery based on the time difference
            
            ev_charged = 0
            
            if(time_value.hour >= 17 or time_value.hour <= 8):
                ev_charged, ev_residue = ev_battery.charge(100, time_difference_hours)
                charge_discharge_battery = pv_power_value - power_usage_value - ev_charged
            else:
                charge_discharge_battery = pv_power_value - power_usage_value

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

            elif charge_discharge_battery < 0:
                discharged, residue_to_little_energy = battery.discharge(
                    abs(charge_discharge_battery), time_difference_hours
                )
                current_point["grid_injection"] = 0
                current_point["grid_offtake"] = residue_to_little_energy
                current_point["charge_value"] = 0
                current_point["discharge_value"] = discharged
                current_point["ev_charge_value"] = ev_charged

            else:
                current_point["grid_injection"] = 0
                current_point["grid_offtake"] = 0
                current_point["charge_value"] = 0
                current_point["discharge_value"] = 0
                current_point["ev_charge_value"] = ev_charged

    return data_points


def get_power_usage_values(data_points, selected_user_profile):
    profile = "consumptionProfile/profile_" + selected_user_profile + ".csv"
    try:
        with open(profile, "r") as file:
            sample_data = file.read()

            if sample_data:
                # Parse CSV data into list of dictionaries
                reader = csv.DictReader(sample_data.splitlines())
                samples_list = list(reader)

            for i in range(len(data_points) - 1):
                data_points[i]["power_usage_value"] = float(samples_list[i]["Power"]) + float(samples_list[i]["Power"]) * random.uniform(-0.1, 0.1)
            

        return data_points

    except Exception as e:
        print(f"Error reading sample data power usage: {e}")
        return None


def calculate_values(data_points, specific_time, scale):

    if scale == "SPECIFIC DAY":
        # Filter data points for the first day
        day_data_points = [
            point
            for point in data_points
            if point["time_value"].day == int(specific_time.split("-")[0]) and point["time_value"].strftime("%B") == specific_time.split("-")[1]
        ]  # Modify the date accordingly
        data_points = day_data_points

        # Perform some calculations to get new data
        time_values = [point["time_value"] for point in data_points]
        pv_power_sums = [point["pv_power_value"] for point in data_points]
        power_usage_sums = [-point["power_usage_value"] for point in data_points]
        charge_sums = [-point["charge_value"] for point in data_points]
        discharge_sums = [point["discharge_value"] for point in data_points]
        soc_sums = [point["soc_value"] for point in data_points]
        grid_injection_sums = [-point["grid_injection"] for point in data_points]
        grid_offtake_sums = [point["grid_offtake"] for point in data_points]
        prices_injection = [point["price_injection"] for point in data_points]
        prices_offtake = [point["price_offtake"] for point in data_points]
        ev_charge_sums = [-point["ev_charge_value"] for point in data_points]
        line_width = 0.04
        title = "Not Optimized - Hourly Data For Date " + str(specific_time) + " In 2023"

        
        # Calculate cost for grid injection and grid offtake
        grid_injection_costs = [x * y / 1000 for x, y in zip(grid_injection_sums, prices_injection)]
        grid_offtake_costs = [x * y / 1000 for x, y in zip(grid_offtake_sums, prices_offtake)]

        # Calculate sum of costs
        grid_injection_costs_total = sum(grid_injection_costs)
        grid_offtake_costs_total = sum(grid_offtake_costs)
        
        grid_injection_sum = sum(grid_injection_sums)
        grid_offtake_sum = sum(grid_offtake_sums)
        

    if scale == "SPECIFIC WEEK":
        
        # Dictionary mapping month names to numerical values
        month_to_num = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }

        # Split the date string into day and month
        day, month_name = specific_time.split("-")

        month_num = month_to_num[month_name]
        date_obj = datetime.strptime(f"2024-{month_num}-{day}", "%Y-%m-%d")
        week_number = date_obj.isocalendar()[1]
        
         # Filter data points for the first month
        month_data_points = [
            point
            for point in data_points
            if (point["time_value"].month, point["time_value"].day) == (1, 1) and 1 == int(week_number)
            or (point["time_value"].month, point["time_value"].day) != (1, 1) and point["time_value"].isocalendar()[1] == int(week_number)
        ]  # Modify the date accordingly
        data_points = month_data_points
        
        # Assuming time_values contains datetime objects
        # If time_values contains strings, convert them to datetime objects first
        time_values = [point["time_value"] for point in data_points]
        pv_power_values = [point["pv_power_value"] for point in data_points]
        power_usage_values = [-point["power_usage_value"] for point in data_points]
        charge_values = [-point["charge_value"] for point in data_points]
        discharge_values = [point["discharge_value"] for point in data_points]
        soc_values = [point["soc_value"] for point in data_points]
        grid_injection_values = [-point["grid_injection"] for point in data_points]
        grid_offtake_values = [point["grid_offtake"] for point in data_points]
        prices_injection = [point["price_injection"] for point in data_points]
        prices_offtake = [point["price_offtake"] for point in data_points]
        ev_charge_values = [-point["ev_charge_value"] for point in data_points]
        
        # Calculate cost for grid injection and grid offtake
        grid_injection_costs = [x * y / 1000 for x, y in zip(grid_injection_values, prices_injection)]
        grid_offtake_costs = [x * y / 1000 for x, y in zip(grid_offtake_values, prices_offtake)]

        # Calculate sum of costs
        grid_injection_costs_total = sum(grid_injection_costs)
        grid_offtake_costs_total = sum(grid_offtake_costs)
        
        grid_injection_sum = sum(grid_injection_values)
        grid_offtake_sum = sum(grid_offtake_values)

        # Create a defaultdict to store sums for each day
        daily_sums = defaultdict(lambda: defaultdict(float))

        # Iterate over the data_points and accumulate sums for each day
        for time_value, pv_power, power_usage, charge, discharge, grid_injection, grid_offtake, ev_charge in zip(
            time_values, pv_power_values, power_usage_values, charge_values, discharge_values, grid_injection_values, grid_offtake_values, ev_charge_values
        ):
            # Extract day from the datetime object
            day = time_value.date()
            
            # Accumulate sums for each column for the corresponding day
            daily_sums[day]['pv_power'] += pv_power
            daily_sums[day]['power_usage'] += power_usage
            daily_sums[day]['charge'] += charge
            daily_sums[day]['discharge'] += discharge
            daily_sums[day]['grid_injection'] += grid_injection
            daily_sums[day]['grid_offtake'] += grid_offtake
            daily_sums[day]['ev_charge'] += ev_charge

        pv_power_sums = [sums['pv_power'] for sums in daily_sums.values()]
        power_usage_sums = [sums['power_usage'] for sums in daily_sums.values()]
        charge_sums = [sums['charge'] for sums in daily_sums.values()]
        discharge_sums = [sums['discharge'] for sums in daily_sums.values()]
        grid_injection_sums = [sums['grid_injection'] for sums in daily_sums.values()]
        grid_offtake_sums = [sums['grid_offtake'] for sums in daily_sums.values()]
        ev_charge_sums = [sums['ev_charge'] for sums in daily_sums.values()]
        time_values = list(daily_sums.keys())
        line_width = 0.95
        title = "Not Optimized - Dayly Data For Week " + str(week_number) + " In 2023"
        
        soc_sums = soc_values
    
    
    if scale == "SPECIFIC MONTH":
         # Filter data points for the first month
        month_data_points = [
            point
            for point in data_points
            if point["time_value"].strftime("%B") == specific_time.split("-")[1]
        ]  # Modify the date accordingly
        data_points = month_data_points
        
        # Assuming time_values contains datetime objects
        # If time_values contains strings, convert them to datetime objects first
        time_values = [point["time_value"] for point in data_points]
        pv_power_values = [point["pv_power_value"] for point in data_points]
        power_usage_values = [-point["power_usage_value"] for point in data_points]
        charge_values = [-point["charge_value"] for point in data_points]
        discharge_values = [point["discharge_value"] for point in data_points]
        soc_values = [point["soc_value"] for point in data_points]
        grid_injection_values = [-point["grid_injection"] for point in data_points]
        grid_offtake_values = [point["grid_offtake"] for point in data_points]
        prices_injection = [point["price_injection"] for point in data_points]
        prices_offtake = [point["price_offtake"] for point in data_points]
        ev_charge_values = [-point["ev_charge_value"] for point in data_points]
        
        # Calculate cost for grid injection and grid offtake
        grid_injection_costs = [x * y / 1000 for x, y in zip(grid_injection_values, prices_injection)]
        grid_offtake_costs = [x * y / 1000 for x, y in zip(grid_offtake_values, prices_offtake)]

        # Calculate sum of costs
        grid_injection_costs_total = sum(grid_injection_costs)
        grid_offtake_costs_total = sum(grid_offtake_costs)
        
        grid_injection_sum = sum(grid_injection_values)
        grid_offtake_sum = sum(grid_offtake_values)

        # Create a defaultdict to store sums for each day
        daily_sums = defaultdict(lambda: defaultdict(float))

        # Iterate over the data_points and accumulate sums for each day
        for time_value, pv_power, power_usage, charge, discharge, grid_injection, grid_offtake, ev_charge in zip(
            time_values, pv_power_values, power_usage_values, charge_values, discharge_values, grid_injection_values, grid_offtake_values, ev_charge_values
        ):
            # Extract day from the datetime object
            day = time_value.date()
            
            # Accumulate sums for each column for the corresponding day
            daily_sums[day]['pv_power'] += pv_power
            daily_sums[day]['power_usage'] += power_usage
            daily_sums[day]['charge'] += charge
            daily_sums[day]['discharge'] += discharge
            daily_sums[day]['grid_injection'] += grid_injection
            daily_sums[day]['grid_offtake'] += grid_offtake
            daily_sums[day]['ev_charge'] += ev_charge

        pv_power_sums = [sums['pv_power'] for sums in daily_sums.values()]
        power_usage_sums = [sums['power_usage'] for sums in daily_sums.values()]
        charge_sums = [sums['charge'] for sums in daily_sums.values()]
        discharge_sums = [sums['discharge'] for sums in daily_sums.values()]
        grid_injection_sums = [sums['grid_injection'] for sums in daily_sums.values()]
        grid_offtake_sums = [sums['grid_offtake'] for sums in daily_sums.values()]
        ev_charge_sums = [sums['ev_charge'] for sums in daily_sums.values()]
        time_values = list(daily_sums.keys())
        line_width = 0.9
        title = "Not Optimized - Dayly Data For Month " + str(specific_time) + " In 2023"
        
        soc_sums = soc_values
    
    if scale == "PER YEAR":
        # Assuming time_values contains datetime objects
        # If time_values contains strings, convert them to datetime objects first
        time_values = [point["time_value"] for point in data_points]
        pv_power_values = [point["pv_power_value"] for point in data_points]
        power_usage_values = [-point["power_usage_value"] for point in data_points]
        charge_values = [-point["charge_value"] for point in data_points]
        discharge_values = [point["discharge_value"] for point in data_points]
        soc_values = [point["soc_value"] for point in data_points]
        grid_injection_values = [-point["grid_injection"] for point in data_points]
        grid_offtake_values = [point["grid_offtake"] for point in data_points]
        prices_injection = [point["price_injection"] for point in data_points]
        prices_offtake = [point["price_offtake"] for point in data_points]
        ev_charge_values = [-point["ev_charge_value"] for point in data_points]
        
        # Calculate cost for grid injection and grid offtake
        grid_injection_costs = [x * y / 1000 for x, y in zip(grid_injection_values, prices_injection)]
        grid_offtake_costs = [x * y / 1000 for x, y in zip(grid_offtake_values, prices_offtake)]

        # Calculate sum of costs
        grid_injection_costs_total = sum(grid_injection_costs)
        grid_offtake_costs_total = sum(grid_offtake_costs)
        
        grid_injection_sum = sum(grid_injection_values)
        grid_offtake_sum = sum(grid_offtake_values)
        
        # Create a defaultdict to store sums for each day
        daily_sums = defaultdict(lambda: defaultdict(float))

        # Iterate over the data_points and accumulate sums for each day
        for time_value, pv_power, power_usage, charge, discharge, soc, grid_injection, grid_offtake, ev_charge in zip(
            time_values, pv_power_values, power_usage_values, charge_values, discharge_values, soc_values, grid_injection_values, grid_offtake_values, ev_charge_values
        ):
        
            year_year = time_value.year
            
            # Accumulate sums for each column for the corresponding day
            daily_sums[year_year]['pv_power'] += pv_power
            daily_sums[year_year]['power_usage'] += power_usage
            daily_sums[year_year]['charge'] += charge
            daily_sums[year_year]['discharge'] += discharge
            daily_sums[year_year]['soc'] += soc
            daily_sums[year_year]['grid_injection'] += grid_injection
            daily_sums[year_year]['grid_offtake'] += grid_offtake
            daily_sums[year_year]['ev_charge'] += ev_charge

        pv_power_sums = [sums['pv_power'] for sums in daily_sums.values()]
        power_usage_sums = [sums['power_usage'] for sums in daily_sums.values()]
        charge_sums = [sums['charge'] for sums in daily_sums.values()]
        discharge_sums = [sums['discharge'] for sums in daily_sums.values()]
        soc_sums = [sums['soc'] for sums in daily_sums.values()]
        grid_injection_sums = [sums['grid_injection'] for sums in daily_sums.values()]
        grid_offtake_sums = [sums['grid_offtake'] for sums in daily_sums.values()]
        ev_charge_sums = [sums['ev_charge'] for sums in daily_sums.values()]
        time_values = list(daily_sums.keys())
        line_width = 2
        title = "Not Optimized - Yealy Data For 2023"
        
        soc_sums = [x /(365*24) for x in soc_sums]
        
    if scale == "PER MONTH":
        # Assuming time_values contains datetime objects
        # If time_values contains strings, convert them to datetime objects first
        time_values = [point["time_value"] for point in data_points]
        pv_power_values = [point["pv_power_value"] for point in data_points]
        power_usage_values = [-point["power_usage_value"] for point in data_points]
        charge_values = [-point["charge_value"] for point in data_points]
        discharge_values = [point["discharge_value"] for point in data_points]
        soc_values = [point["soc_value"] for point in data_points]
        grid_injection_values = [-point["grid_injection"] for point in data_points]
        grid_offtake_values = [point["grid_offtake"] for point in data_points]
        prices_injection = [point["price_injection"] for point in data_points]
        prices_offtake = [point["price_offtake"] for point in data_points]
        ev_charge_values = [-point["ev_charge_value"] for point in data_points]
        
        # Calculate cost for grid injection and grid offtake
        grid_injection_costs = [x * y / 1000 for x, y in zip(grid_injection_values, prices_injection)]
        grid_offtake_costs = [x * y / 1000 for x, y in zip(grid_offtake_values, prices_offtake)]

        # Calculate sum of costs
        grid_injection_costs_total = sum(grid_injection_costs)
        grid_offtake_costs_total = sum(grid_offtake_costs)
        
        grid_injection_sum = sum(grid_injection_values)
        grid_offtake_sum = sum(grid_offtake_values)

        # Create a defaultdict to store sums for each day
        daily_sums = defaultdict(lambda: defaultdict(float))

        # Iterate over the data_points and accumulate sums for each day
        for time_value, pv_power, power_usage, charge, discharge, soc, grid_injection, grid_offtake, ev_charge in zip(
            time_values, pv_power_values, power_usage_values, charge_values, discharge_values, soc_values, grid_injection_values, grid_offtake_values, ev_charge_values
        ):
        
            year_month = time_value.month
            
            # Accumulate sums for each column for the corresponding day
            daily_sums[year_month]['pv_power'] += pv_power
            daily_sums[year_month]['power_usage'] += power_usage
            daily_sums[year_month]['charge'] += charge
            daily_sums[year_month]['discharge'] += discharge
            daily_sums[year_month]['soc'] += soc
            daily_sums[year_month]['grid_injection'] += grid_injection
            daily_sums[year_month]['grid_offtake'] += grid_offtake
            daily_sums[year_month]['ev_charge'] += ev_charge

        pv_power_sums = [sums['pv_power'] for sums in daily_sums.values()]
        power_usage_sums = [sums['power_usage'] for sums in daily_sums.values()]
        charge_sums = [sums['charge'] for sums in daily_sums.values()]
        discharge_sums = [sums['discharge'] for sums in daily_sums.values()]
        soc_sums = [sums['soc'] for sums in daily_sums.values()]
        grid_injection_sums = [sums['grid_injection'] for sums in daily_sums.values()]
        grid_offtake_sums = [sums['grid_offtake'] for sums in daily_sums.values()]
        ev_charge_sums = [sums['ev_charge'] for sums in daily_sums.values()]
        time_values = list(daily_sums.keys())
        line_width = 0.9
        title = "Not Optimized - Montly Data For 2023"
        
        soc_sums = [x /(30.5*24) for x in soc_sums]
        
    if scale == "PER WEEK":
        # Assuming time_values contains datetime objects
        # If time_values contains strings, convert them to datetime objects first
        time_values = [point["time_value"] for point in data_points]
        pv_power_values = [point["pv_power_value"] for point in data_points]
        power_usage_values = [-point["power_usage_value"] for point in data_points]
        charge_values = [-point["charge_value"] for point in data_points]
        discharge_values = [point["discharge_value"] for point in data_points]
        soc_values = [point["soc_value"] for point in data_points]
        grid_injection_values = [-point["grid_injection"] for point in data_points]
        grid_offtake_values = [point["grid_offtake"] for point in data_points]
        prices_injection = [point["price_injection"] for point in data_points]
        prices_offtake = [point["price_offtake"] for point in data_points]
        ev_charge_values = [-point["ev_charge_value"] for point in data_points]
        
        # Calculate cost for grid injection and grid offtake
        grid_injection_costs = [x * y / 1000 for x, y in zip(grid_injection_values, prices_injection)]
        grid_offtake_costs = [x * y / 1000 for x, y in zip(grid_offtake_values, prices_offtake)]

        # Calculate sum of costs
        grid_injection_costs_total = sum(grid_injection_costs)
        grid_offtake_costs_total = sum(grid_offtake_costs)
        
        grid_injection_sum = sum(grid_injection_values)
        grid_offtake_sum = sum(grid_offtake_values)

        # Create a defaultdict to store sums for each day
        daily_sums = defaultdict(lambda: defaultdict(float))

        # Iterate over the data_points and accumulate sums for each day
        for time_value, pv_power, power_usage, charge, discharge, soc, grid_injection, grid_offtake, ev_charge in zip(
            time_values, pv_power_values, power_usage_values, charge_values, discharge_values, soc_values, grid_injection_values, grid_offtake_values, ev_charge_values
        ):
            

            year_week = time_value.isocalendar()[1]
            if time_value.month == 1 and time_value.day == 1:
                year_week = 1
            
            # Accumulate sums for each column for the corresponding day
            daily_sums[year_week]['pv_power'] += pv_power
            daily_sums[year_week]['power_usage'] += power_usage
            daily_sums[year_week]['charge'] += charge
            daily_sums[year_week]['discharge'] += discharge
            daily_sums[year_week]['soc'] += soc
            daily_sums[year_week]['grid_injection'] += grid_injection
            daily_sums[year_week]['grid_offtake'] += grid_offtake
            daily_sums[year_week]['ev_charge'] += ev_charge

        pv_power_sums = [sums['pv_power'] for sums in daily_sums.values()]
        power_usage_sums = [sums['power_usage'] for sums in daily_sums.values()]
        charge_sums = [sums['charge'] for sums in daily_sums.values()]
        discharge_sums = [sums['discharge'] for sums in daily_sums.values()]
        soc_sums = [sums['soc'] for sums in daily_sums.values()]
        grid_injection_sums = [sums['grid_injection'] for sums in daily_sums.values()]
        grid_offtake_sums = [sums['grid_offtake'] for sums in daily_sums.values()]
        ev_charge_sums = [sums['ev_charge'] for sums in daily_sums.values()]
        time_values = list(daily_sums.keys())
        line_width = 0.7
        title = "Not Optimized - Weekly Data For 2023"
        
        soc_sums = [x /(7*24) for x in soc_sums]
        
    return {
        "time_values": time_values,
        "pv_power_values": pv_power_sums,
        "power_usage_values": power_usage_sums,
        "charge_values": charge_sums,
        "discharge_values": discharge_sums,
        "soc_values": soc_sums,
        "injection_values": grid_injection_sums,
        "offtake_values": grid_offtake_sums,
        "grid_injection_prices": prices_injection,
        "grid_offtake_prices": prices_offtake,
        "grid_injection_sum": round(grid_injection_sum, 4),
        "grid_offtake_sum": round(grid_offtake_sum, 4),
        "grid_injection_cost": round(grid_injection_costs_total, 4),
        "grid_offtake_cost": round(grid_offtake_costs_total, 4),
        "ev_charge_values": ev_charge_sums,
        "line_width": line_width,
        "title": title
        }


def scale_list(original_list, new_length):
    scaled_list = []
    old_length = len(original_list)
    for i in range(new_length):
        # Calculate the corresponding index in the original list
        index = (i / (new_length - 1)) * (old_length - 1)
        # Calculate the integer and fractional parts of the index
        index_int = int(index)
        index_frac = index - index_int
        # Interpolate the value
        if index_int == old_length - 1:
            scaled_value = original_list[index_int]  # If it's the last element, take it directly
        else:
            scaled_value = (1 - index_frac) * original_list[index_int] + index_frac * original_list[index_int + 1]
        scaled_list.append(scaled_value)
    return scaled_list

    
