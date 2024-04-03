# todo
# add the solcast api and try showing wheater
# add the fluvius live prices and try to show it
# Peukert's law or the coulombic efficiency model bekijken
#

from collections import defaultdict
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from battery import Battery
from pybammBattery import PyBaMM_Battery
from APISolcast import get_solar_data
import csv
import matplotlib.dates as mdates
import datetime


def process_data(data_points, battery, pybamm_battery):
    for i in range(len(data_points) - 1):
        current_point = data_points[i]
        next_point = data_points[i + 1]

        pv_power_value = current_point.get("pv_power_value", 0)
        power_usage_value = current_point.get("power_usage_value")
        time_value = current_point.get("time_value")
        next_time = next_point.get("time_value")

        if time_value and next_time:
            # Calculate time difference in hours
            time_difference_hours = (next_time - time_value).total_seconds() / 3600
            # Charge the battery based on the time difference
            # print(time_difference_hours)

            charge_discharge_battery = pv_power_value - power_usage_value
            # print(charge_discharge_battery)

            current_point["soc_value"] = battery.soc

            if charge_discharge_battery > 0:
                charged, residue_to_much_energy = battery.charge(
                    charge_discharge_battery, time_difference_hours
                )
                current_point["grid_injection"] = residue_to_much_energy
                current_point["grid_extraction"] = 0
                current_point["charge_value"] = charged
                current_point["discharge_value"] = 0

            elif charge_discharge_battery < 0:
                discharged, residue_to_little_energy = battery.discharge(
                    abs(charge_discharge_battery), time_difference_hours
                )
                current_point["grid_injection"] = 0
                current_point["grid_extraction"] = residue_to_little_energy
                current_point["charge_value"] = 0
                current_point["discharge_value"] = discharged

            else:
                current_point["grid_injection"] = 0
                current_point["grid_extraction"] = 0
                current_point["charge_value"] = 0
                current_point["discharge_value"] = 0

            # pybamm_battery.charge(pv_power_value, time_difference_hours)
            # pybamm_battery.discharge(power_usage_value, time_difference_hours)

            # Add charge value to the data_point dictionary

    return data_points


def get_power_usage_values(data_points):
    try:
        with open("sampleData/power_usage_data_year.csv", "r") as file:
            sample_data = file.read()

            if sample_data:
                # Parse CSV data into list of dictionaries
                reader = csv.DictReader(sample_data.splitlines())
                samples_list = list(reader)

            for i in range(len(data_points) - 1):
                data_points[i]["power_usage_value"] = float(samples_list[i]["Power"])

        return data_points

    except Exception as e:
        print(f"Error reading sample data: {e}")
        return None


