import tkinter
import tkinter.messagebox
from CTkMessagebox import CTkMessagebox
import customtkinter
from customtkinter import *
from matplotlib.figure import Figure
from CTkListbox import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

import pandas as pd
from battery import Battery
from databaseManager import DatabaseManager
from batteryManager import BatteryManager
from process import get_power_usage_values, process_data, retrieve_data_api
from pybammBattery import PyBaMM_Battery
from solcast import get_solar_radiation_forecast
import csv
import matplotlib.dates as mdates
import datetime
import numpy as np

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager("database_master.db")  # Create an instance of DatabaseManager


        # configure window
        self.title("Smart Home Simulation")
        #self.geometry(f"{1280}x{760}")

       # configure grid layout (2x3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        

        customtkinter.set_appearance_mode("Dark")

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=270, corner_radius=0, border_width=2)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(11, weight=1)
        self.sidebar_frame.grid_propagate(False)  # Prevent resizing

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Simulation Params", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(15, 20), columnspan=2)

        # Option Menu for Battery
        self.label_battery = customtkinter.CTkLabel(self.sidebar_frame, text="Battery", font=customtkinter.CTkFont(size=15))
        self.label_battery.grid(row=1, column=0, padx=5, pady=(5, 0))
        self.optionmenu_battery = customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False)
        self.optionmenu_battery.grid(row=2, column=0, padx=20, pady=(5, 5))
        self.edit_button_battery = customtkinter.CTkButton(self.sidebar_frame, width=60, text="Edit", command=self.edit_battery)
        self.edit_button_battery.grid(row=2, column=1, padx=5, pady=(5, 5))
        self.populate_battery_options()

        # Option Menu for SolarPanel
        self.label_solar_panel = customtkinter.CTkLabel(self.sidebar_frame, text="Solar Panel", font=customtkinter.CTkFont(size=15))
        self.label_solar_panel.grid(row=3, column=0, padx=5, pady=(5, 0))
        self.optionmenu_solar_panel = customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                                        values=["Monocrystalline", "Polycrystalline", "PERC", "Thin film", "..."])
        self.optionmenu_solar_panel.grid(row=4, column=0, padx=5, pady=(5, 5))
        self.edit_button_solar_panel = customtkinter.CTkButton(self.sidebar_frame, width=60, text="Edit", command=self.edit_battery)
        self.edit_button_solar_panel.grid(row=4, column=1, padx=5, pady=(5, 5))

        # Option Menu for EVCharger
        self.label_ev_charger = customtkinter.CTkLabel(self.sidebar_frame, text="EV Charger", font=customtkinter.CTkFont(size=15))
        self.label_ev_charger.grid(row=5, column=0, padx=5, pady=(5, 0))
        self.optionmenu_ev_charger = customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                                        values=["Type 1", "Type 2", "Type 3"])
        self.optionmenu_ev_charger.grid(row=6, column=0, padx=20, pady=(5, 30))
        self.edit_button_ev_charger = customtkinter.CTkButton(self.sidebar_frame, width=60, text="Edit", command=self.edit_battery)
        self.edit_button_ev_charger.grid(row=6, column=1, padx=5, pady=(5, 30))

        # create main entry and button
        self.entry_latitude = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Latitude")
        self.entry_latitude.grid(row=7, column=0, padx=20, pady=(5, 5), columnspan=2)

        self.entry_longitude = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Longitude")
        self.entry_longitude.grid(row=8, column=0, padx=20, pady=(5, 25), columnspan=2)

        self.entry_start_date = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Start date")
        self.entry_start_date.grid(row=9, column=0, padx=20, pady=(5, 5), columnspan=2)

        self.entry_end_date = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="End date")
        self.entry_end_date.grid(row=10, column=0, padx=20, pady=(5, 25), columnspan=2)


        #self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="battery", command=self.sidebar_button_event)
        #self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Start Sim.", command=lambda: self.start_process("50.9254992", "5.3932811", "16/03/2018", "16/04/2018"))
        self.sidebar_button_2.grid(row=11, column=0, padx=20, pady=10, columnspan=2)

        # Update layout after adding widgets
        self.sidebar_frame.update_idletasks()
        self.sidebar_frame_width = self.sidebar_frame.winfo_reqwidth()  # Get the required width of the sidebar frame
        self.sidebar_frame.grid_configure(padx=(0, 10))  # Adjust padding as needed

        # set default values
        customtkinter.set_appearance_mode("Dark")

        # create Matplotlib graphs
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 9))
        self.canvas1 = FigureCanvasTkAgg(self.fig, master=self)

        self.ax1.set_title('Not Optimized')
        self.ax2.set_title('Battery Charge')
        
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('kWh')

        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('Charge (kWh)')

        self.canvas1.get_tk_widget().grid(row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew")

        # Adjust layout to add space between subplots
        plt.subplots_adjust(hspace=0.4)


        # create sidebar frame with widgets
        self.sidebar_frame2 = customtkinter.CTkFrame(self, corner_radius=0, border_width=2)
        self.sidebar_frame2.grid(row=1, column=1, sticky="nsew")
        self.sidebar_frame2.grid_rowconfigure(10, weight=1)
        self.logo_label2 = customtkinter.CTkLabel(self.sidebar_frame2, text="Sim Results", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label2.grid(row=0, column=0, padx=20, pady=(20, 5), columnspan=4)

        self.label_result1 = customtkinter.CTkLabel(self.sidebar_frame2, text="Grid Extraction:", font=customtkinter.CTkFont(size=15))
        self.label_result1.grid(row=1, column=0, padx=20, pady=(5, 5))
        self.label_result1 = customtkinter.CTkLabel(self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=15))
        self.label_result1.grid(row=1, column=1, padx=(0,30), pady=(5, 0))

        self.label_result2 = customtkinter.CTkLabel(self.sidebar_frame2, text="Grid Injection:", font=customtkinter.CTkFont(size=15))
        self.label_result2.grid(row=2, column=0, padx=20, pady=(5, 20))
        self.label_result2 = customtkinter.CTkLabel(self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=15))
        self.label_result2.grid(row=2, column=1, padx=(0,30), pady=(5, 20))

        self.label_result3 = customtkinter.CTkLabel(self.sidebar_frame2, text="Total Cost:", font=customtkinter.CTkFont(size=15))
        self.label_result3.grid(row=1, column=2, padx=5, pady=(5, 5))
        self.label_result3 = customtkinter.CTkLabel(self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=15))
        self.label_result3.grid(row=1, column=3, padx=(0,15), pady=(5, 0))

        self.label_result4 = customtkinter.CTkLabel(self.sidebar_frame2, text="Total Earning:", font=customtkinter.CTkFont(size=15))
        self.label_result4.grid(row=2, column=2, padx=5, pady=(5, 20))
        self.label_result4 = customtkinter.CTkLabel(self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=15))
        self.label_result4.grid(row=2, column=3, padx=(0,15), pady=(5, 20))


    def update_graphs_with_new_data(self, data_points):
        # Perform some calculations to get new data
        time_values = [point['time_value'] for point in data_points]
        pv_power_values = [point['pv_power_value'] for point in data_points]
        power_usage_values = [-point['power_usage_value'] for point in data_points]
        charge_values = [max(0, point['charge_value']) for point in data_points]
        discharge_values = [min(0, point['charge_value']) for point in data_points]
        soc_values = [point['soc_value'] for point in data_points]
        grid_injection_values = [min(0, point['grid_usage']) for point in data_points]
        grid_extraction_values = [max(0, point['grid_usage']) for point in data_points]

        discharge_values = [-1 * x for x in discharge_values]
        charge_values = [-1 * x for x in charge_values]

        # Calculate sum of positive and negative residue values
        grid_injection_sum = sum(grid_injection_values)
        grid_extraction_sum = sum(grid_extraction_values)

        # Calculate cost for grid injection and grid extraction assuming energy cost of 0.1 euro per kWh
        grid_injection_cost = grid_injection_sum * 0.035
        grid_extraction_cost = grid_extraction_sum * -0.1211

        #code to display in text field
        self.label_result1.configure(text=str(round(grid_extraction_sum, 4)) + " kWh")
        self.label_result2.configure(text=str(round(grid_injection_sum, 4)) + " kWh")
        self.label_result3.configure(text=str(round(grid_extraction_cost, 4)) + " €")
        self.label_result4.configure(text=str(round(grid_injection_cost, 4)) + " €")

        # Clear existing plots
        self.ax1.clear()
        self.ax2.clear()

        df = pd.DataFrame({'Time': time_values,
                   'soc': soc_values,
                   'PV Power': pv_power_values,
                   'Grid Extraction': grid_extraction_values,
                   'Discharge': discharge_values,
                   'Power Usage': power_usage_values,
                   'Charge': charge_values,
                   'Grid Injection': grid_injection_values})

        print(df)

        print(len(pv_power_values))
        print(len(grid_extraction_values))
        print(len(discharge_values))
        print(len(power_usage_values))
        print(len(charge_values))

        # Calculate bottom values
        bottom_discharge = [x + y for x, y in zip(pv_power_values, grid_extraction_values)]

        bottom_injection = [x + y for x, y in zip(power_usage_values, charge_values)]

        self.ax1.bar(time_values, pv_power_values, color='g', width=0.02)
        self.ax1.bar(time_values, grid_extraction_values, bottom=pv_power_values, color='b', width=0.02)
        self.ax1.bar(time_values, discharge_values, bottom=bottom_discharge, color='y', width=0.02)
        
        self.ax1.bar(time_values, power_usage_values, color='r', width=0.02)
        self.ax1.bar(time_values, charge_values, bottom=power_usage_values, color='c', width=0.02)
        self.ax1.bar(time_values, grid_injection_values, bottom=bottom_injection, color='m', width=0.02)

        # Customize the plot
        self.ax1.legend(["PV Power", "Grid Extraction", "Discharge", "Power Usage", "Charge", "Grid Injection"])
        self.ax1.axhline(y=0, color='C0', linestyle='-', linewidth=1)
        self.ax1.set_title('Not Optimized')

        self.ax2.bar(time_values, soc_values, width=0.01)
        self.ax2.axhline(y=0, color='C0', linestyle='-', linewidth=1)
        self.ax2.set_title('Battery Charge')

        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('kWh')

        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('Charge (kWh)')

        # Filter time values to display only every 6 hours
        filtered_time_values = [time_values[i] for i in range(len(time_values)) if i % 12 == 0]
        self.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Format to display only hour and minute
        self.ax1.set_xticks(filtered_time_values)
        self.ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Format to display only hour and minute
        self.ax2.set_xticks(filtered_time_values)

        # Redraw canvas
        self.canvas1.draw()

    # TODO this doesnt work yet
    def populate_battery_options(self):
        # Fetch battery data from the database
        battery_data = self.db_manager.fetch_battery_data()
        # Extract battery names
        self.battery_options = [battery[1] for battery in battery_data]
        # Update option menu with battery names   
        self.optionmenu_battery.configure(values=self.battery_options)
        self.optionmenu_battery.set(self.battery_options[0])

    def edit_battery(self):
        edit_dialog = BatteryManager(self.db_manager, callback=self.populate_battery_options)
        
    def start_process(self, latitude, longitude, start_date, end_date):
        
        selected_battery = self.optionmenu_battery.get()
        selected_battery_data = self.db_manager.fetch_battery_by_name(selected_battery)

        # Initialize battery using the retrieved data
        battery = Battery(
            capacity=selected_battery_data[2],
            soc=1,
            charge_power=selected_battery_data[3],
            discharge_power=selected_battery_data[4],
            max_soc=selected_battery_data[5],
            min_dod=selected_battery_data[6],
            efficiency=selected_battery_data[7]
        )

        #.battery = Battery(capacity=2, soc=2, charge_power=5.0, discharge_power=5.0, max_soc=0.95, min_dod=0.05, efficiency=0.90)
        pybamm_battery = PyBaMM_Battery(capacity=2, soc=1, charge_power=5.0, discharge_power=5.0, max_soc=0.95, min_dod=0.05, efficiency=0.9)

        # the used data_points list is formatted like this data_points = ['pv_power_value', 'time_value', 'soc_value', 'charge_value', 'grid_usage', 'power_usage_value']
        # where pv_power_value is in kWh
        # time_value is in dd/mm/yy
        # soc_value is in kWh
        # charge_value is in kWh and is positive when charged and negative when discharged
        # grid_usage is in kWh and is positive when extracted and is negative when injected

        data_points = retrieve_data_api(latitude, longitude, start_date, end_date)

        data_points = get_power_usage_values(data_points)

        data_points = process_data(data_points, battery, pybamm_battery)

        #time_values, new_charge_values = calculate_new_values(time_values, charge_values, daily_average_usage)

        self.update_graphs_with_new_data(data_points)

if __name__ == "__main__":
    app = App()
    app.mainloop()