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
        print("Solar Radiation Data:")
        #print(forecast_data)
        # Parse CSV data into list of dictionaries
        reader = csv.DictReader(forecast_data.splitlines())
        forecast_list = list(reader)
        
        # Initialize list to store data for plotting as tuples of (power_value, time_value)
        data_points = []

        # Iterate over the forecast data
        for data_point in forecast_list:
            pv_estimate = float(data_point['PvEstimate'])
            #print(data_point["PeriodEnd"])
            period_end = datetime.datetime.strptime(data_point['PeriodEnd'], "%Y-%m-%dT%H:%M:%SZ")  # Convert string to datetime
            #print(f"Pv Estimate: {pv_estimate}, Period End: {period_end}")
            
            # Store data point as a dictionary
            data_points.append({'power_value': pv_estimate, 'time_value': period_end, 'charge_value': 0, 'residue_energy': 0})

    return data_points

def process_data(data_points, power_usage, battery, pybamm_battery):
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
            
            pybamm_battery.charge(power_value, time_difference_hours)
            pybamm_battery.discharge(power_usage/48, 0.5)

            #print(f"Battery charge after charging: {battery.soc} kWh")

            # Add charge value to the data_point dictionary
            current_point['charge_value'] = battery.soc
            current_point['residue_energy'] = (residue_to_much_energy - residue_to_little_energy)

    ######
    ######
    #pybamm_battery.simulation()
    ######  
    ######


    return data_points
    
def calculate_new_values(time_values, charge_values, power_usage):
    new_charge_values = []
    for charge_value in charge_values:
        #print(charge_value)
        # Subtract daily average power usage from solar power values
        new_charge_value = max(0, charge_value - power_usage/48) #because time windows are 30 min
        new_charge_values.append(new_charge_value)
    return time_values, new_charge_values

def update_gui(fig, ax1, ax2, ax3, ax4, data_points, daily_average_usage, grid_injection, grid_extraction):
    # Extract values for plotting

    #print(data_points)
    time_values = [point['time_value'] for point in data_points]# if point['time_value']]
    power_values = [point['power_value'] for point in data_points]
    charge_values = [point['charge_value'] for point in data_points]
    residue_energy_values = [point['residue_energy'] for point in data_points]# if 'residue_energy' in point]
    
    # Plot PV production on the first graph
    ax1.plot(time_values, power_values, color='lightgreen', label='PV Production')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('PV Production (kW)')
    ax1.set_title('PV Production')

    # Plot power usage throughout the day on the second graph
    ax2.plot(time_values, [daily_average_usage/48]*len(time_values), color='lightgreen', label='Power Usage')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Power (kW)')
    ax2.set_title('Home Power Usage')

    # Plot battery charge on the third graph
    ax3.clear()
    ax3.plot(time_values, charge_values, color='lightgreen', marker='o', linestyle='-')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Charge (kWh)')
    ax3.set_title(f'Battery Charge (Start: {time_values[0].strftime("%Y-%m-%d %H:%M")})')

    # Plot residue energy as a bar chart on the fourth graph
    ax4.clear()
    ax4.stem(time_values, residue_energy_values, label='Residue Energy', linefmt='lightgreen', markerfmt='lightgreen', basefmt=' ')
    ax4.set_xlabel('Time')
    ax4.set_ylabel('Energy (kWh)')
    ax4.set_title('Grid Usage')

    # Calculate sum of positive and negative residue values
    grid_injection_sum = sum(value for value in residue_energy_values if value > 0)
    grid_extraction_sum = sum(value for value in residue_energy_values if value < 0)

    # Calculate cost for grid injection and grid extraction assuming energy cost of 0.1 euro per kWh
    grid_injection_cost = grid_injection_sum * 0.035
    grid_extraction_cost = grid_extraction_sum * -0.1211

    # Update labels with sums
    grid_injection.config(text=f"Grid injection: {grid_injection_sum:.4f} kWh     Received Money: {grid_injection_cost:.4f} €")
    grid_extraction.config(text=f"Grid extraction: {(grid_extraction_sum*-1):.4f} kWh     Paid Money: {grid_extraction_cost:.4f} €")

    # Filter time values to display only every 6 hours
    filtered_time_values = [time_values[i] for i in range(len(time_values)) if i % 12 == 0]
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Format to display only hour and minute
    ax1.set_xticks(filtered_time_values)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Format to display only hour and minute
    ax2.set_xticks(filtered_time_values)
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Format to display only hour and minute
    ax3.set_xticks(filtered_time_values)
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Format to display only hour and minute
    ax4.set_xticks(filtered_time_values)

    fig.canvas.draw()

