#todo
#add the solcast api and try showing wheater
#add the fluvius live prices and try to show it
#Peukert's law or the coulombic efficiency model bekijken
#

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from battery import Battery 
from pybammBattery import PyBaMM_Battery
from solcast import get_solar_radiation_forecast
import csv
import matplotlib.dates as mdates
import datetime

def retrieve_data_api(latitude, longitude, start_date, end_date):
    forecast_data = get_solar_radiation_forecast(latitude, longitude, start_date, end_date)

    if forecast_data:
        # Parse CSV data into list of dictionaries
        reader = csv.DictReader(forecast_data.splitlines())
        forecast_list = list(reader)
        
        # Initialize list to store data for plotting as tuples of (pv_power_value, time_value)
        data_points = []

        # Iterate over the forecast data
        for data_point in forecast_list:
            pv_estimate = float(data_point['PvEstimate'])
            #print(data_point["PeriodEnd"])
            period_end = datetime.datetime.strptime(data_point['PeriodEnd'], "%Y-%m-%dT%H:%M:%SZ")  # Convert string to datetime
            #print(f"Pv Estimate: {pv_estimate}, Period End: {period_end}")
            
            # Store data point as a dictionary
            data_points.append({'pv_power_value': pv_estimate, 'time_value': period_end, 'soc_value': 0, 'charge_value': 0, 'discharge_value': 0, 'grid_injection': 0, 'grid_extraction': 0, 'power_usage_value': 0})

    return data_points

def process_data(data_points, battery, pybamm_battery):
    for i in range(len(data_points) - 1):
        current_point = data_points[i]
        next_point = data_points[i + 1]

        pv_power_value = current_point.get('pv_power_value', 0)
        power_usage_value = current_point.get('power_usage_value')
        time_value = current_point.get('time_value')
        next_time = next_point.get('time_value')

        if time_value and next_time:
            # Calculate time difference in hours
            time_difference_hours = (next_time - time_value).total_seconds() / 3600
            # Charge the battery based on the time difference
            #print(time_difference_hours)

            charge_discharge_battery = pv_power_value - power_usage_value
            #print(charge_discharge_battery)

            current_point['soc_value'] = battery.soc

            if charge_discharge_battery > 0:
                charged, residue_to_much_energy = battery.charge(charge_discharge_battery, time_difference_hours)
                current_point['grid_injection'] = residue_to_much_energy
                current_point['grid_extraction'] = 0
                current_point['charge_value'] = charged
                current_point['discharge_value'] = 0
                    
            elif charge_discharge_battery < 0: 
                discharged, residue_to_little_energy = battery.discharge(abs(charge_discharge_battery), time_difference_hours)
                current_point['grid_injection'] = 0
                current_point['grid_extraction'] = residue_to_little_energy
                current_point['charge_value'] = 0
                current_point['discharge_value'] = discharged

            
            else:
                current_point['grid_injection'] = 0
                current_point['grid_extraction'] = 0
                current_point['charge_value'] = 0
                current_point['discharge_value'] = 0
            
            #pybamm_battery.charge(pv_power_value, time_difference_hours)
            #pybamm_battery.discharge(power_usage_value, time_difference_hours)

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
                data_points[i]['power_usage_value'] = float(samples_list[i]['Power'])
        
        return data_points

    except Exception as e:
        print(f"Error reading sample dataaaa: {e}")
        return None
    
    

def calculate_values(data_points, scale):

    if scale == "DAY":
        # Filter data points for the first day
        first_day_data_points = [point for point in data_points if point['time_value'].date() == datetime.date(2023, 1, 1)]  # Modify the date accordingly
        data_points = first_day_data_points

        print(len(data_points))

        # Perform some calculations to get new data
        time_values = [point['time_value'] for point in data_points]
        pv_power_values = [point['pv_power_value'] for point in data_points]
        power_usage_values = [-point['power_usage_value'] for point in data_points]
        charge_values = [-point['charge_value'] for point in data_points]
        discharge_values = [point['discharge_value'] for point in data_points]
        soc_values = [point['soc_value'] for point in data_points]
        grid_injection_values = [-point['grid_injection'] for point in data_points]
        grid_extraction_values = [point['grid_extraction'] for point in data_points]

        # Calculate sum of positive and negative residue values
        grid_injection_sum = sum(grid_injection_values)
        grid_extraction_sum = sum(grid_extraction_values)

        # Calculate cost for grid injection and grid extraction assuming energy cost of 0.1 euro per kWh
        grid_injection_cost = grid_injection_sum * 0.035
        grid_extraction_cost = grid_extraction_sum * -0.1211





    return {
        'time_values': time_values,
        'pv_power_values': pv_power_values,
        'power_usage_values': power_usage_values,
        'charge_values': charge_values,
        'discharge_values': discharge_values,
        'soc_values': soc_values,
        'injection_values': grid_injection_values,
        'extraction_values': grid_extraction_values,
        'grid_injection_sum': round(grid_injection_sum, 4),
        'grid_extraction_sum': round(grid_extraction_sum, 4),
        'grid_injection_cost': round(grid_injection_cost, 4),
        'grid_extraction_cost': round(grid_extraction_cost, 4)
    }

