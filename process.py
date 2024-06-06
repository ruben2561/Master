import copy
import csv
import datetime
import importlib
import matplotlib.dates as mdates
import random
import tkinter as tk
from collections import defaultdict
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk

from battery import Battery


def process_data_points(algorithm_name, data_points, battery, ev_battery, ev_total_distance, OPEX, temp_desired):
    # algorithm_name = algorithm_name + ".py"
    algorithm_name = algorithm_name.replace(" ", "_")

    # Construct the module name based on the provided algorithm name
    module_name = f"algorithms.{algorithm_name}"

    # Dynamically import the module
    module = importlib.import_module(module_name)

    # Run the process function from the imported module
    return module.process_data(data_points, battery, ev_battery, ev_total_distance, OPEX, temp_desired)


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
                number = random.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3])
                if number == 1: data_points[i]["power_usage_value"] = float(samples_list[i]["Power"]) + float(
                    samples_list[i]["Power"]) * random.uniform(-0.1, 0.1)
                if number == 2: data_points[i]["power_usage_value"] = float(samples_list[i]["Power"]) + float(
                    samples_list[i]["Power"]) * random.uniform(-0.3, 0.3)
                if number == 3: data_points[i]["power_usage_value"] = float(samples_list[i]["Power"]) + float(
                    samples_list[i]["Power"]) * random.uniform(-0.5, 0.5)
                else: data_points[i]["power_usage_value"] = float(samples_list[i]["Power"])

        return data_points

    except Exception as e:
        print(f"Error reading sample data power usage: {e}")
        return None


def get_ev_charge_values(data_points, ev_distance_year, ev_number_of_cars):
    car_charge_day = (((ev_distance_year * ev_number_of_cars) / 100) * 15) / 365  # average car uses 15kWh/100km
    for i in range(len(data_points) - 1):
        if data_points[i]["time_value"].hour == 12 and data_points[i][
            "time_value"].minute == 0 and ev_number_of_cars != 0:
            number = random.choice([1, 1, 1, 1, 1, 2, 2, 3])
            if number == 1: data_points[i]["ev_charge_value"] = car_charge_day + car_charge_day * random.uniform(-0.1,
                                                                                                                 0.1)
            if number == 2: data_points[i]["ev_charge_value"] = car_charge_day + car_charge_day * random.uniform(-0.4,
                                                                                                                 0.4)
            if number == 3: data_points[i]["ev_charge_value"] = car_charge_day + car_charge_day * random.uniform(-1, 1)

    return data_points


