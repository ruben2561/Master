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
            data_points.append({'pv_power_value': pv_estimate, 'time_value': period_end, 'soc_value': 0, 'charge_value': 0, 'grid_usage': 0, 'power_usage_value': 0})

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

            if charge_discharge_battery > 0:
                charged, residue_to_much_energy = battery.charge(charge_discharge_battery, time_difference_hours)
                current_point['grid_usage'] = residue_to_much_energy * -1
                current_point['charge_value'] = charged
                    
            elif charge_discharge_battery < 0: 
                discharged, residue_to_little_energy = battery.discharge(abs(charge_discharge_battery), time_difference_hours)
                current_point['grid_usage'] = residue_to_little_energy
                current_point['charge_value'] = discharged * -1

            
            else:
                current_point['grid_usage'] = 0
            
            #pybamm_battery.charge(pv_power_value, time_difference_hours)
            #pybamm_battery.discharge(power_usage_value, time_difference_hours)

            # Add charge value to the data_point dictionary
            current_point['soc_value'] = battery.soc

    ######
    ######
    #pybamm_battery.simulation()
    ######  
    ######


    return data_points

def get_power_usage_values(data_points):
    try:
        with open("sampleData/power_usage_data_day.csv", "r") as file:
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
    
    

