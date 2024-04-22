import time
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
from scipy.interpolate import interp1d
import pandas as pd
from battery import Battery
from databaseManager import DatabaseManager
from batteryManager import BatteryManager
from process import (
    calculate_values,
    get_power_usage_values,
    process_data,
    scale_list,
)
from processPVPower import process_solar_data
from processPrices import process_prices_data
from pybammBattery import PyBaMM_Battery
import csv
import matplotlib.dates as mdates
import datetime
import numpy as np

from simulationDialog import SimulationDialog

customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "green"
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
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        customtkinter.set_appearance_mode("Dark")


        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, corner_radius=0, border_width=2
        )
        self.sidebar_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        #self.sidebar_frame.grid_rowconfigure(18, weight=1)
        #self.sidebar_frame.grid_propagate(False)  # Prevent resizing
        
        #####################################################
        
        # self.sidebar_button_1 = customtkinter.CTkButton(
        #     self.sidebar_frame,
        #     text="Start Simulation",
        #     command=lambda: self.start_process(
        #         self.entry_latitude.get(),
        #         self.entry_longitude.get(),
        #         self.entry_start_date.get(),
        #         self.entry_end_date.get()
        #     ),
        # )
        # self.sidebar_button_1.grid(row=0, column=0, padx=(20,20))
        
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Start Simulation",
            command=self.start_process,
        )
        self.sidebar_button_1.grid(row=0, column=0, pady=(10,10), padx=(20,20))
        
        ######################################################
        
        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Simulation Parameters",
            command=self.simulation_parameters,
        )
        self.sidebar_button_2.grid(row=0, column=1, padx=(20,20))
        
        ######################################################
        
        # Option Menu for Simulation scale
        self.label_scale = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Visualisation:",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.label_scale.grid(row=0, column=2, padx=(40,0))
        
        self.optionmenu_scale = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            dynamic_resizing=False, values=["PER YEAR", "PER MONTH", "PER WEEK", "SPECIFIC MONTH", "SPECIFIC WEEK", "SPECIFIC DAY"],
            command=self.update_time_options
        )
        self.optionmenu_scale.grid(row=0, column=3, padx=(20,0))
        
        self.optionmenu_time = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            width=60,
            values=[""]
        )
        self.optionmenu_time.grid(row=0, column=4, padx=(20, 20))

        #######################################################

        # Update layout after adding widgets
        self.sidebar_frame.update_idletasks()
        self.sidebar_frame_width = (
            self.sidebar_frame.winfo_reqwidth()
        )  # Get the required width of the sidebar frame
        self.sidebar_frame.grid_configure(padx=(0, 10))  # Adjust padding as needed

        # set default values
        customtkinter.set_appearance_mode("Dark")

        #######################################################
    
        # create Matplotlib graphs
        self.fig, (self.ax1, self.ax2) = plt.subplots(
            2, 1, figsize=(13, 7), gridspec_kw={"height_ratios": [2, 1]}
        )
        self.fig.patch.set_facecolor("#c4d404")
        
        self.ax1.set_facecolor("#c4d404")  # Change to your desired color
        self.ax2.set_facecolor("#c4d404")  # Change to your desired color

        self.canvas1 = FigureCanvasTkAgg(self.fig, master=self)

        self.canvas1.get_tk_widget().grid(
            row=1, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew"
        )

        # Adjust layout to add space between subplots
        plt.subplots_adjust(hspace=0.4)
        
        ######################################################

        # create sidebar frame with widgets
        self.sidebar_frame2 = customtkinter.CTkFrame(
            self, corner_radius=0, border_width=2
        )
        self.sidebar_frame2.grid(row=1, column=1, sticky="nsew")
        
        
        self.logo_label1 = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Sim Results",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label1.grid(row=0, column=0, pady=(20,20), columnspan=3)
        
        self.logo_label2 = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Default",
            font=customtkinter.CTkFont(size=15),
        )
        self.logo_label2.grid(row=1, column=1, padx=(0,10))
        
        self.logo_label3 = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Optimized",
            font=customtkinter.CTkFont(size=15),
        )
        self.logo_label3.grid(row=1, column=2, padx=(0,20))

        ############################################################

        self.label_extraction = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Total Grid Extraction:",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_extraction.grid(row=2, column=0, padx=20, pady=(5, 0), sticky="w")
        
        self.label_extraction_result_1 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=10)
        )
        self.label_extraction_result_1.grid(row=2, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_extraction_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=10)
        )
        self.label_extraction_result_2.grid(row=2, column=2, pady=(5, 0) )

        ############################################################

        self.label_injection = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Total Grid Injection:",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_injection.grid(row=3, column=0, padx=20, pady=(5, 0) , sticky="w")
        
        self.label_injection_result_1 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=10)
        )
        self.label_injection_result_1.grid(row=3, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_injection_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=10)
        )
        self.label_injection_result_2.grid(row=3, column=2, pady=(5, 0) )

        ###########################################################
        
        self.label_charge = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Total Bat. Charge:",
            anchor="w",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_charge.grid(row=4, column=0, padx=20, pady=(5, 0) , sticky="w")
        
        self.label_charge_result_1 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=10)
        )
        self.label_charge_result_1.grid(row=4, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_charge_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=10)
        )
        self.label_charge_result_2.grid(row=4, column=2, pady=(5, 0) )

        ###########################################################
        
        self.label_discharge = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Total Bat. Discharge:",
            anchor="w",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_discharge.grid(row=5, column=0, padx=20, pady=(5, 0) , sticky="w")
        
        self.label_discharge_result_1 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=10)
        )
        self.label_discharge_result_1.grid(row=5, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_discharge_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=10)
        )
        self.label_discharge_result_2.grid(row=5, column=2, pady=(5, 0) )

        ###########################################################
        
        self.label_pv_production = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Total Pv Production:",
            anchor="w",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_pv_production.grid(row=6, column=0, padx=20, pady=(5, 0) , sticky="w")
        
        self.label_pv_production_result_1 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=10)
        )
        self.label_pv_production_result_1.grid(row=6, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_pv_production_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=10)
        )
        self.label_pv_production_result_2.grid(row=6, column=2, pady=(5, 0) )

        ###########################################################
        
        self.label_power_use = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Total Power Use:",
            anchor="w",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_power_use.grid(row=7, column=0, padx=20, pady=(5, 0) , sticky="w")
        
        self.label_power_use_result_1 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=10)
        )
        self.label_power_use_result_1.grid(row=7, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_power_use_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=10)
        )
        self.label_power_use_result_2.grid(row=7, column=2, pady=(5, 0) )

        ###########################################################
        
        self.label_earning = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Total Earning:",
            anchor="w",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_earning.grid(row=8, column=0, padx=20, pady=(5, 0) , sticky="w")
        
        self.label_earning_result_1 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=10)
        )
        self.label_earning_result_1.grid(row=8, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_earning_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=10)
        )
        self.label_earning_result_2.grid(row=8, column=2, pady=(5, 0) )

        ###########################################################
        
        self.label_cost = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Total Cost:",
            anchor="w",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_cost.grid(row=9, column=0, padx=20, pady=(5, 0) , sticky="w")
        
        self.label_cost_result_1 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=10)
        )
        self.label_cost_result_1.grid(row=9, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_cost_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=10)
        )
        self.label_cost_result_2.grid(row=9, column=2, pady=(5, 0) )

        ###########################################################
        
        
        
        
        
        #set default values
        #self.entry_start_date.insert(tkinter.END, '2023-01-01')
        #self.entry_end_date.insert(tkinter.END, '2024-01-01')
        #self.entry_latitude.insert(tkinter.END, "50.92549")
        #self.entry_longitude.insert(tkinter.END, "5.39328")
        self.optionmenu_time.set("/")

    def simulation_parameters(self):
        simulation_dialog = SimulationDialog(
            self.db_manager
        )
    
    def update_graphs_with_new_data(self, data_points):

        calculated_values = calculate_values(data_points, self.optionmenu_time.get(), self.optionmenu_scale.get())

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
        grid_extraction_prices = calculated_values["grid_extraction_prices"]

        grid_injection_sum = calculated_values["grid_injection_sum"]
        grid_extraction_sum = calculated_values["grid_extraction_sum"]

        grid_injection_cost = calculated_values["grid_injection_cost"]
        grid_extraction_cost = calculated_values["grid_extraction_cost"]

        # code to display in text field
        self.label_result1.configure(text=str(round(grid_extraction_sum, 4)) + " kWh")
        self.label_result2.configure(text=str(abs(round(grid_injection_sum, 4))) + " kWh")
        self.label_result3.configure(text=str(round(grid_extraction_cost, 4)) + " €")
        self.label_result4.configure(text=str(abs(round(grid_injection_cost, 4))) + " €")
        self.label_result5.configure(text=str(abs(round(sum(pv_power_values, 4)))) + " kWh")
        self.label_result6.configure(text=str(abs(round(sum(power_usage_values, 4)))) + " kWh")
        self.label_result7.configure(text=str(abs(round(sum(charge_values, 4)))) + " kWh")
        self.label_result8.configure(text=str(abs(round(sum(discharge_values, 4)))) + " kWh")

        # Clear existing plots
        self.ax1.clear()
        self.ax2.clear()
        #self.ax3.clear()

        # Calculate bottom values
        bottom_extraction = [x + y for x, y in zip(pv_power_values, discharge_values)]
        bottom_injection = [x + y for x, y in zip(power_usage_values, charge_values)]

        line_width = calculated_values["line_width"]
        self.ax1.set_title(calculated_values["title"])
        self.ax1.set_xlabel("Time")            

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
            color="#4C00A4",
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
        self.ax1.set_ylabel("kWh")

        new_soc_values = scale_list(soc_values, len(grid_extraction_prices))
        
        grid_injection_prices_scaled = scale_list(grid_injection_prices, 400)
        grid_extraction_prices_scaled = scale_list(grid_extraction_prices, 400)
        
        # Plot injection and extraction prices with their y-axis on the left
        self.ax2.plot(grid_injection_prices_scaled, color="y", label="Injection Prices", linewidth=0.5)
        self.ax2.plot(grid_extraction_prices_scaled, color="g", label="Extraction Prices", linewidth=0.5)
        self.ax2.set_ylabel("Grid Prices per MWh")
        self.ax2.set_xlabel("Time")
        self.ax2.tick_params(axis='y', labelcolor="black")

        
        # self.ax3.plot(new_soc_values, color="k", label="Battery Charge")
        # self.ax3.set_ylabel("Battery Charge kWh")
        # self.ax3.tick_params(axis='y', labelcolor="black")  # Change y-axis label color to green

        # Add legend
        self.ax2.legend(loc="upper left")
        #self.ax3.legend(loc="upper right")
        

        filtered_time_values = [
            time_values[i] for i in range(len(time_values)) if i % 24 == 0
        ]
        # self.ax1.xaxis.set_major_formatter(
        #     mdates.DateFormatter("%H:%M")
        # )  # Format to display only hour and minute
        # self.ax1.set_xticks(filtered_time_values)

        # Redraw canvas
        self.canvas1.draw()

    # TODO this doesnt work yet
    def populate_battery_options(self):
        # Fetch battery data from the database
        battery_data = self.db_manager.fetch_battery_data()
        print(battery_data)
        # Extract battery names
        battery_options = [battery[1] for battery in battery_data]
        # Update option menu with battery names
        self.optionmenu_battery.option_clear
        self.optionmenu_battery.configure(values=battery_options)
        self.optionmenu_battery.set(battery_options[0])

    def edit_battery(self):
        edit_dialog = BatteryManager(
            self.db_manager, callback=self.populate_battery_options
        )
        self.populate_battery_options()
        
    def update_time_options(self, event):
        selected_scale = self.optionmenu_scale.get()
        time_options = []

        if selected_scale == "SPECIFIC MONTH":
            time_options = [str(x) for x in range(1, 13)]  # Months from 0 to 12
        elif selected_scale == "SPECIFIC WEEK":
            time_options = [str(x) for x in range(1, 53)]  # Weeks from 0 to 52
        elif selected_scale == "SPECIFIC DAY":
            for month in range(1, 13):
                for day in range(1, 32):
                    try:
                        date = datetime.date(2023, month, day)
                        time_options.append((date.strftime("%d-%m")))
                    except ValueError:
                        # Handle cases where the day is out of range for the month
                        pass
        else: 
            time_options = ["/"]
        
        # Update the option menu for time values
        self.optionmenu_time.option_clear
        self.optionmenu_time.configure(values=time_options)
        self.optionmenu_time.set(time_options[0])

    def start_process(self, latitude, longitude, start_date, end_date):

        selected_battery = self.optionmenu_battery.get()
        selected_battery_data = self.db_manager.fetch_battery_by_name(selected_battery)
        selected_user_profile = self.optionmenu_consumer.get()

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

        data_points = get_power_usage_values(data_points, selected_user_profile)
        
        data_points = process_prices_data(data_points, latitude, longitude)
        
        data_points = process_data(data_points, battery, pybamm_battery)

        self.update_graphs_with_new_data(data_points)
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