def start_process(fig, ax1, ax2, ax3, ax4, grid_injection, grid_extraction, latitude, longitude, start_date, end_date):
    battery = Battery(capacity=3, soc=2, charge_power=5.0, discharge_power=5.0, max_soc=0.95, min_dod=0.05, efficiency=0.90)
    pybamm_battery = PyBaMM_Battery(capacity=3, soc=2, charge_power=5.0, discharge_power=5.0, max_soc=0.95, min_dod=0.05, efficiency=0.90)
    
    daily_average_usage = 9  # kWh

    data_points = retrieve_data_api(latitude, longitude, start_date, end_date)

    data_points = process_data(data_points, daily_average_usage, battery, pybamm_battery)

    #time_values, new_charge_values = calculate_new_values(time_values, charge_values, daily_average_usage)

    #update_gui(fig, ax1, ax2, ax3, ax4, data_points, daily_average_usage, grid_injection, grid_extraction)

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

    latitude_label = tk.Label(left_frame, text="Latitude:")
    latitude_label.grid(row=1, column=0, padx=5, pady=5)
    latitude_entry = tk.Entry(left_frame)
    latitude_entry.grid(row=1, column=1, padx=5, pady=5)

    longitude_label = tk.Label(left_frame, text="Longitude:")
    longitude_label.grid(row=2, column=0, padx=5, pady=5)
    longitude_entry = tk.Entry(left_frame)
    longitude_entry.grid(row=2, column=1, padx=5, pady=5)

    start_date_label = tk.Label(left_frame, text="Start Date:")
    start_date_label.grid(row=3, column=0, padx=5, pady=5)
    start_date_entry = tk.Entry(left_frame)
    start_date_entry.grid(row=3, column=1, padx=5, pady=5)

    end_date_label = tk.Label(left_frame, text="End Date:")
    end_date_label.grid(row=4, column=0, padx=5, pady=5)
    end_date_entry = tk.Entry(left_frame)
    end_date_entry.grid(row=4, column=1, padx=5, pady=5)

    start_button = ttk.Button(left_frame, text="Start", command=lambda: start_process(fig, ax1, ax2, ax3, ax4, grid_injection, grid_extraction, latitude_entry.get(), longitude_entry.get(), start_date_entry.get(), end_date_entry.get()))
    start_button.grid(row=5, columnspan=2, pady=10)

    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    fig = Figure(figsize=(12, 6), dpi=100)

    # Add subplot 1
    ax1 = fig.add_subplot(221)  # 2 rows, 2 columns, subplot 1
    # Add subplot 2
    ax2 = fig.add_subplot(222)  # 2 rows, 2 columns, subplot 2
    # Add subplot 3
    ax3 = fig.add_subplot(223)  # 2 rows, 2 columns, subplot 3
    # Add subplot 4
    ax4 = fig.add_subplot(224)  # 2 rows, 2 columns, subplot 4

    # Adjust spacing between subplots
    fig.subplots_adjust(hspace=0.5, wspace=0.3)

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Add labels for battery charge, grid injection, and grid extraction on the right side of the graph
    battery_charge_label = tk.Label(right_frame, text="Battery Charge: ", font=("Arial", 10))
    battery_charge_label.pack(side=tk.TOP, padx=10, pady=5)
    grid_injection = tk.Label(right_frame, text="Grid injection: ", font=("Arial", 10))
    grid_injection.pack(side=tk.TOP, padx=10, pady=5)
    grid_extraction = tk.Label(right_frame, text="Grid extraction: ", font=("Arial", 10))
    grid_extraction.pack(side=tk.TOP, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
