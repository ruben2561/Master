import copy
import math
import time
import tkinter
import tkinter.messagebox
from PIL import Image, ImageTk
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
from process import (
    calculate_values,
    get_power_usage_values,
    process_data,
    process_data_optimized,
    scale_list,
)
from processPVPower import process_solar_data
from processPrices import process_prices_data
import csv
import matplotlib.dates as mdates
import datetime
import numpy as np

from simulationDialog import SimulationDialog

customtkinter.set_appearance_mode("Dark")
# Set the default color theme to use the custom theme
customtkinter.set_default_color_theme("MPTheme.json")



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

        self.data_available = False

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, corner_radius=0, border_width=2
        )
        self.sidebar_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        #self.sidebar_frame.grid_rowconfigure(18, weight=1)
        #self.sidebar_frame.grid_propagate(False)  # Prevent resizing
        
        #####################################################
        
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Start Simulation",
            command=self.verify_parameters
            ,
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
            command=self.update_date_options
        )
        self.optionmenu_scale.grid(row=0, column=3, padx=(20,0))
        
        self.optionmenu_day = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            width=60,
            command=self.option_menu_time_event
        )
        self.optionmenu_day.grid(row=0, column=4, padx=(20, 0))
        
        self.optionmenu_month = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            width=80,
            command=self.option_menu_month_event
        )
        self.optionmenu_month.grid(row=0, column=5, padx=(5, 20))
        
        #######################################################
        
        self.image_uhasselt = customtkinter.CTkImage(dark_image=Image.open(os.path.join("images/uhasselt.png")), size=(80 * 1.5, 19 * 1.5))
        label_uhasselt = customtkinter.CTkLabel(self.sidebar_frame, image=self.image_uhasselt, text='')
        label_uhasselt.grid(row=0, column=6, padx=(200,0), sticky="e")
        
        self.image_ilumen = customtkinter.CTkImage(dark_image=Image.open(os.path.join("images/ilumen.png")), size=(72.4 * 1.4 , 29.2 * 1.4))
        label_ilumen = customtkinter.CTkLabel(self.sidebar_frame, image=self.image_ilumen, text='')
        label_ilumen.grid(row=0, column=7, padx=(20,0), sticky="e")

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
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(
            3, 1, figsize=(13, 8), gridspec_kw={"height_ratios": [2, 2, 2]}
        )
        
        self.ax4 = 0
        
        self.fig.patch.set_facecolor("#AEB74F")
        
        # Hide the plots initially
        #self.fig.patch.set_visible(False)
        self.ax1.set_visible(False)
        self.ax2.set_visible(False)
        self.ax3.set_visible(False)
        
        self.fig.tight_layout(pad=5.0)
        self.fig.subplots_adjust(right=0.8)
        
        self.ax1.set_facecolor("#FCFBF3")  # Change to your desired color
        self.ax2.set_facecolor("#FCFBF3")  # Change to your desired color
        self.ax3.set_facecolor("#FCFBF3")  # Change to your desired color

        self.canvas1 = FigureCanvasTkAgg(self.fig, master=self)

        self.canvas1.get_tk_widget().grid(
            row=1, column=0, sticky="w"
        )

        # Adjust layout to add space between subplots
        plt.subplots_adjust(hspace=0.6)
        
        ######################################################

        # create sidebar frame with widgets
        self.sidebar_frame2 = customtkinter.CTkFrame(
            self, corner_radius=0, border_width=2
        )
        self.sidebar_frame2.grid(row=1, column=1, sticky="nsew")
        
        
        self.logo_label1 = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Simulation Results",
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

        self.label_offtake = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Total Grid Offtake:",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_offtake.grid(row=2, column=0, padx=20, pady=(5, 0), sticky="w")
        
        self.label_offtake_result_1 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
        )
        self.label_offtake_result_1.grid(row=2, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_offtake_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
        )
        self.label_offtake_result_2.grid(row=2, column=2, pady=(5, 0) )

        ############################################################

        self.label_injection = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Total Grid Injection:",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_injection.grid(row=3, column=0, padx=20, pady=(5, 0) , sticky="w")
        
        self.label_injection_result_1 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
        )
        self.label_injection_result_1.grid(row=3, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_injection_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
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
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
        )
        self.label_charge_result_1.grid(row=4, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_charge_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
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
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
        )
        self.label_discharge_result_1.grid(row=5, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_discharge_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
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
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
        )
        self.label_pv_production_result_1.grid(row=6, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_pv_production_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
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
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
        )
        self.label_power_use_result_1.grid(row=7, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_power_use_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
        )
        self.label_power_use_result_2.grid(row=7, column=2, pady=(5, 0) )
        
        ###########################################################
        
        self.label_ev_charge = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Total Ev Charge:",
            anchor="w",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_ev_charge.grid(row=8, column=0, padx=20, pady=(5, 0) , sticky="w")
        
        self.label_ev_charge_result_1 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
        )
        self.label_ev_charge_result_1.grid(row=8, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_ev_charge_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
        )
        self.label_ev_charge_result_2.grid(row=8, column=2, pady=(5, 0) )

        ###########################################################
        
        self.label_earning = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Total Earning:",
            anchor="w",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_earning.grid(row=9, column=0, padx=20, pady=(5, 0) , sticky="w")
        
        self.label_earning_result_1 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
        )
        self.label_earning_result_1.grid(row=9, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_earning_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
        )
        self.label_earning_result_2.grid(row=9, column=2, pady=(5, 0) )

        ###########################################################
        
        self.label_cost = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Total Cost:",
            anchor="w",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_cost.grid(row=10, column=0, padx=20, pady=(5, 0) , sticky="w")
        
        self.label_cost_result_1 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
        )
        self.label_cost_result_1.grid(row=10, column=1, pady=(5, 0) , padx=(0,10))
        
        self.label_cost_result_2 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12)
        )
        self.label_cost_result_2.grid(row=10, column=2, pady=(5, 0) )

        ########################################################### 
        
        self.label_saved = customtkinter.CTkLabel(
            self.sidebar_frame2,
            text="Saved:",
            anchor="w",
            font=customtkinter.CTkFont(size=15, weight='bold'),
        )
        self.label_saved.grid(row=11, column=0, padx=20, pady=(15, 0) , sticky="w")
        
        self.label_saved_result_1 = customtkinter.CTkLabel(
            self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=12, weight='bold')
        )
        self.label_saved_result_1.grid(row=11, column=1, columnspan=2, pady=(15, 0) , padx=(0,10))
        
        ########################################################### 
        
        self.optionmenu_day.set(" ")
        self.optionmenu_month.set(" ")
        self.optionmenu_day.configure(fg_color="grey20", button_color="grey20", state = "disabled")
        self.optionmenu_month.configure(fg_color="grey20", button_color="grey20", state = "disabled")
        self.optionmenu_scale.set("PER MONTH")
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def simulation_parameters(self):
        simulation_dialog = SimulationDialog(self.db_manager)
        simulation_dialog.mainloop()
        
    #############################################################################
    #############################################################################
    #############################################################################
    
    def update_graphs_with_new_data(self, data_points, data_points_optimized):
        
        # Clear existing plots
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        
        self.ax1.set_visible(True)
        self.ax2.set_visible(True)
        self.ax3.set_visible(True)

        calculated_values = calculate_values(data_points, str(self.optionmenu_day.get()) + "-" + str(self.optionmenu_month.get()), self.optionmenu_scale.get())

        # Perform some calculations to get new data
        time_values = calculated_values["time_values"]
        pv_power_values = calculated_values["pv_power_values"]
        power_usage_values = calculated_values["power_usage_values"]
        charge_values = calculated_values["charge_values"]
        discharge_values = calculated_values["discharge_values"]
        soc_values = calculated_values["soc_values"]
        grid_injection_values = calculated_values["injection_values"]
        grid_offtake_values = calculated_values["offtake_values"]
        
        grid_injection_prices = calculated_values["grid_injection_prices"]
        grid_offtake_prices = calculated_values["grid_offtake_prices"]

        grid_injection_sum = calculated_values["grid_injection_sum"]
        grid_offtake_sum = calculated_values["grid_offtake_sum"]

        grid_injection_cost = calculated_values["grid_injection_cost"]
        grid_offtake_cost = calculated_values["grid_offtake_cost"]
        
        ev_charge_values = calculated_values["ev_charge_values"]
        
        # Create a DataFrame from the calculated values
        df = pd.DataFrame({
            "Time": time_values,
            "PV Power": pv_power_values,
            "Power Usage": power_usage_values,
            "Charge": charge_values,
            "Discharge": discharge_values,
            "SoC": scale_list(soc_values, len(power_usage_values)) if len(power_usage_values) > 1 else soc_values,
            "Grid Injection": grid_injection_values,
            "Grid Offtake": grid_offtake_values,
            "Ev Charge Values": ev_charge_values
        })

        # Print the DataFrame
        print(df)

        # code to display in text field
        self.label_offtake_result_1.configure(text=str(round(grid_offtake_sum, 3)) + " kWh")
        self.label_injection_result_1.configure(text=str(abs(round(grid_injection_sum, 3))) + " kWh")
        self.label_charge_result_1.configure(text=str(abs(round(sum(charge_values), 3))) + " kWh")
        self.label_discharge_result_1.configure(text=str(abs(round(sum(discharge_values), 3))) + " kWh")
        self.label_pv_production_result_1.configure(text=str(abs(round(sum(pv_power_values), 3))) + " kWh")
        self.label_power_use_result_1.configure(text=str(abs(round(sum(power_usage_values), 3))) + " kWh")
        self.label_ev_charge_result_1.configure(text=str(abs(round(sum(ev_charge_values), 3))) + " kWh")
        self.label_cost_result_1.configure(text=str(round(grid_offtake_cost, 3)) + " €")
        self.label_earning_result_1.configure(text=str(abs(round(grid_injection_cost, 3))) + " €")
        
        # Calculate bottom values
        bottom_offtake = [x + y for x, y in zip(pv_power_values, discharge_values)]
        bottom_charge = [x + y for x, y in zip(power_usage_values, ev_charge_values)]
        bottom_injection = [x + y + z for x, y, z in zip(power_usage_values, ev_charge_values, charge_values)]

        line_width = calculated_values["line_width"]
        self.ax1.set_title(calculated_values["title"])
        self.ax1.set_xlabel("Time")            

        self.ax1.bar(
            time_values, 
            pv_power_values, 
            color="y", 
            label="PV Power",
            width=line_width
        )
        self.ax1.bar(
            time_values,
            discharge_values,
            bottom=pv_power_values,
            color="#FF0000",
            label="Bat. Discharge",
            width=line_width,
        )
        self.ax1.bar(
            time_values,
            grid_offtake_values,
            bottom=bottom_offtake,
            color="b",
            label="Grid Offtake",
            width=line_width,
        )

        self.ax1.bar(
            time_values, 
            power_usage_values, 
            color="c", 
            label="Power Usage",
            width=line_width
        )
        self.ax1.bar(
            time_values, 
            ev_charge_values,
            bottom=power_usage_values, 
            color="black", 
            label="Ev Charge",
            width=line_width
        )
        self.ax1.bar(
            time_values,
            charge_values,
            bottom=bottom_charge,
            color="#009600",
            label="Bat. Charge",
            width=line_width,
        )
        self.ax1.bar(
            time_values,
            grid_injection_values,
            bottom=bottom_injection,
            color="#4C00A4",
            label="Grid Injection",
            width=line_width,
        )
        
        self.ax1.axhline(y=0, color="k", linestyle="-", linewidth=0.1)
        self.ax1.set_ylabel("kWh")
        
        ############################################################################
        ############################################################################
        ############################################################################
        
        calculated_values_optimized = calculate_values(data_points_optimized, str(self.optionmenu_day.get()) + "-" + str(self.optionmenu_month.get()), self.optionmenu_scale.get())

        # Perform some calculations to get new data
        time_values_optimized = calculated_values_optimized["time_values"]
        pv_power_values_optimized = calculated_values_optimized["pv_power_values"]
        power_usage_values_optimized = calculated_values_optimized["power_usage_values"]
        charge_values_optimized = calculated_values_optimized["charge_values"]
        discharge_values_optimized = calculated_values_optimized["discharge_values"]
        soc_values_optimized = calculated_values_optimized["soc_values"]
        grid_injection_values_optimized = calculated_values_optimized["injection_values"]
        grid_offtake_values_optimized = calculated_values_optimized["offtake_values"]
        
        grid_injection_prices_optimized = calculated_values_optimized["grid_injection_prices"]
        grid_offtake_prices_optimized = calculated_values_optimized["grid_offtake_prices"]

        grid_injection_sum_optimized = calculated_values_optimized["grid_injection_sum"]
        grid_offtake_sum_optimized = calculated_values_optimized["grid_offtake_sum"]

        grid_injection_cost_optimized = calculated_values_optimized["grid_injection_cost"]
        grid_offtake_cost_optimized = calculated_values_optimized["grid_offtake_cost"]
        
        ev_charge_values_optimized = calculated_values_optimized["ev_charge_values"]

        # code to display in text field
        self.label_offtake_result_2.configure(text=str(round(grid_offtake_sum_optimized, 3)) + " kWh")
        self.label_injection_result_2.configure(text=str(abs(round(grid_injection_sum_optimized, 3))) + " kWh")
        self.label_charge_result_2.configure(text=str(abs(round(sum(charge_values_optimized), 3))) + " kWh")
        self.label_discharge_result_2.configure(text=str(abs(round(sum(discharge_values_optimized), 3))) + " kWh")
        self.label_pv_production_result_2.configure(text=str(abs(round(sum(pv_power_values_optimized), 3))) + " kWh")
        self.label_power_use_result_2.configure(text=str(abs(round(sum(power_usage_values_optimized), 3))) + " kWh")
        self.label_ev_charge_result_2.configure(text=str(abs(round(sum(ev_charge_values_optimized), 3))) + " kWh")
        self.label_cost_result_2.configure(text=str(round(grid_offtake_cost_optimized, 3)) + " €")
        self.label_earning_result_2.configure(text=str(abs(round(grid_injection_cost_optimized, 3))) + " €")

        # Calculate bottom values
        bottom_offtake_optimized = [x + y for x, y in zip(pv_power_values_optimized, discharge_values_optimized)]
        bottom_charge_optimized = [x + y for x, y in zip(power_usage_values_optimized, ev_charge_values_optimized)]
        bottom_injection_optimized = [x + y + z for x, y, z in zip(power_usage_values_optimized, ev_charge_values_optimized, charge_values_optimized)]

        line_width_optimized = calculated_values_optimized["line_width"]
        self.ax2.set_title(calculated_values_optimized["title"].replace('Not ', ''))
        self.ax2.set_xlabel("Time")            

        self.ax2.bar(
            time_values_optimized, 
            pv_power_values_optimized, 
            color="y", 
            label="PV Power",
            width=line_width_optimized
        )
        self.ax2.bar(
            time_values_optimized,
            discharge_values_optimized,
            bottom=pv_power_values_optimized,
            color="#FF0000",
            label="Discharge",
            width=line_width_optimized,
        )
        self.ax2.bar(
            time_values_optimized,
            grid_offtake_values_optimized,
            bottom=bottom_offtake_optimized,
            color="b",
            label="Grid Offtake",
            width=line_width_optimized,
        )

        self.ax2.bar(
            time_values_optimized, 
            power_usage_values_optimized, 
            color="c", 
            label="Power Usage",
            width=line_width_optimized
        )
        self.ax2.bar(
            time_values_optimized, 
            ev_charge_values_optimized,
            bottom=power_usage_values_optimized, 
            color="black", 
            label="Ev Charge",
            width=line_width
        )
        self.ax2.bar(
            time_values_optimized,
            charge_values_optimized,
            bottom=bottom_charge_optimized,
            color="#009600",
            label="Bat. Charge",
            width=line_width,
        )
        self.ax2.bar(
            time_values_optimized,
            grid_injection_values_optimized,
            bottom=bottom_injection_optimized,
            color="#4C00A4",
            label="Grid Injection",
            width=line_width_optimized,
        )
        
        self.ax2.axhline(y=0, color="k", linestyle="-", linewidth=0.1)
        self.ax2.set_ylabel("kWh")
          
        ############################################################################
        ############################################################################
        ############################################################################
        
        self.label_saved_result_1.configure(text=str(abs(round(abs(grid_offtake_cost)-abs(grid_injection_cost)-abs(grid_offtake_cost_optimized)+abs(grid_injection_cost_optimized), 3))) + " €")
        
        new_soc_values = scale_list(soc_values, 400)
        new_soc_values_optimized = scale_list(soc_values_optimized, 400)
        
        grid_injection_prices_scaled = scale_list(grid_injection_prices, 400)
        grid_offtake_prices_scaled = scale_list(grid_offtake_prices, 400)
        
        average_price_1 = sum(grid_offtake_prices_scaled)/400
        average_price_2 = sum(grid_offtake_prices_scaled)/400
        average_price = (average_price_1+average_price_2)/2
        
        # Plot injection and offtake prices with their y-axis on the left
        self.ax3.plot(grid_injection_prices_scaled, color="#290BE1", label="Injection Prices", linewidth=0.8)
        self.ax3.plot(grid_offtake_prices_scaled, color="r", label="Offtake Prices", linewidth=0.8)
        self.ax3.axhline(y=average_price, color="black", label="Average Price", linewidth=0.8)
        self.ax3.set_ylabel("Grid Prices per MWh")
        self.ax3.set_xlabel("Time")
        self.ax3.tick_params(axis='y', labelcolor="black")
        
        ax4 = self.ax3.twinx()
        removed = False
        
        ax4.clear()

        ax4.set_ylabel('SOC', color="g", labelpad=15) 
        ax4.yaxis.set_label_coords(1.055, 0.5)  # Adjust the position of the label
        ax4.plot(new_soc_values, color="g", linestyle=":", label="Soc", linewidth=0.8)
        ax4.plot(new_soc_values_optimized, color="g", linestyle="-.", label="Soc Optimized", linewidth=0.8)
        ax4.tick_params(axis='y', labelcolor="g")
        ax4.legend(loc='center left', bbox_to_anchor=(1.06, 0.3))
        
        if self.optionmenu_scale.get() in ["PER YEAR", "PER MONTH", "PER WEEK"]: 
            ax4.remove()
            removed = True    

        # Add legend
        self.ax3.legend(loc='center left', bbox_to_anchor=(1.06, 0.7))
        self.ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        self.ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
        # Redraw canvas
        self.canvas1.draw()
        
        if removed == False:
            ax4.remove()
        
    def update_date_options(self, event):
        selected_scale = self.optionmenu_scale.get()
        time_options = True

        if selected_scale == "SPECIFIC MONTH":
            time_options = True
        elif selected_scale == "SPECIFIC WEEK":
            time_options = True
        elif selected_scale == "SPECIFIC DAY":
            time_options = True
            # for month in range(1, 13):
            #     for day in range(1, 32):
            #         try:
            #             date = datetime.date(2023, month, day)
            #             time_options.append((date.strftime("%d-%m")))
            #         except ValueError:
            #             # Handle cases where the day is out of range for the month
            #             pass
        else: 
            time_options = False
            self.optionmenu_day.configure(fg_color="grey20", button_color="grey20", state = "disabled")
            self.optionmenu_month.configure(fg_color="grey20", button_color="grey20", state = "disabled")
            self.optionmenu_day.option_clear
            self.optionmenu_month.option_clear
            self.optionmenu_day.set("")
            self.optionmenu_month.set("")
        
        # Update the option menu for time values
        if time_options == True:
            self.optionmenu_day.configure(fg_color="#AEB74F", button_color="#9fa845", state = "normal")
            self.optionmenu_month.configure(fg_color="#AEB74F", button_color="#9fa845", state = "normal")
            self.optionmenu_day.option_clear
            self.optionmenu_month.option_clear
            self.optionmenu_day.configure(values=[str(val) for val in range(1, 32)])
            self.optionmenu_month.configure(values=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
            if self.optionmenu_day.get() not in [str(val) for val in range(1, 32)]: self.optionmenu_day.set(1)
            if self.optionmenu_month.get() not in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]: self.optionmenu_month.set("January")
        
        if self.data_available:
            self.update_graphs_with_new_data(self.data_points_complete, self.data_points_complete_optimized)
            
    def option_menu_time_event(self, event):
        if self.data_available:
            self.update_graphs_with_new_data(self.data_points_complete, self.data_points_complete_optimized)
            
    def option_menu_month_event(self, event):
        selected_month = self.optionmenu_month.get()
        days_in_month = {
            "January": 31,
            "February": 28,  # Assuming it's not a leap year
            "March": 31,
            "April": 30,
            "May": 31,
            "June": 30,
            "July": 31,
            "August": 31,
            "September": 30,
            "October": 31,
            "November": 30,
            "December": 31
        }

        # Update the option menu for days based on the selected month
        if selected_month in days_in_month:
            num_days = days_in_month[selected_month]
            day_values = [str(day) for day in range(1, num_days + 1)]
            self.optionmenu_day.configure(values=day_values)
        else:
            # Default to 31 days if the selected month is not found
            self.optionmenu_day.configure(values=[str(day) for day in range(1, 32)])
            
        if self.optionmenu_day.get() not in day_values:
            self.optionmenu_day.set(len(day_values))

        if self.data_available:
            self.update_graphs_with_new_data(self.data_points_complete, self.data_points_complete_optimized)
            
        
    def verify_parameters(self):
        try:
            self.simulation_data = self.db_manager.fetch_simulation_by_name("temp")
            
            if(self.simulation_data):
                self.battery_charge = self.simulation_data[3]
                self.battery_discharge = self.simulation_data[4]
                self.battery_capacity = self.simulation_data[5]
                self.battery_efficiency = self.simulation_data[6]
                self.solar_azimuth = self.simulation_data[8]
                self.solar_tilt = self.simulation_data[9]
                self.solar_number_of_panels = self.simulation_data[10]
                self.solar_efficiency = self.simulation_data[11]
                self.solar_length = self.simulation_data[12]
                self.solar_width = self.simulation_data[13]
                self.ev_charge = self.simulation_data[15]
                self.ev_number_of_cars = self.simulation_data[16]
                self.ev_efficiency = self.simulation_data[17]
                self.ev_distance_year = self.simulation_data[18]
                self.selected_consumer_profile = self.simulation_data[19]
                self.selected_provider = self.simulation_data[20]
                self.general_latitude = self.simulation_data[21]
                self.general_longitude = self.simulation_data[22]
                self.general_start_date = self.simulation_data[23]
                self.use_api = self.simulation_data[24]
        
        except:
            # Show some retry/cancel warnings
            msg = CTkMessagebox(title="Warning Message!", message="Please Select Simulation Parameters",
                        icon="warning", option_1="OK")
            
        self.start_process()

    def start_process(self):    
        # Initialize battery using the retrieved data
        battery_home_1 = Battery(
            capacity=self.battery_capacity,
            soc=0,
            charge_power=self.battery_charge,
            discharge_power=self.battery_discharge,
            max_soc=0.95,
            min_dod=0.05,
            efficiency=self.battery_efficiency,
        )
        
        battery_car_1 = Battery(
            capacity=40,
            soc=0,
            charge_power=self.ev_charge,
            discharge_power=15,
            max_soc=0.95,
            min_dod=0.05,
            efficiency=self.ev_efficiency,
        )
        
        battery_home_2 = Battery(
            capacity=self.battery_capacity,
            soc=0,
            charge_power=self.battery_charge,
            discharge_power=self.battery_discharge,
            max_soc=0.95,
            min_dod=0.05,
            efficiency=self.battery_efficiency,
        )
        
        battery_car_2 = Battery(
            capacity=40,
            soc=0,
            charge_power=self.ev_charge,
            discharge_power=15,
            max_soc=0.95,
            min_dod=0.05,
            efficiency=self.ev_efficiency,
        )

        # the used data_points list is formatted like this data_points = ['pv_power_value', 'time_value', 'soc_value', 'charge_value', 'grid_usage', 'power_usage_value']
        # where pv_power_value is in kWh
        # time_value is in yyyy-mm-dd
        # soc_value is in kWh
        # charge_value is in kWh and is positive when charged and negative when discharged
        # grid_usage is in kWh and is positive when extracted and is negative when injected
        
        data_points = process_solar_data(self.general_latitude, self.general_longitude, self.general_start_date, self.solar_number_of_panels, self.solar_width*self.solar_length, self.solar_azimuth, self.solar_tilt, self.solar_efficiency, self.solar_efficiency, self.use_api)

        data_points = get_power_usage_values(data_points, self.selected_consumer_profile)
        
        data_points = process_prices_data(data_points, self.general_latitude, self.general_longitude, self.general_start_date, self.selected_provider, self.use_api)
        
        data_points_optimized = copy.deepcopy(data_points)  # Make a deep copy of the original data_points list
        
        self.data_points_complete_optimized = process_data_optimized(data_points_optimized, battery_home_2, battery_car_2, self.ev_distance_year * self.ev_number_of_cars)
        
        self.data_points_complete = process_data(data_points, battery_home_1, battery_car_1, self.ev_distance_year * self.ev_number_of_cars)

        self.update_graphs_with_new_data(self.data_points_complete, self.data_points_complete_optimized)
        
        self.data_available = True
        
    def on_close(self):
        try:
            self.db_manager.delete_simulation_by_name("temp")
        except:
            pass
        self.destroy()
        
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
