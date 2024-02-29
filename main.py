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

def retrieve_data():
    forecast_data = get_solar_radiation_forecast("radiation", 5)
    return forecast_data

def process_data(forecast_data):
    if forecast_data:
        print("Solar Radiation Data:")
        print(forecast_data)
        # Parse CSV data into list of dictionaries
        reader = csv.DictReader(forecast_data.splitlines())
        forecast_list = list(reader)
        # Initialize battery
        battery = Battery(capacity=13, charge_power=5.0, discharge_power=5.0, max_soc=0.9, min_dod=0.1, efficienty=0.95)
        # Initialize lists to store data for plotting
        charge_values = []
        time_values = []
        # Iterate over the forecast data
        for data_point in forecast_list:
            pv_estimate = float(data_point['PvEstimate'])
            period_end = data_point['PeriodEnd']
            print(f"Pv Estimate: {pv_estimate}, Period End: {period_end}")
            
            # Convert period to hours
            period_hours = 0.5  # Assuming each period is 0.5 hours
            
            # Charge the battery
            battery.charge(pv_estimate, period_hours)
            print(f"Battery charge after charging: {battery.soc} kWh")
            
            # Store battery charge and time for plotting
            charge_values.append(battery.soc)
            time_values.append(period_end)

        return time_values, charge_values
    else:
        print("Failed to retrieve solar radiation forecast.")
        return [], []
    
def calculate_new_values(time_values, charge_values, daily_average_usage):
    new_charge_values = []
    for charge_value in charge_values:
        # Subtract daily average power usage from solar power values
        new_charge_value = max(0, charge_value - daily_average_usage/48) #because time windows are 30 min
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
