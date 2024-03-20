import tkinter
import tkinter.messagebox
import customtkinter
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from battery import Battery
from process import get_power_usage_values, process_data, retrieve_data_api
from pybammBattery import PyBaMM_Battery
from solcast import get_solar_radiation_forecast
import csv
import matplotlib.dates as mdates
import datetime

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Smart Home Simulation")
        self.geometry(f"{1280}x{560}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        #self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure(0, weight=1)

        customtkinter.set_appearance_mode("Dark")

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)
        self.sidebar_frame.grid_propagate(False)  # Prevent resizing
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Simulation Params", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 5), columnspan=2)

        # Option Menu for Battery
        self.label_battery = customtkinter.CTkLabel(self.sidebar_frame, text="Battery", font=customtkinter.CTkFont(size=15))
        self.label_battery.grid(row=1, column=0, padx=5, pady=(5, 0))
        self.optionmenu_battery = customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                                        values=["Lithium-ion", "Lead-acid", "..."])
        self.optionmenu_battery.grid(row=2, column=0, padx=20, pady=(5, 5))
        self.edit_button_battery = customtkinter.CTkButton(self.sidebar_frame, text="Edit", command=self.open_input_dialog_event)
        self.edit_button_battery.grid(row=2, column=1, padx=5, pady=(5, 5))

        # Option Menu for SolarPanel
        self.label_solar_panel = customtkinter.CTkLabel(self.sidebar_frame, text="Solar Panel", font=customtkinter.CTkFont(size=15))
        self.label_solar_panel.grid(row=3, column=0, padx=5, pady=(5, 0))
        self.optionmenu_solar_panel = customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                                        values=["Monocrystalline", "Polycrystalline", "PERC", "Thin film", "..."])
        self.optionmenu_solar_panel.grid(row=4, column=0, padx=20, pady=(5, 5))
        self.edit_button_solar_panel = customtkinter.CTkButton(self.sidebar_frame, text="Edit", command=self.open_input_dialog_event)
        self.edit_button_solar_panel.grid(row=4, column=1, padx=5, pady=(5, 5))

        # Option Menu for EVCharger
        self.label_ev_charger = customtkinter.CTkLabel(self.sidebar_frame, text="EV Charger", font=customtkinter.CTkFont(size=15))
        self.label_ev_charger.grid(row=5, column=0, padx=5, pady=(5, 0))
        self.optionmenu_ev_charger = customtkinter.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                                        values=["Type 1", "Type 2", "Type 3"])
        self.optionmenu_ev_charger.grid(row=6, column=0, padx=20, pady=(5, 40))
        self.edit_button_ev_charger = customtkinter.CTkButton(self.sidebar_frame, text="Edit", command=self.open_input_dialog_event)
        self.edit_button_ev_charger.grid(row=6, column=1, padx=5, pady=(5, 40))

        # create main entry and button
        self.entry_field1 = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Start date")
        self.entry_field1.grid(row=7, column=0, padx=20, pady=(5, 40))

        self.entry_field2 = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="End date")
        self.entry_field2.grid(row=7, column=1, padx=20, pady=(5, 40))


        #self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="battery", command=self.sidebar_button_event)
        #self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Start Sim.", command=lambda: self.start_process("50.9254992", "5.3932811", "16/03/2018", "16/04/2018"))
        self.sidebar_button_2.grid(row=8, column=0, padx=20, pady=10, columnspan=2)

        #self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))

        # set default values
        customtkinter.set_appearance_mode("Dark")
        #self.optionmenu_1.set("Battery")

        # create Matplotlib graphs
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(8, 6))
        self.canvas1 = FigureCanvasTkAgg(self.fig, master=self)
        plt.subplots_adjust(wspace=0.5, hspace=0.5)
        self.ax1.set_title('PV Production')
        self.ax2.set_title('Home Power Usage')
        self.ax3.set_title('Battery Charge')
        self.ax4.set_title('Grid Usage')
        
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('PV Production (kW)')

        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('Power (kW)')

        self.ax3.set_xlabel('Time')
        self.ax3.set_ylabel('Charge (kWh)')

        self.ax4.set_xlabel('Time')
        self.ax4.set_ylabel('Energy (kWh)')
        self.canvas1.get_tk_widget().grid(row=0, column=1, rowspan=10, padx=(40, 40), pady=(40, 40))


        # create sidebar frame with widgets
        self.sidebar_frame2 = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame2.grid(row=0, column=2, sticky="nsew")
        self.sidebar_frame2.grid_rowconfigure(10, weight=1)
        self.logo_label2 = customtkinter.CTkLabel(self.sidebar_frame2, text="Sim Results", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label2.grid(row=0, column=0, padx=20, pady=(20, 5), columnspan=2)

        self.label_result1 = customtkinter.CTkLabel(self.sidebar_frame2, text="Grid Extraction:", font=customtkinter.CTkFont(size=15))
        self.label_result1.grid(row=1, column=0, padx=5, pady=(5, 0))
        self.label_result1 = customtkinter.CTkLabel(self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=15))
        self.label_result1.grid(row=1, column=1, padx=(5,15), pady=(5, 0))

        self.label_result2 = customtkinter.CTkLabel(self.sidebar_frame2, text="Grid Injection:", font=customtkinter.CTkFont(size=15))
        self.label_result2.grid(row=2, column=0, padx=5, pady=(5, 0))
        self.label_result2 = customtkinter.CTkLabel(self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=15))
        self.label_result2.grid(row=2, column=1, padx=(5,15), pady=(5, 0))

        self.label_result3 = customtkinter.CTkLabel(self.sidebar_frame2, text="Total Cost:", font=customtkinter.CTkFont(size=15))
        self.label_result3.grid(row=3, column=0, padx=5, pady=(5, 0))
        self.label_result3 = customtkinter.CTkLabel(self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=15))
        self.label_result3.grid(row=3, column=1, padx=(5,15), pady=(5, 0))

        self.label_result4 = customtkinter.CTkLabel(self.sidebar_frame2, text="Total Earning:", font=customtkinter.CTkFont(size=15))
        self.label_result4.grid(row=4, column=0, padx=5, pady=(5, 0))
        self.label_result4 = customtkinter.CTkLabel(self.sidebar_frame2, text="...", font=customtkinter.CTkFont(size=15))
        self.label_result4.grid(row=4, column=1, padx=(5,15), pady=(5, 0))


    def update_graphs_with_new_data(self, data_points):
        # Perform some calculations to get new data
        time_values = [point['time_value'] for point in data_points]
        pv_power_values = [point['pv_power_value'] for point in data_points]
        power_usage_values = [point['power_usage_value'] for point in data_points]
        charge_values = [point['charge_value'] for point in data_points]
        residue_energy_values = [point['residue_energy'] for point in data_points]

        # Calculate sum of positive and negative residue values
        grid_injection_sum = sum(value for value in residue_energy_values if value > 0)
        grid_extraction_sum = sum(value for value in residue_energy_values if value < 0)

        # Calculate cost for grid injection and grid extraction assuming energy cost of 0.1 euro per kWh
        grid_injection_cost = grid_injection_sum * 0.035
        grid_extraction_cost = grid_extraction_sum * -0.1211

        #code to display in text field
        self.label_result1.configure(text=str(round(grid_extraction_sum, 4)) + " kWh")
        self.label_result2.configure(text=str(round(grid_injection_sum, 4)) + " kWh")
        self.label_result3.configure(text=str(round(grid_extraction_cost, 4)) + " €")
        self.label_result4.configure(text=str(round(grid_injection_cost, 4)) + " €")

        # For example, let's generate new random data for each graph
        import numpy as np
        new_y1 = pv_power_values
        new_y2 = power_usage_values
        new_y3 = charge_values
        new_y4 = residue_energy_values

        # Clear existing plots
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()

        # Plot new data
        self.ax1.plot(time_values, new_y1)
        self.ax1.set_title('PV Production')

        self.ax2.plot(time_values, new_y2)
        self.ax2.set_title('Home Power Usage')

        self.ax3.plot(time_values, new_y3)
        self.ax3.set_title('Battery Charge')

        self.ax4.plot(time_values, new_y4)
        self.ax4.set_title('Grid Usage')

        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('PV Production (kW)')

        self.ax2.set_xlabel('Time')
        self.ax2.set_ylabel('Power (kW)')

        self.ax3.set_xlabel('Time')
        self.ax3.set_ylabel('Charge (kWh)')

        self.ax4.set_xlabel('Time')
        self.ax4.set_ylabel('Energy (kWh)')

        # Filter time values to display only every 6 hours
        filtered_time_values = [time_values[i] for i in range(len(time_values)) if i % 12 == 0]
        self.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Format to display only hour and minute
        self.ax1.set_xticks(filtered_time_values)
        self.ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Format to display only hour and minute
        self.ax2.set_xticks(filtered_time_values)
        self.ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Format to display only hour and minute
        self.ax3.set_xticks(filtered_time_values)
        self.ax4.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # Format to display only hour and minute
        self.ax4.set_xticks(filtered_time_values)

        # Adjust layout to add space between subplots
        plt.subplots_adjust(wspace=0.5, hspace=0.5)

        # Redraw canvas
        self.canvas1.draw()

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print('"sidebar button')
    
    def start_process(self, latitude, longitude, start_date, end_date):
        
        battery = Battery(capacity=2, soc=2, charge_power=5.0, discharge_power=5.0, max_soc=0.95, min_dod=0.05, efficiency=0.90)
        pybamm_battery = PyBaMM_Battery(capacity=2, soc=2, charge_power=5.0, discharge_power=5.0, max_soc=0.95, min_dod=0.05, efficiency=0.90)

        data_points = retrieve_data_api(latitude, longitude, start_date, end_date)

        data_points = get_power_usage_values(data_points)

        data_points = process_data(data_points, battery, pybamm_battery)

        #time_values, new_charge_values = calculate_new_values(time_values, charge_values, daily_average_usage)

        self.update_graphs_with_new_data(data_points)

if __name__ == "__main__":
    app = App()
    app.mainloop()