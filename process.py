from collections import defaultdict
import copy
import importlib
import random
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from battery import Battery
import csv
import matplotlib.dates as mdates
import datetime
from datetime import datetime


def process_data_points(algorithm_name, data_points, battery, ev_battery, ev_total_distance):
    #algorithm_name = algorithm_name + ".py"
    algorithm_name = algorithm_name.replace(" ", "_")

    # Construct the module name based on the provided algorithm name
    module_name = f"algorithms.{algorithm_name}"
    
    # Dynamically import the module
    module = importlib.import_module(module_name)
    
    # Run the process function from the imported module
    return module.process_data(data_points, battery, ev_battery, ev_total_distance)
    

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
                number = random.choice([1,1,1,1,1,1,2,2,3])
                if number == 1: data_points[i]["power_usage_value"] = float(samples_list[i]["Power"]) + float(samples_list[i]["Power"]) * random.uniform(-0.1, 0.1)
                if number == 2: data_points[i]["power_usage_value"] = float(samples_list[i]["Power"]) + float(samples_list[i]["Power"]) * random.uniform(-0.3, 0.3)
                if number == 3: data_points[i]["power_usage_value"] = float(samples_list[i]["Power"]) + float(samples_list[i]["Power"]) * random.uniform(-0.7, 0.7)
            

        return data_points

    except Exception as e:
        print(f"Error reading sample data power usage: {e}")
        return None
    
