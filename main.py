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
from solcast import get_solar_radiation_forecast 
import csv
import matplotlib.dates as mdates
import datetime

def retrieve_data_api():
    forecast_data = get_solar_radiation_forecast("radiation", 5)

    if forecast_data:
        print("Solar Radiation Data:")
        print(forecast_data)
        # Parse CSV data into list of dictionaries
        reader = csv.DictReader(forecast_data.splitlines())
        forecast_list = list(reader)
        
        # Initialize list to store data for plotting as tuples of (power_value, time_value)
        data_points = []

        # Iterate over the forecast data
        for data_point in forecast_list:
            pv_estimate = float(data_point['PvEstimate'])
            print(data_point["PeriodEnd"])
            period_end = datetime.datetime.strptime(data_point['PeriodEnd'], "%Y-%m-%dT%H:%M:%SZ")  # Convert string to datetime
            print(f"Pv Estimate: {pv_estimate}, Period End: {period_end}")
            
            # Store data point as a dictionary
            data_points.append({'power_value': pv_estimate, 'time_value': period_end, 'charge_value': 0, 'residue_energy': 0})

    return data_points

def process_data(data_points, power_usage, battery):
    for i in range(len(data_points) - 1):
        current_point = data_points[i]
        next_point = data_points[i + 1]

        power_value = current_point.get('power_value', 0)
        time_value = current_point.get('time_value')
        next_time = next_point.get('time_value')

        if time_value and next_time:
            # Calculate time difference in hours
            time_difference_hours = (next_time - time_value).total_seconds() / 3600
            print(time_difference_hours)
            print(power_value)
            # Charge the battery based on the time difference
            residue_to_much_energy = battery.charge(power_value, time_difference_hours)
            residue_to_little_energy = battery.discharge_kWh(power_usage / 48)  # Subtract average power usage every half hour

            print(f"Battery charge after charging: {battery.soc} kWh")

            # Add charge value to the data_point dictionary
            current_point['charge_value'] = battery.soc
            current_point['residue_energy'] = (residue_to_much_energy - residue_to_little_energy)

    return data_points
    
def calculate_new_values(time_values, charge_values, power_usage):
    new_charge_values = []
    for charge_value in charge_values:
        print(charge_value)
        # Subtract daily average power usage from solar power values
        new_charge_value = max(0, charge_value - power_usage/48) #because time windows are 30 min
        new_charge_values.append(new_charge_value)
    return time_values, new_charge_values

def update_gui(fig, ax, time_values, charge_values):
    ax.clear()
    ax.plot(time_values, charge_values, marker='o', linestyle='-')
    ax.set_xlabel('Time')
    ax.set_ylabel('Battery Charge (kWh)')
    ax.set_title('Battery Charge Over Time')

     # Filter time values to display only every 6 hours
    filtered_time_values = [time_values[i] for i in range(len(time_values)) if i % 12 == 0]
    ax.set_xticks(filtered_time_values)

    fig.canvas.draw()

def start_process(fig, ax):
    forecast_data = retrieve_data()
    time_values, charge_values = process_data(forecast_data)
    # Calculate daily average power usage (example value)
    daily_average_usage = 7.5  # kWh
    time_values, new_charge_values = calculate_new_values(time_values, charge_values, daily_average_usage)
    update_gui(fig, ax, time_values, new_charge_values)

def create_gui():
    root = tk.Tk()
    root.title("Smart home Simulation")

    # Define custom style
    style = ttk.Style()
    style.theme_use('clam')  # Use 'clam' theme as base

    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10)

    title_label = tk.Label(left_frame, text="Smart Home Simulation", font=("Arial", 14))
    title_label.grid(row=0, columnspan=2, pady=10)

    start_button = ttk.Button(left_frame, text="Start", command=lambda: start_process(fig, ax))
    start_button.grid(row=1, columnspan=2, pady=10)

    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