def calculate_values(data_points, specific_time, scale):
    if scale == "SPECIFIC DAY":
        day, month = specific_time.split("-")
        data_points = [point for point in data_points if
                       point["time_value"].day == int(day) and point["time_value"].strftime("%B") == month]

    elif scale == "SPECIFIC WEEK":

        # Dictionary mapping month names to numerical values
        month_to_num = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7,
            "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}

        # Split the date string into day and month
        day, month_name = specific_time.split("-")

        month_num = month_to_num[month_name]
        date_obj = datetime.strptime(f"2024-{month_num}-{day}", "%Y-%m-%d")
        week_number = date_obj.isocalendar()[1]

        # Filter data points for the first month
        month_data_points = [point for point in data_points if
            (point["time_value"].month, point["time_value"].day) == (1, 1) and 1 == int(week_number) or (
            point["time_value"].month, point["time_value"].day) != (1, 1) and point["time_value"].isocalendar()[
                1] == int(week_number)]  # Modify the date accordingly
        data_points = month_data_points

    elif scale == "SPECIFIC MONTH":
        month_data_points = [point for point in data_points if
            point["time_value"].strftime("%B") == specific_time.split("-")[1]]  # Modify the date accordingly
        data_points = month_data_points

    elif scale == "PER YEAR":
        data_points = data_points

    elif scale == "PER MONTH":
        data_points = data_points

    elif scale == "PER WEEK":
        data_points = data_points

    # Extract and process the data
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
    price_battery_use = [point["price_battery_use"] for point in data_points]

    # Calculate costs
    grid_injection_costs = [x * y / 1000 for x, y in zip(grid_injection_values, prices_injection)]
    grid_offtake_costs = [x * y / 1000 for x, y in zip(grid_offtake_values, prices_offtake)]
    grid_injection_costs_total = sum(grid_injection_costs)
    grid_offtake_costs_total = sum(grid_offtake_costs)
    grid_injection_sum = sum(grid_injection_values)
    grid_offtake_sum = sum(grid_offtake_values)
    battery_use_cost_total = sum(price_battery_use)

    # Create a defaultdict to store sums based on the time scale
    sums = defaultdict(lambda: defaultdict(float))

    if scale == "SPECIFIC WEEK" or scale == "PER WEEK" or scale == "SPECIFIC MONTH" or scale == "PER MONTH" or scale == "PER YEAR":
        for time_value, pv_power, power_usage, charge, discharge, soc, grid_injection, grid_offtake, ev_charge, heat_pump in zip(
                time_values, pv_power_values, power_usage_values, charge_values, discharge_values, soc_values,
                grid_injection_values, grid_offtake_values, ev_charge_values, heat_pump_values):
            if scale == "SPECIFIC WEEK" or scale == "SPECIFIC MONTH":
                key = time_value.date()
            elif scale == "PER YEAR":
                key = time_value.year
            elif scale == "PER WEEK":
                key = time_value.isocalendar()[1]
                if time_value.month == 1 and time_value.day == 1:
                    key = 1
            elif scale == "PER MONTH":
                key = time_value.month

            sums[key]['pv_power'] += pv_power
            sums[key]['power_usage'] += power_usage
            sums[key]['charge'] += charge
            sums[key]['discharge'] += discharge
            sums[key]['soc'] += soc
            sums[key]['grid_injection'] += grid_injection
            sums[key]['grid_offtake'] += grid_offtake
            sums[key]['ev_charge'] += ev_charge
            sums[key]['heat_pump'] += heat_pump

            pv_power_sums = [sums[key]['pv_power'] for key in sorted(sums.keys())]
            power_usage_sums = [sums[key]['power_usage'] for key in sorted(sums.keys())]
            charge_sums = [sums[key]['charge'] for key in sorted(sums.keys())]
            discharge_sums = [sums[key]['discharge'] for key in sorted(sums.keys())]
            soc_sums = [sums[key]['soc'] for key in sorted(sums.keys())]
            grid_injection_sums = [sums[key]['grid_injection'] for key in sorted(sums.keys())]
            grid_offtake_sums = [sums[key]['grid_offtake'] for key in sorted(sums.keys())]
            ev_charge_sums = [sums[key]['ev_charge'] for key in sorted(sums.keys())]
            heat_pump_sums = [sums[key]['heat_pump'] for key in sorted(sums.keys())]
            time_values = sorted(sums.keys())

    else:
        pv_power_sums = pv_power_values
        power_usage_sums = power_usage_values
        charge_sums = charge_values
        discharge_sums = discharge_values
        soc_sums = soc_values
        grid_injection_sums = grid_injection_values
        grid_offtake_sums = grid_offtake_values
        ev_charge_sums = ev_charge_values
        heat_pump_sums = heat_pump_values
        time_values = time_values

    # Adjust titles and line widths based on the scale
    if scale == "SPECIFIC DAY":
        line_width = 0.04
        title = f"Not Optimized - Hourly Data For Date {specific_time} In 2023"
    elif scale == "SPECIFIC WEEK":
        line_width = 0.95
        title = f"Not Optimized - Daily Data For Week {specific_time.split('-')[0]} In 2023"
    elif scale == "SPECIFIC MONTH":
        line_width = 0.9
        title = f"Not Optimized - Daily Data For Month {specific_time} In 2023"
    elif scale == "PER YEAR":
        line_width = 2
        title = "Not Optimized - Yearly Data For 2023"
    elif scale == "PER MONTH":
        line_width = 0.9
        title = "Not Optimized - Monthly Data For 2023"
    elif scale == "PER WEEK":
        line_width = 0.7
        title = "Not Optimized - Weekly Data For 2023"

    return {"time_values": time_values, "pv_power_values": pv_power_sums, "power_usage_values": power_usage_sums,
        "charge_values": charge_sums, "discharge_values": discharge_sums, "soc_values": soc_sums,
        "injection_values": grid_injection_sums, "offtake_values": grid_offtake_sums,
        "grid_injection_prices": prices_injection, "grid_offtake_prices": prices_offtake,
        "grid_injection_sum": round(grid_injection_sum, 4), "grid_offtake_sum": round(grid_offtake_sum, 4),
        "grid_injection_cost": round(grid_injection_costs_total, 4),
        "grid_offtake_cost": round(grid_offtake_costs_total, 4), "battery_use_cost": round(battery_use_cost_total, 4),
        "ev_charge_values": ev_charge_sums, "heat_pump_values": heat_pump_sums, "line_width": line_width,
        "title": title}


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