def get_ev_charge_values(data_points, ev_distance_year, ev_number_of_cars):
    car_charge_day = (((ev_distance_year * ev_number_of_cars) / 100) * 15) / 365  #average car uses 15kWh/100km
    for i in range(len(data_points) - 1):
        if data_points[i]["time_value"].hour == 12 and data_points[i]["time_value"].minute == 0 and ev_number_of_cars != 0:
            number = random.choice([1,1,1,1,1,2,2,3])
            if number == 1: data_points[i]["ev_charge_value"] = car_charge_day + car_charge_day * random.uniform(-0.1, 0.1)
            if number == 2: data_points[i]["ev_charge_value"] = car_charge_day + car_charge_day * random.uniform(-0.4, 0.4)
            if number == 3: data_points[i]["ev_charge_value"] = car_charge_day + car_charge_day * random.uniform(-1, 1)
            
    return data_points


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
        heat_pump_sums = [-point["heat_pump_value"] for point in data_points]
        
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
        heat_pump_values = [-point["heat_pump_value"] for point in data_points]
        
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
        for time_value, pv_power, power_usage, charge, discharge, grid_injection, grid_offtake, ev_charge, heat_pump in zip(
            time_values, pv_power_values, power_usage_values, charge_values, discharge_values, grid_injection_values, grid_offtake_values, ev_charge_values, heat_pump_values
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
            daily_sums[day]['heat_pump'] += heat_pump

        pv_power_sums = [sums['pv_power'] for sums in daily_sums.values()]
        power_usage_sums = [sums['power_usage'] for sums in daily_sums.values()]
        charge_sums = [sums['charge'] for sums in daily_sums.values()]
        discharge_sums = [sums['discharge'] for sums in daily_sums.values()]
        grid_injection_sums = [sums['grid_injection'] for sums in daily_sums.values()]
        grid_offtake_sums = [sums['grid_offtake'] for sums in daily_sums.values()]
        ev_charge_sums = [sums['ev_charge'] for sums in daily_sums.values()]
        heat_pump_sums = [sums['heat_pump'] for sums in daily_sums.values()]
        
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
        heat_pump_values = [-point["heat_pump_value"] for point in data_points]
        
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
        for time_value, pv_power, power_usage, charge, discharge, grid_injection, grid_offtake, ev_charge, heat_pump in zip(
            time_values, pv_power_values, power_usage_values, charge_values, discharge_values, grid_injection_values, grid_offtake_values, ev_charge_values, heat_pump_values
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
            daily_sums[day]['heat_pump'] += heat_pump

        pv_power_sums = [sums['pv_power'] for sums in daily_sums.values()]
        power_usage_sums = [sums['power_usage'] for sums in daily_sums.values()]
        charge_sums = [sums['charge'] for sums in daily_sums.values()]
        discharge_sums = [sums['discharge'] for sums in daily_sums.values()]
        grid_injection_sums = [sums['grid_injection'] for sums in daily_sums.values()]
        grid_offtake_sums = [sums['grid_offtake'] for sums in daily_sums.values()]
        ev_charge_sums = [sums['ev_charge'] for sums in daily_sums.values()]
        heat_pump_sums = [sums['heat_pump'] for sums in daily_sums.values()]
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
        heat_pump_values = [-point["heat_pump_value"] for point in data_points]
        
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
        for time_value, pv_power, power_usage, charge, discharge, soc, grid_injection, grid_offtake, ev_charge, heat_pump in zip(
            time_values, pv_power_values, power_usage_values, charge_values, discharge_values, soc_values, grid_injection_values, grid_offtake_values, ev_charge_values, heat_pump_values
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
            daily_sums[year_year]['heat_pump'] += heat_pump

        pv_power_sums = [sums['pv_power'] for sums in daily_sums.values()]
        power_usage_sums = [sums['power_usage'] for sums in daily_sums.values()]
        charge_sums = [sums['charge'] for sums in daily_sums.values()]
        discharge_sums = [sums['discharge'] for sums in daily_sums.values()]
        soc_sums = [sums['soc'] for sums in daily_sums.values()]
        grid_injection_sums = [sums['grid_injection'] for sums in daily_sums.values()]
        grid_offtake_sums = [sums['grid_offtake'] for sums in daily_sums.values()]
        ev_charge_sums = [sums['ev_charge'] for sums in daily_sums.values()]
        heat_pump_sums = [sums['heat_pump'] for sums in daily_sums.values()]
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
        heat_pump_values = [-point["heat_pump_value"] for point in data_points]
        
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
        for time_value, pv_power, power_usage, charge, discharge, soc, grid_injection, grid_offtake, ev_charge, heat_pump in zip(
            time_values, pv_power_values, power_usage_values, charge_values, discharge_values, soc_values, grid_injection_values, grid_offtake_values, ev_charge_values, heat_pump_values
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
            daily_sums[year_month]['heat_pump'] += heat_pump

        pv_power_sums = [sums['pv_power'] for sums in daily_sums.values()]
        power_usage_sums = [sums['power_usage'] for sums in daily_sums.values()]
        charge_sums = [sums['charge'] for sums in daily_sums.values()]
        discharge_sums = [sums['discharge'] for sums in daily_sums.values()]
        soc_sums = [sums['soc'] for sums in daily_sums.values()]
        grid_injection_sums = [sums['grid_injection'] for sums in daily_sums.values()]
        grid_offtake_sums = [sums['grid_offtake'] for sums in daily_sums.values()]
        ev_charge_sums = [sums['ev_charge'] for sums in daily_sums.values()]
        heat_pump_sums = [sums['heat_pump'] for sums in daily_sums.values()]
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
        heat_pump_values = [-point["heat_pump_value"] for point in data_points]
        
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
        for time_value, pv_power, power_usage, charge, discharge, soc, grid_injection, grid_offtake, ev_charge, heat_pump in zip(
            time_values, pv_power_values, power_usage_values, charge_values, discharge_values, soc_values, grid_injection_values, grid_offtake_values, ev_charge_values, heat_pump_values
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
            daily_sums[year_week]['heat_pump'] += heat_pump

        pv_power_sums = [sums['pv_power'] for sums in daily_sums.values()]
        power_usage_sums = [sums['power_usage'] for sums in daily_sums.values()]
        charge_sums = [sums['charge'] for sums in daily_sums.values()]
        discharge_sums = [sums['discharge'] for sums in daily_sums.values()]
        soc_sums = [sums['soc'] for sums in daily_sums.values()]
        grid_injection_sums = [sums['grid_injection'] for sums in daily_sums.values()]
        grid_offtake_sums = [sums['grid_offtake'] for sums in daily_sums.values()]
        ev_charge_sums = [sums['ev_charge'] for sums in daily_sums.values()]
        heat_pump_sums = [sums['heat_pump'] for sums in daily_sums.values()]
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
        "heat_pump_values": heat_pump_sums,
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

    
