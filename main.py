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
from process import (
    calculate_values,
    get_power_usage_values,
    process_data,
)
from processPVPower import process_solar_data
from processPrices import process_prices_data
from pybammBattery import PyBaMM_Battery
import csv
import matplotlib.dates as mdates
import datetime
import numpy as np

customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager(
            "database_master.db"
        )  # Create an instance of DatabaseManager

        # configure window
        self.title("Smart Home Simulation")
        # self.geometry(f"{1280}x{760}")

        # configure grid layout (2x3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        customtkinter.set_appearance_mode("Dark")

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=265, corner_radius=0, border_width=2
        )
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(16, weight=1)
        self.sidebar_frame.grid_propagate(False)  # Prevent resizing

        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Simulation Params",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(15, 20), columnspan=2)

        # Option Menu for Battery
        self.label_battery = customtkinter.CTkLabel(
            self.sidebar_frame, text="Battery", font=customtkinter.CTkFont(size=15)
        )
        self.label_battery.grid(row=1, column=0, padx=5, pady=(5, 0))
        self.optionmenu_battery = customtkinter.CTkOptionMenu(
            self.sidebar_frame, dynamic_resizing=False
        )
        self.optionmenu_battery.grid(row=2, column=0, padx=20, pady=(5, 5))
        self.edit_button_battery = customtkinter.CTkButton(
            self.sidebar_frame, width=60, text="Edit", command=self.edit_battery
        )
        self.edit_button_battery.grid(row=2, column=1, padx=5, pady=(5, 5))
        self.populate_battery_options()

        # Option Menu for SolarPanel
        self.label_solar_panel = customtkinter.CTkLabel(
            self.sidebar_frame, text="Solar Panel", font=customtkinter.CTkFont(size=15)
        )
        self.label_solar_panel.grid(row=3, column=0, padx=5, pady=(5, 0))
        self.optionmenu_solar_panel = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            dynamic_resizing=False,
            values=["Monocrystalline", "Polycrystalline", "PERC", "Thin film", "..."],
        )
        self.optionmenu_solar_panel.grid(row=4, column=0, padx=5, pady=(5, 5))
        self.edit_button_solar_panel = customtkinter.CTkButton(
            self.sidebar_frame, width=60, text="Edit", command=self.edit_battery
        )
        self.edit_button_solar_panel.grid(row=4, column=1, padx=5, pady=(5, 5))

        # Option Menu for EVCharger
        self.label_ev_charger = customtkinter.CTkLabel(
            self.sidebar_frame, text="EV Charger", font=customtkinter.CTkFont(size=15)
        )
        self.label_ev_charger.grid(row=5, column=0, padx=5, pady=(5, 0))
        self.optionmenu_ev_charger = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            dynamic_resizing=False,
            values=["Type 1", "Type 2", "Type 3"],
        )
        self.optionmenu_ev_charger.grid(row=6, column=0, padx=20, pady=(5, 5))
        self.edit_button_ev_charger = customtkinter.CTkButton(
            self.sidebar_frame, width=60, text="Edit", command=self.edit_battery
        )
        self.edit_button_ev_charger.grid(row=6, column=1, padx=5, pady=(5, 5))

        # Option Menu for consumer profiles
        self.label_consumer = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Consumer Profile",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_consumer.grid(row=7, column=0, columnspan=2, padx=5, pady=(15, 0))
        self.optionmenu_consumer = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            dynamic_resizing=False,
            values=[
                "Single person",
                "couple",
                "singe with kids",
                "couple with kids",
                "pensioner",
            ],
        )
        self.optionmenu_consumer.grid(
            row=8, column=0, columnspan=2, padx=20, pady=(5, 30)
        )

        # create main entry and button
        self.entry_latitude = customtkinter.CTkEntry(
            self.sidebar_frame, placeholder_text="Latitude"
        )
        self.entry_latitude.grid(row=9, column=0, pady=(5, 5), columnspan=2)

        self.entry_longitude = customtkinter.CTkEntry(
            self.sidebar_frame, placeholder_text="Longitude"
        )
        self.entry_longitude.grid(row=10, column=0, pady=(5, 25), columnspan=2)

        self.entry_start_date = customtkinter.CTkEntry(
            self.sidebar_frame, placeholder_text="Start date"
        )
        self.entry_start_date.grid(row=11, column=0, padx=20, pady=(5, 5), columnspan=2)

        self.entry_end_date = customtkinter.CTkEntry(
            self.sidebar_frame, placeholder_text="End date"
        )
        self.entry_end_date.grid(row=12, column=0, padx=20, pady=(5, 0), columnspan=2)

        # Option Menu for Simulation scale
        self.label_scale = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Simulation scale",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_scale.grid(row=13, column=0, columnspan=2, padx=5, pady=(15, 0))
        self.optionmenu_scale = customtkinter.CTkOptionMenu(
            self.sidebar_frame, dynamic_resizing=False, values=["DAY", "MONTH", "YEAR"]
        )
        self.optionmenu_scale.grid(row=14, column=0, columnspan=2, pady=(5, 0))

        # self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="battery", command=self.sidebar_button_event)
        # self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Start Sim.",
            command=lambda: self.start_process(
                "50.9254992", "5.3932811", "16/03/2018", "16/04/2018"
            ),
        )
        self.sidebar_button_2.grid(row=15, column=0, padx=20, pady=25, columnspan=2)

        # Update layout after adding widgets
        self.sidebar_frame.update_idletasks()
        self.sidebar_frame_width = (
            self.sidebar_frame.winfo_reqwidth()
        )  # Get the required width of the sidebar frame
        self.sidebar_frame.grid_configure(padx=(0, 10))  # Adjust padding as needed

        # set default values
        customtkinter.set_appearance_mode("Dark")

        # create Matplotlib graphs
        self.fig, (self.ax1, self.ax2) = plt.subplots(
            2, 1, figsize=(15, 7), gridspec_kw={"height_ratios": [2, 1]}
        )
        self.canvas1 = FigureCanvasTkAgg(self.fig, master=self)

        self.ax1.set_title("Not Optimized")
        self.ax2.set_title("Battery Charge")

        self.ax1.set_xlabel("Time")
        self.ax1.set_ylabel("kWh")

        self.ax2.set_xlabel("Time")
        self.ax2.set_ylabel("Charge (kWh)")

        self.canvas1.get_tk_widget().grid(
            row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew"
        )

        # Adjust layout to add space between subplots
        plt.subplots_adjust(hspace=0.4)

        # create sidebar frame with widgets
        self.sidebar_frame2 = customtkinter.CTkFrame(
            self, corner_radius=0, border_width=2
        )
        self.sidebar_frame2.grid(row=1, column=1, sticky="nsew")
        self.sidebar_frame2.grid_rowconfigure(10, weight=1)
        self.logo_label2 = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Sim Results",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label2.grid(row=0, column=0, padx=20, pady=(20, 5), columnspan=4)

        self.label_result1 = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Grid Extraction:",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_result1.grid(row=1, column=0, padx=20, pady=(5, 5))
        self.label_result1 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=15)
        )
        self.label_result1.grid(row=1, column=1, padx=(0, 30), pady=(5, 0))

        self.label_result2 = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Grid Injection:",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_result2.grid(row=2, column=0, padx=20, pady=(5, 20))
        self.label_result2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=15)
        )
        self.label_result2.grid(row=2, column=1, padx=(0, 30), pady=(5, 20))

        self.label_result3 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="Total Cost:", font=customtkinter.CTkFont(size=15)
        )
        self.label_result3.grid(row=1, column=2, padx=5, pady=(5, 5))
        self.label_result3 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=15)
        )
        self.label_result3.grid(row=1, column=3, padx=(0, 15), pady=(5, 0))

        self.label_result4 = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Total Earning:",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_result4.grid(row=2, column=2, padx=5, pady=(5, 20))
        self.label_result4 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=15)
        )
        self.label_result4.grid(row=2, column=3, padx=(0, 15), pady=(5, 20))

    def update_graphs_with_new_data(self, data_points):

        calculated_values = calculate_values(data_points, self.optionmenu_scale.get())

        # Perform some calculations to get new data
        time_values = calculated_values["time_values"]
        pv_power_values = calculated_values["pv_power_values"]
        power_usage_values = calculated_values["power_usage_values"]
        charge_values = calculated_values["charge_values"]
        discharge_values = calculated_values["discharge_values"]
        soc_values = calculated_values["soc_values"]
        grid_injection_values = calculated_values["injection_values"]
        grid_extraction_values = calculated_values["extraction_values"]
        
        grid_injection_prices = calculated_values["grid_injection_prices"]
        grid_extraction_prices = calculated_values["grid_injection_prices"]

        grid_injection_sum = calculated_values["grid_injection_sum"]
        grid_extraction_sum = calculated_values["grid_extraction_sum"]

        grid_injection_cost = calculated_values["grid_injection_cost"]
        grid_extraction_cost = calculated_values["grid_extraction_cost"]

        # code to display in text field
        self.label_result1.configure(text=str(round(grid_extraction_sum, 4)) + " kWh")
        self.label_result2.configure(text=str(round(grid_injection_sum, 4)) + " kWh")
        self.label_result3.configure(text=str(round(grid_extraction_cost, 4)) + " €")
        self.label_result4.configure(text=str(round(grid_injection_cost, 4)) + " €")

        # Clear existing plots
        self.ax1.clear()
        self.ax2.clear()

        # Calculate bottom values
        bottom_extraction = [x + y for x, y in zip(pv_power_values, discharge_values)]
        bottom_injection = [x + y for x, y in zip(power_usage_values, charge_values)]

        line_width = 0.5

        self.ax1.bar(
            time_values, 
            pv_power_values, 
            color="y", 
            width=line_width
        )
        self.ax1.bar(
            time_values,
            discharge_values,
            bottom=pv_power_values,
            color="#FF0000",
            width=line_width,
        )
        self.ax1.bar(
            time_values,
            grid_extraction_values,
            bottom=bottom_extraction,
            color="b",
            width=line_width,
        )

        self.ax1.bar(
            time_values, 
            power_usage_values, 
            color="c", 
            width=line_width
        )
        self.ax1.bar(
            time_values,
            charge_values,
            bottom=power_usage_values,
            color="#009600",
            width=line_width,
        )
        self.ax1.bar(
            time_values,
            grid_injection_values,
            bottom=bottom_injection,
            color="m",
            width=line_width,
        )

        # Customize the plot
        self.ax1.legend(
            [
                "PV Power",
                "Discharge",
                "Grid Extraction",
                "Power Usage",
                "Charge",
                "Grid Injection",
            ]
        )
        self.ax1.axhline(y=0, color="k", linestyle="-", linewidth=0.1)
        self.ax1.set_title("Not Optimized")
        self.ax1.set_xlabel("Time")
        self.ax1.set_ylabel("kWh")

        #self.ax2.plot(time_values, soc_values, color="k")
        self.ax2.plot(list(range(len(grid_injection_prices))), grid_injection_prices, color="m")
        self.ax2.plot(list(range(len(grid_extraction_prices))), grid_extraction_prices, color="b")
        self.ax2.set_title("Battery Charge")
        self.ax2.set_xlabel("Time")
        self.ax2.set_ylabel("Charge (kWh)")

        # Filter time values to display only every 6 hours
        filtered_time_values = [
            time_values[i] for i in range(len(time_values)) if i % 24 == 0
        ]
        # self.ax1.xaxis.set_major_formatter(
        #     mdates.DateFormatter("%H:%M")
        # )  # Format to display only hour and minute
        # self.ax1.set_xticks(filtered_time_values)
        # self.ax2.xaxis.set_major_formatter(
        #     mdates.DateFormatter("%H:%M")
        # )  # Format to display only hour and minute
        # self.ax2.set_xticks(filtered_time_values)

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
        edit_dialog = BatteryManager(
            self.db_manager, callback=self.populate_battery_options
        )

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
            efficiency=selected_battery_data[7],
        )

        # .battery = Battery(capacity=2, soc=2, charge_power=5.0, discharge_power=5.0, max_soc=0.95, min_dod=0.05, efficiency=0.90)
        pybamm_battery = PyBaMM_Battery(
            capacity=2,
            soc=1,
            charge_power=5.0,
            discharge_power=5.0,
            max_soc=0.95,
            min_dod=0.05,
            efficiency=0.9,
        )

        # the used data_points list is formatted like this data_points = ['pv_power_value', 'time_value', 'soc_value', 'charge_value', 'grid_usage', 'power_usage_value']
        # where pv_power_value is in kWh
        # time_value is in dd/mm/yy
        # soc_value is in kWh
        # charge_value is in kWh and is positive when charged and negative when discharged
        # grid_usage is in kWh and is positive when extracted and is negative when injected

        data_points = process_solar_data(latitude, longitude, start_date, end_date)

        data_points = get_power_usage_values(data_points)
        
        data_points = process_prices_data(data_points, latitude, longitude)

        data_points = process_data(data_points, battery, pybamm_battery)

        # time_values, new_charge_values = calculate_new_values(time_values, charge_values, daily_average_usage)

        self.update_graphs_with_new_data(data_points)


if __name__ == "__main__":
    app = App()
    app.mainloop()
