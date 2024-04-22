import datetime
import os
import tkinter
import customtkinter
from CTkListbox import *
import tkinter
import customtkinter
from batteryCreateDialog import batteryCreateDialog
from batteryManager import BatteryManager
from databaseManager import DatabaseManager
from batteryEditDialog import batteryEditDialog

class SimulationDialog(customtkinter.CTk):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager

        self.title("Simulation Manager")

        self.frame_3 = customtkinter.CTkFrame(master=self)
        self.frame_3.pack(fill="both", expand=True)
        
        ###########################################################################
        ###########################################################################
        ###########################################################################

        self.logo_label = customtkinter.CTkLabel(
            self.frame_3,
            text="Load Simulation",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=25, pady=(25, 30), sticky="w")
        
        self.optionmenu_simulation = customtkinter.CTkOptionMenu(
            self.frame_3, dynamic_resizing=False
        )
        self.optionmenu_simulation.grid(row=0, column=2, padx=(0,25), pady=(25,30))
        
        ###########################################################################
        ###########################################################################
        ###########################################################################

        # Option Menu for Battery
        self.label_battery = customtkinter.CTkLabel(
            self.frame_3, text="Battery", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_battery.grid(row=1, column=0, padx=25, pady=(0,0), sticky="w")
        self.optionmenu_battery = customtkinter.CTkOptionMenu(
            self.frame_3, dynamic_resizing=False, command=self.update_battery_options
        )
        self.optionmenu_battery.grid(row=2, column=0, padx=25, pady=(0,0), sticky="w")
        
        self.edit_button_battery = customtkinter.CTkButton(
            self.frame_3, width=60, text="Edit", command=self.edit_battery
        )
        self.edit_button_battery.grid(row=3, column=0, padx=25, pady=(0,0), sticky="w")
        self.populate_battery_options()
        
        #########################
        
        self.label_battery_charge = customtkinter.CTkLabel(
            self.frame_3,
            text="Max Charge (kW)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_battery_charge.grid(row=1, column=1, padx=30, pady=(0,0), sticky='w')
        self.entry_battery_charge = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_battery_charge.grid(row=1, column=2, pady=(0,0), padx=(0,25))
        
        #########################
        
        self.label_battery_discharge = customtkinter.CTkLabel(
            self.frame_3,
            text="Max Discharge (kW)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_battery_discharge.grid(row=2, column=1, padx=30, pady=(0,0), sticky='w')
        self.entry_battery_discharge = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_battery_discharge.grid(row=2, column=2, pady=(0,0), padx=(0,25))
        
        #########################
        
        self.label_battery_capacity = customtkinter.CTkLabel(
            self.frame_3,
            text="Capacity (kWh)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_battery_capacity.grid(row=3, column=1, padx=30, pady=(0,0), sticky='w')
        self.entry_battery_capacity = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_battery_capacity.grid(row=3, column=2, pady=(0,0), padx=(0,25))
        
        #########################
        
        self.label_battery_efficienty = customtkinter.CTkLabel(
            self.frame_3,
            text="Efficienty (%)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_battery_efficienty.grid(row=4, column=1, padx=30, pady=(0, 30), sticky='w')
        self.entry_battery_efficienty = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_battery_efficienty.grid(row=4, column=2, pady=(0, 30), padx=(0,25))
        
        ###########################################################################
        ###########################################################################
        ###########################################################################

        # Option Menu for SolarPanel
        self.label_solar_panel = customtkinter.CTkLabel(
            self.frame_3, text="Solar Panel", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_solar_panel.grid(row=5, column=0, padx=25, pady=(0,0), sticky="w")
        self.optionmenu_solar_panel = customtkinter.CTkOptionMenu(
            self.frame_3,
            dynamic_resizing=False,
            command=self.update_solarpanel_options,
        )
        self.optionmenu_solar_panel.grid(row=6, column=0, padx=25, pady=(0,0), sticky="w")
        self.edit_button_solar_panel = customtkinter.CTkButton(
            self.frame_3, width=60, text="Edit", command=self.edit_battery
        )
        self.edit_button_solar_panel.grid(row=7, column=0, padx=25, pady=(0,0), sticky="w")
        self.populate_solarpanel_options()
        
        #########################
        
        self.label_solar_azimuth = customtkinter.CTkLabel(
            self.frame_3,
            text="Azimuth (°)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_solar_azimuth.grid(row=5, column=1, padx=30, pady=(0,0), sticky='w')
        self.entry_solar_azimuth = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_solar_azimuth.grid(row=5, column=2, pady=(0,0), padx=(0,25))
        
        #########################
        
        self.label_solar_tilt = customtkinter.CTkLabel(
            self.frame_3,
            text="Tilt (°)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_solar_tilt.grid(row=6, column=1, padx=30, pady=(0,0), sticky='w')
        self.entry_solar_tilt = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_solar_tilt.grid(row=6, column=2, pady=(0,0), padx=(0,25))
        
        #########################
        
        self.label_solar_number_of_panels = customtkinter.CTkLabel(
            self.frame_3,
            text="Number Of Panels",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_solar_number_of_panels.grid(row=7, column=1, padx=30, pady=(0,0), sticky='w')
        self.entry_solar_number_of_panels = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_solar_number_of_panels.grid(row=7, column=2, pady=(0,0), padx=(0,25))
        
        #########################
        
        self.label_solar_efficienty = customtkinter.CTkLabel(
            self.frame_3,
            text="Efficienty (%)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_solar_efficienty.grid(row=8, column=1, padx=30, pady=(0,0), sticky='w')
        self.entry_solar_efficienty = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_solar_efficienty.grid(row=8, column=2, pady=(0,0), padx=(0,25))
        
        #########################
        
        self.label_solar_lenght = customtkinter.CTkLabel(
            self.frame_3,
            text="Lenght (m)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_solar_lenght.grid(row=9, column=1, padx=30, pady=(0,0), sticky='w')
        self.entry_solar_lenght = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_solar_lenght.grid(row=9, column=2, pady=(0,0), padx=(0,25))
        
        #########################
        
        self.label_solar_width = customtkinter.CTkLabel(
            self.frame_3,
            text="Width (m)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_solar_width.grid(row=10, column=1, padx=(30,0), pady=(0, 30), sticky='w')
        self.entry_solar_width = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_solar_width.grid(row=10, column=2, pady=(0, 30), padx=(0,25))
        
        ###########################################################################
        ###########################################################################
        ###########################################################################

        # Option Menu for EVCharger
        self.label_ev_charger = customtkinter.CTkLabel(
            self.frame_3, text="EV Charger", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_ev_charger.grid(row=11, column=0, padx=25, pady=(0,0), sticky="w")
        self.optionmenu_ev_charger = customtkinter.CTkOptionMenu(
            self.frame_3,
            dynamic_resizing=False,
            values=["Type 1", "Type 2", "Type 3"],
        )
        self.optionmenu_ev_charger.grid(row=12, column=0, padx=25, pady=(0,0), sticky="w")
        self.edit_button_ev_charger = customtkinter.CTkButton(
            self.frame_3, width=60, text="Edit", command=self.edit_battery
        )
        self.edit_button_ev_charger.grid(row=13, column=0, padx=25, pady=(0,0), sticky="w")
        
        #########################
        
        self.label_ev_charge = customtkinter.CTkLabel(
            self.frame_3,
            text="Max Charge (kW)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_ev_charge.grid(row=11, column=1, padx=30, pady=(0,0), sticky='w')
        self.entry_ev_charge = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_ev_charge.grid(row=11, column=2, pady=(0,0), padx=(0,25))
        
        #########################
        
        self.label_ev_fast_charge = customtkinter.CTkLabel(
            self.frame_3,
            text="Max Fast Charge (kW)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_ev_fast_charge.grid(row=12, column=1, padx=30, pady=(0,0), sticky='w')
        self.entry_ev_fast_charge = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_ev_fast_charge.grid(row=12, column=2, pady=(0,0), padx=(0,25))
        
        #########################
        
        self.label_ev_efficienty = customtkinter.CTkLabel(
            self.frame_3,
            text="Efficienty (%)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_ev_efficienty.grid(row=13, column=1, padx=30, pady=(0,0), sticky='w')
        self.entry_ev_efficienty = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_ev_efficienty.grid(row=13, column=2, pady=(0,0), padx=(0,25))
        
        #########################
        
        self.label_ev_capacity_car = customtkinter.CTkLabel(
            self.frame_3,
            text="Capacity Car (kWh)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_ev_capacity_car.grid(row=14, column=1, padx=30, pady=(0,30), sticky='w')
        self.entry_ev_capacity_car = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_ev_capacity_car.grid(row=14, column=2, pady=(0,30), padx=(0,25))
        
        ###########################################################################
        ###########################################################################
        ###########################################################################
        
        current_directory = os.getcwd()
        folder_name = 'consumptionProfile'
        folder_path = os.path.join(current_directory, folder_name)
        file_names = os.listdir(folder_path)
        file_names = [name.replace('profile_', '') for name in file_names]
        file_names = [name.replace('.csv', '') for name in file_names]
        file_names = [name.replace('_', ', ') for name in file_names]

        # Option Menu for consumer profiles
        self.label_consumer_profile = customtkinter.CTkLabel(
            self.frame_3, text="Consumer Profile", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_consumer_profile.grid(row=15, column=0, padx=25, pady=(0,30), sticky="w")
        
        self.optionmenu_consumer_profile = customtkinter.CTkOptionMenu(
            self.frame_3,
        )
        self.optionmenu_consumer_profile.grid(
            row=15, column=2, pady=(0, 30), padx=(0,25)
        )
        
        ###########################################################################
        ###########################################################################
        ###########################################################################
        
        # Option Menu for General values
        self.label_general = customtkinter.CTkLabel(
            self.frame_3, text="General", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_general.grid(row=16, column=0, padx=25, pady=(0,0), sticky="w")

        ########################
        
        self.label_general_latitude = customtkinter.CTkLabel(
            self.frame_3,
            text="Latitude",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_general_latitude.grid(row=16, column=1, padx=30, pady=(0,0), sticky='w')
        self.entry_general_latitude = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_general_latitude.grid(row=16, column=2, pady=(0,0), padx=(0,25))
        
        ########################
        
        self.label_general_longitude = customtkinter.CTkLabel(
            self.frame_3,
            text="Longitude",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_general_longitude.grid(row=17, column=1, padx=30, pady=(0,0), sticky='w')
        self.entry_general_longitude = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_general_longitude.grid(row=17, column=2, pady=(0,0), padx=(0,25))
        
        ########################
        
        self.label_general_start_date = customtkinter.CTkLabel(
            self.frame_3,
            text="Start Date",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_general_start_date.grid(row=18, column=1, padx=30, pady=(0, 25), sticky='w')
        self.entry_general_start_date = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_general_start_date.grid(row=18, column=2, pady=(0, 25), padx=(0,25))
        
        ###########################################################################
        ###########################################################################
        ###########################################################################

        self.mainloop()

    def update_battery_options(self, selected_battery):
        
        selected_battery = self.optionmenu_battery.get()
        selected_battery_data = self.db_manager.fetch_battery_by_name(selected_battery)
        
        self.entry_battery_charge.delete(0, tkinter.END)
        self.entry_battery_discharge.delete(0, tkinter.END)
        self.entry_battery_capacity.delete(0, tkinter.END)
        self.entry_battery_efficienty.delete(0, tkinter.END)
        
        self.entry_battery_charge.insert(0, selected_battery_data[3])
        self.entry_battery_discharge.insert(0, selected_battery_data[4])
        self.entry_battery_capacity.insert(0, selected_battery_data[2])
        self.entry_battery_efficienty.insert(0, selected_battery_data[7])
        
    def update_solarpanel_options(self, selected_solarpanel):
        
        selected_solarpanel = self.optionmenu_solar_panel.get()
        selected_solarpanel_data = self.db_manager.fetch_solarpanel_by_name(selected_solarpanel)
        
        self.entry_solar_azimuth.delete(0, tkinter.END)
        self.entry_solar_tilt.delete(0, tkinter.END)
        self.entry_solar_efficienty.delete(0, tkinter.END)
        self.entry_solar_lenght.delete(0, tkinter.END)
        self.entry_solar_width.delete(0, tkinter.END)
        
        self.entry_solar_azimuth.insert(0, selected_solarpanel_data[2])
        self.entry_solar_tilt.insert(0, selected_solarpanel_data[3])
        self.entry_solar_efficienty.insert(0, selected_solarpanel_data[6])
        self.entry_solar_lenght.insert(0, selected_solarpanel_data[4])
        self.entry_solar_width.insert(0, selected_solarpanel_data[5])

    # TODO this doesnt work yet
    def populate_battery_options(self):
        # Fetch battery data from the database
        battery_data = self.db_manager.fetch_battery_data()
        # Extract battery names
        battery_options = [battery[1] for battery in battery_data]
        # Update option menu with battery names
        self.optionmenu_battery.option_clear
        self.optionmenu_battery.configure(values=battery_options)
        self.optionmenu_battery.set(" ")
        
    def populate_solarpanel_options(self):
        # Fetch battery data from the database
        solarpanel_data = self.db_manager.fetch_solarpanel_data()
        # Extract battery names
        solarpanel_options = [solarpanel[1] for solarpanel in solarpanel_data]
        # Update option menu with battery names
        self.optionmenu_solar_panel.option_clear
        self.optionmenu_solar_panel.configure(values=solarpanel_options)
        self.optionmenu_solar_panel.set(" ")

    def edit_battery(self):
        edit_dialog = BatteryManager(
            self.db_manager, callback=self.populate_battery_options
        )
        self.populate_battery_options()