def calculate_values(data_points, scale):

    if scale == "DAY":
        # Filter data points for the first day
        first_day_data_points = [
            point
            for point in data_points
            if point["time_value"].date() == datetime.date(2023, 1, 1)
        ]  # Modify the date accordingly
        data_points = first_day_data_points

        # Perform some calculations to get new data
        time_values = [point["time_value"] for point in data_points]
        pv_power_values = [point["pv_power_value"] for point in data_points]
        power_usage_values = [-point["power_usage_value"] for point in data_points]
        charge_values = [-point["charge_value"] for point in data_points]
        discharge_values = [point["discharge_value"] for point in data_points]
        soc_values = [point["soc_value"] for point in data_points]
        grid_injection_values = [-point["grid_injection"] for point in data_points]
        grid_extraction_values = [point["grid_extraction"] for point in data_points]
        prices_injection = [point["price_injection"] for point in data_points]
        prices_extraction = [point["price_extraction"] for point in data_points]

        
        # Calculate cost for grid injection and grid extraction
        grid_injection_costs = [x * y / 1000 for x, y in zip(grid_injection_values, prices_injection)]
        grid_extraction_costs = [x * y / 1000 for x, y in zip(grid_extraction_values, prices_extraction)]

        # Calculate sum of costs
        grid_injection_costs_total = sum(grid_injection_costs)
        grid_extraction_costs_total = sum(grid_extraction_costs)
        
        grid_injection_sum = sum(grid_injection_values)
        grid_extraction_sum = sum(grid_extraction_values)
        
        return {
        "time_values": time_values,
        "pv_power_values": pv_power_values,
        "power_usage_values": power_usage_values,
        "charge_values": charge_values,
        "discharge_values": discharge_values,
        "soc_values": soc_values,
        "injection_values": grid_injection_values,
        "extraction_values": grid_extraction_values,
        "grid_injection_prices": prices_injection,
        "grid_extraction_prices": prices_extraction,
        "grid_injection_sum": round(grid_injection_sum, 4),
        "grid_extraction_sum": round(grid_extraction_sum, 4),
        "grid_injection_cost": round(grid_injection_costs_total, 4),
        "grid_extraction_cost": round(grid_extraction_costs_total, 4),
        }

    if scale == "MONTH":
         # Filter data points for the first month
        first_month_data_points = [
            point
            for point in data_points
            if point["time_value"].date().month == 1
        ]  # Modify the date accordingly
        data_points = first_month_data_points
        
        # Assuming time_values contains datetime objects
        # If time_values contains strings, convert them to datetime objects first
        time_values = [point["time_value"] for point in data_points]
        pv_power_values = [point["pv_power_value"] for point in data_points]
        power_usage_values = [-point["power_usage_value"] for point in data_points]
        charge_values = [-point["charge_value"] for point in data_points]
        discharge_values = [point["discharge_value"] for point in data_points]
        soc_values = [point["soc_value"] for point in data_points]
        grid_injection_values = [-point["grid_injection"] for point in data_points]
        grid_extraction_values = [point["grid_extraction"] for point in data_points]
        prices_injection = [point["price_injection"] for point in data_points]
        prices_extraction = [point["price_extraction"] for point in data_points]
        
        # Calculate cost for grid injection and grid extraction
        grid_injection_costs = [x * y / 1000 for x, y in zip(grid_injection_values, prices_injection)]
        grid_extraction_costs = [x * y / 1000 for x, y in zip(grid_extraction_values, prices_extraction)]

        # Calculate sum of costs
        grid_injection_costs_total = sum(grid_injection_costs)
        grid_extraction_costs_total = sum(grid_extraction_costs)
        
        grid_injection_sum = sum(grid_injection_values)
        grid_extraction_sum = sum(grid_extraction_values)

        # Create a defaultdict to store sums for each day
        daily_sums = defaultdict(lambda: defaultdict(float))

        # Iterate over the data_points and accumulate sums for each day
        for time_value, pv_power, power_usage, charge, discharge, soc, grid_injection, grid_extraction in zip(
            time_values, pv_power_values, power_usage_values, charge_values, discharge_values, soc_values, grid_injection_values, grid_extraction_values
        ):
            # Extract day from the datetime object
            day = time_value.date()
            
            # Accumulate sums for each column for the corresponding day
            daily_sums[day]['pv_power'] += pv_power
            daily_sums[day]['power_usage'] += power_usage
            daily_sums[day]['charge'] += charge
            daily_sums[day]['discharge'] += discharge
            daily_sums[day]['soc'] += soc
            daily_sums[day]['grid_injection'] += grid_injection
            daily_sums[day]['grid_extraction'] += grid_extraction

        pv_power_sums = [sums['pv_power'] for sums in daily_sums.values()]
        power_usage_sums = [sums['power_usage'] for sums in daily_sums.values()]
        charge_sums = [sums['charge'] for sums in daily_sums.values()]
        discharge_sums = [sums['discharge'] for sums in daily_sums.values()]
        soc_sums = [sums['soc'] for sums in daily_sums.values()]
        grid_injection_sums = [sums['grid_injection'] for sums in daily_sums.values()]
        grid_extraction_sums = [sums['grid_extraction'] for sums in daily_sums.values()]
        unique_dates = list(daily_sums.keys())
        
        return {
        "time_values": unique_dates,
        "pv_power_values": pv_power_sums,
        "power_usage_values": power_usage_sums,
        "charge_values": charge_sums,
        "discharge_values": discharge_sums,
        "soc_values": soc_sums,
        "injection_values": grid_injection_sums,
        "extraction_values": grid_extraction_sums,
        "grid_injection_prices": prices_injection,
        "grid_extraction_prices": prices_extraction,
        "grid_injection_sum": round(grid_injection_sum, 4),
        "grid_extraction_sum": round(grid_extraction_sum, 4),
        "grid_injection_cost": round(grid_injection_costs_total, 4),
        "grid_extraction_cost": round(grid_extraction_costs_total, 4),
        }
        
    if scale == "YEAR":
        # Assuming time_values contains datetime objects
        # If time_values contains strings, convert them to datetime objects first
        time_values = [point["time_value"] for point in data_points]
        pv_power_values = [point["pv_power_value"] for point in data_points]
        power_usage_values = [-point["power_usage_value"] for point in data_points]
        charge_values = [-point["charge_value"] for point in data_points]
        discharge_values = [point["discharge_value"] for point in data_points]
        soc_values = [point["soc_value"] for point in data_points]
        grid_injection_values = [-point["grid_injection"] for point in data_points]
        grid_extraction_values = [point["grid_extraction"] for point in data_points]
        prices_injection = [point["price_injection"] for point in data_points]
        prices_extraction = [point["price_extraction"] for point in data_points]
        
        # Calculate cost for grid injection and grid extraction
        grid_injection_costs = [x * y / 1000 for x, y in zip(grid_injection_values, prices_injection)]
        grid_extraction_costs = [x * y / 1000 for x, y in zip(grid_extraction_values, prices_extraction)]

        # Calculate sum of costs
        grid_injection_costs_total = sum(grid_injection_costs)
        grid_extraction_costs_total = sum(grid_extraction_costs)
        
        grid_injection_sum = sum(grid_injection_values)
        grid_extraction_sum = sum(grid_extraction_values)

        # Create a defaultdict to store sums for each day
        daily_sums = defaultdict(lambda: defaultdict(float))

        # Iterate over the data_points and accumulate sums for each day
        for time_value, pv_power, power_usage, charge, discharge, soc, grid_injection, grid_extraction in zip(
            time_values, pv_power_values, power_usage_values, charge_values, discharge_values, soc_values, grid_injection_values, grid_extraction_values
        ):
            # Extract day from the datetime object
            day = time_value.date()
            
            # Accumulate sums for each column for the corresponding day
            daily_sums[day]['pv_power'] += pv_power
            daily_sums[day]['power_usage'] += power_usage
            daily_sums[day]['charge'] += charge
            daily_sums[day]['discharge'] += discharge
            daily_sums[day]['soc'] += soc
            daily_sums[day]['grid_injection'] += grid_injection
            daily_sums[day]['grid_extraction'] += grid_extraction

        pv_power_sums = [sums['pv_power'] for sums in daily_sums.values()]
        power_usage_sums = [sums['power_usage'] for sums in daily_sums.values()]
        charge_sums = [sums['charge'] for sums in daily_sums.values()]
        discharge_sums = [sums['discharge'] for sums in daily_sums.values()]
        soc_sums = [sums['soc'] for sums in daily_sums.values()]
        grid_injection_sums = [sums['grid_injection'] for sums in daily_sums.values()]
        grid_extraction_sums = [sums['grid_extraction'] for sums in daily_sums.values()]
        unique_dates = list(daily_sums.keys())
        
        return {
        "time_values": unique_dates,
        "pv_power_values": pv_power_sums,
        "power_usage_values": power_usage_sums,
        "charge_values": charge_sums,
        "discharge_values": discharge_sums,
        "soc_values": soc_sums,
        "injection_values": grid_injection_sums,
        "extraction_values": grid_extraction_sums,
        "grid_injection_prices": prices_injection,
        "grid_extraction_prices": prices_extraction,
        "grid_injection_sum": round(grid_injection_sum, 4),
        "grid_extraction_sum": round(grid_extraction_sum, 4),
        "grid_injection_cost": round(grid_injection_costs_total, 4),
        "grid_extraction_cost": round(grid_extraction_costs_total, 4),
        }



    
