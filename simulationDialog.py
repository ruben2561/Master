import datetime
from dateutil import parser
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
from CTkMessagebox import CTkMessagebox

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
            self.frame_3,
            command=self.update_simulation_options,
            dynamic_resizing=False
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
        
        self.label_battery_efficiency = customtkinter.CTkLabel(
            self.frame_3,
            text="efficiency (%)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_battery_efficiency.grid(row=4, column=1, padx=30, pady=(0,20), sticky='w')
        self.entry_battery_efficiency = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_battery_efficiency.grid(row=4, column=2, pady=(0,20), padx=(0,25))
        
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
        
        self.label_solar_efficiency = customtkinter.CTkLabel(
            self.frame_3,
            text="efficiency (%)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_solar_efficiency.grid(row=8, column=1, padx=30, pady=(0,0), sticky='w')
        self.entry_solar_efficiency = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_solar_efficiency.grid(row=8, column=2, pady=(0,0), padx=(0,25))
        
        #########################
        
        self.label_solar_length = customtkinter.CTkLabel(
            self.frame_3,
            text="Length (m)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_solar_length.grid(row=9, column=1, padx=30, pady=(0,0), sticky='w')
        self.entry_solar_length = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_solar_length.grid(row=9, column=2, pady=(0,0), padx=(0,25))
        
        #########################
        
        self.label_solar_width = customtkinter.CTkLabel(
            self.frame_3,
            text="Width (m)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_solar_width.grid(row=10, column=1, padx=(30,0), pady=(0,20), sticky='w')
        self.entry_solar_width = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_solar_width.grid(row=10, column=2, pady=(0,20), padx=(0,25))
        
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
            command=self.update_ev_options,
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
        
        self.label_ev_efficiency = customtkinter.CTkLabel(
            self.frame_3,
            text="efficiency (%)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_ev_efficiency.grid(row=13, column=1, padx=30, pady=(0,0), sticky='w')
        self.entry_ev_efficiency = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_ev_efficiency.grid(row=13, column=2, pady=(0,0), padx=(0,25))
        
        #########################
        
        self.label_ev_capacity_car = customtkinter.CTkLabel(
            self.frame_3,
            text="Capacity Car (kWh)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_ev_capacity_car.grid(row=14, column=1, padx=30, pady=(0,20), sticky='w')
        self.entry_ev_capacity_car = customtkinter.CTkEntry(
            self.frame_3,
        )
        self.entry_ev_capacity_car.grid(row=14, column=2, pady=(0,20), padx=(0,25))
        
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
        self.label_consumer_profile.grid(row=15, column=0, padx=25, pady=(0,20), sticky="w")
        
        self.optionmenu_consumer_profile = customtkinter.CTkOptionMenu(
            self.frame_3,
        )
        self.optionmenu_consumer_profile.grid(
            row=15, column=2, pady=(0,20), padx=(0,25)
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
        
        self.button_confirm = customtkinter.CTkButton(
            self.frame_3,
            text="Confirm",
            command=self.confirm_parameters,
        )
        self.button_confirm.grid(row=19, column=1, pady=(0,25), sticky='e')
        
        self.button_confirm_save = customtkinter.CTkButton(
            self.frame_3,
            text="Confirm And Save",
            command=self.confirm_save_parameters,
        )
        self.button_confirm_save.grid(row=19, column=2, pady=(0,25), sticky='w')
        
        self.checkbox_testing = customtkinter.CTkCheckBox(self.frame_3, text="Use API's", onvalue="on", offvalue="off")
        self.checkbox_testing.grid(row=19, column=0, pady=(0,25))

        
        self.populate_simulation_options()
        self.populate_battery_options()
        self.populate_solarpanel_options()
        self.populate_ev_options()
        self.populate_consumer_profile_options()
        
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    
    def update_simulation_options(self, selected_simulation):
        
        selected_simulation = self.optionmenu_simulation.get()
        selected_simulation_data = self.db_manager.fetch_simulation_by_name(selected_simulation)
        
        self.entry_battery_charge.delete(0, tkinter.END)
        self.entry_battery_discharge.delete(0, tkinter.END)
        self.entry_battery_capacity.delete(0, tkinter.END)
        self.entry_battery_efficiency.delete(0, tkinter.END)
        self.entry_solar_azimuth.delete(0, tkinter.END)
        self.entry_solar_tilt.delete(0, tkinter.END)
        self.entry_solar_number_of_panels.delete(0, tkinter.END)
        self.entry_solar_efficiency.delete(0, tkinter.END)
        self.entry_solar_length.delete(0, tkinter.END)
        self.entry_solar_width.delete(0, tkinter.END)
        self.entry_ev_charge.delete(0, tkinter.END)
        self.entry_ev_fast_charge.delete(0, tkinter.END)
        self.entry_ev_efficiency.delete(0, tkinter.END)
        self.entry_ev_capacity_car.delete(0, tkinter.END)
        self.entry_general_latitude.delete(0, tkinter.END)
        self.entry_general_longitude.delete(0, tkinter.END)
        self.entry_general_start_date.delete(0, tkinter.END)
        
        self.entry_battery_charge.insert(0, selected_simulation_data[2])
        self.entry_battery_discharge.insert(0, selected_simulation_data[3])
        self.entry_battery_capacity.insert(0, selected_simulation_data[4])
        self.entry_battery_efficiency.insert(0, selected_simulation_data[5])
        self.entry_solar_azimuth.insert(0, selected_simulation_data[6])
        self.entry_solar_tilt.insert(0, selected_simulation_data[7])
        self.entry_solar_number_of_panels.insert(0, selected_simulation_data[8])
        self.entry_solar_efficiency.insert(0, selected_simulation_data[9])
        self.entry_solar_length.insert(0, selected_simulation_data[10])
        self.entry_solar_width.insert(0, selected_simulation_data[11])
        self.entry_ev_charge.insert(0, selected_simulation_data[12])
        self.entry_ev_fast_charge.insert(0, selected_simulation_data[13])
        self.entry_ev_efficiency.insert(0, selected_simulation_data[14])
        self.entry_ev_capacity_car.insert(0, selected_simulation_data[15])
        self.optionmenu_consumer_profile.set(selected_simulation_data[16])
        self.entry_general_latitude.insert(0, selected_simulation_data[17])
        self.entry_general_longitude.insert(0, selected_simulation_data[18])
        self.entry_general_start_date.insert(0, selected_simulation_data[19])
        #TODO fix this from database
        #self.checkbox_testing.
        
    def update_battery_options(self, selected_battery):
        
        selected_battery = self.optionmenu_battery.get()
        selected_battery_data = self.db_manager.fetch_battery_by_name(selected_battery)
        
        self.entry_battery_charge.delete(0, tkinter.END)
        self.entry_battery_discharge.delete(0, tkinter.END)
        self.entry_battery_capacity.delete(0, tkinter.END)
        self.entry_battery_efficiency.delete(0, tkinter.END)
        
        self.entry_battery_charge.insert(0, selected_battery_data[3])
        self.entry_battery_discharge.insert(0, selected_battery_data[4])
        self.entry_battery_capacity.insert(0, selected_battery_data[2])
        self.entry_battery_efficiency.insert(0, selected_battery_data[7])
        
    def update_solarpanel_options(self, selected_solarpanel):
        
        selected_solarpanel = self.optionmenu_solar_panel.get()
        selected_solarpanel_data = self.db_manager.fetch_solarpanel_by_name(selected_solarpanel)
        
        self.entry_solar_azimuth.delete(0, tkinter.END)
        self.entry_solar_tilt.delete(0, tkinter.END)
        self.entry_solar_efficiency.delete(0, tkinter.END)
        self.entry_solar_number_of_panels.delete(0, tkinter.END)
        self.entry_solar_length.delete(0, tkinter.END)
        self.entry_solar_width.delete(0, tkinter.END)
        
        self.entry_solar_azimuth.insert(0, selected_solarpanel_data[2])
        self.entry_solar_tilt.insert(0, selected_solarpanel_data[3])
        self.entry_solar_efficiency.insert(0, selected_solarpanel_data[7])
        self.entry_solar_number_of_panels.insert(0, selected_solarpanel_data[4])
        self.entry_solar_length.insert(0, selected_solarpanel_data[5])
        self.entry_solar_width.insert(0, selected_solarpanel_data[6])
        
    def update_ev_options(self, selected_ev):
        
        selected_ev = self.optionmenu_ev_charger.get()
        selected_ev_data = self.db_manager.fetch_ev_charger_by_name(selected_ev)
        
        self.entry_ev_charge.delete(0, tkinter.END)
        self.entry_ev_fast_charge.delete(0, tkinter.END)
        self.entry_ev_efficiency.delete(0, tkinter.END)
        self.entry_ev_capacity_car.delete(0, tkinter.END)
        
        self.entry_ev_charge.insert(0, selected_ev_data[2])
        self.entry_ev_fast_charge.insert(0, selected_ev_data[3])
        self.entry_ev_efficiency.insert(0, selected_ev_data[4])
        self.entry_ev_capacity_car.insert(0, selected_ev_data[5])
        
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################

    def populate_simulation_options(self):
        # Fetch simulation data from the database
        simulation_data = self.db_manager.fetch_simulation_data()
        # Extract simulation names
        simulation_options = [simulation[1] for simulation in simulation_data]
        # Update option menu with simulation names
        self.optionmenu_simulation.option_clear
        self.optionmenu_simulation.configure(values=simulation_options)
        self.optionmenu_simulation.set("Load Simulation")

    # TODO this doesnt work yet
    def populate_battery_options(self):
        # Fetch battery data from the database
        battery_data = self.db_manager.fetch_battery_data()
        # Extract battery names
        battery_options = [battery[1] for battery in battery_data]
        # Update option menu with battery names
        self.optionmenu_battery.option_clear
        self.optionmenu_battery.configure(values=battery_options)
        self.optionmenu_battery.set("Load Battery")
        
    def populate_solarpanel_options(self):
        # Fetch battery data from the database
        solarpanel_data = self.db_manager.fetch_solarpanel_data()
        # Extract battery names
        solarpanel_options = [solarpanel[1] for solarpanel in solarpanel_data]
        # Update option menu with battery names
        self.optionmenu_solar_panel.option_clear
        self.optionmenu_solar_panel.configure(values=solarpanel_options)
        self.optionmenu_solar_panel.set("Load Solar Panel")
        
    def populate_ev_options(self):
        # Fetch battery data from the database
        ev_data = self.db_manager.fetch_ev_charger_data()
        # Extract battery names
        ev_options = [ev[1] for ev in ev_data]
        # Update option menu with battery names
        self.optionmenu_ev_charger.option_clear
        self.optionmenu_ev_charger.configure(values=ev_options)
        self.optionmenu_ev_charger.set("Load Ev Charger")
        
    def populate_consumer_profile_options(self):
            current_directory = os.getcwd()
            folder_name = 'consumptionProfile'
            folder_path = os.path.join(current_directory, folder_name)
            file_names = os.listdir(folder_path)
            file_names = [name.replace('profile_', '') for name in file_names]
            file_names = [name.replace('.csv', '') for name in file_names]
            file_names = [name.replace('_', ', ') for name in file_names]
            
            self.optionmenu_consumer_profile.option_clear
            self.optionmenu_consumer_profile.configure(values=file_names)
            self.optionmenu_consumer_profile.set("Load Consumer Profile")
        
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################

    def edit_battery(self):
        edit_dialog = BatteryManager(
            self.db_manager, callback=self.populate_battery_options
        )
        self.populate_battery_options()
        
    def standardize_date(self, date_input):
        try:
            # Parse the date from the given date string
            parsed_date = parser.parse(date_input)
            # Format the date to YYYY-MM-DD
            standardized_date = parsed_date.strftime('%Y-%m-%d')
            return standardized_date
        except ValueError:
            return "Invalid date"
        
        
    def confirm_save_parameters(self):
        # Collect all entries
        entries = {
            "Battery Charge": self.entry_battery_charge.get(),
            "Battery Discharge": self.entry_battery_discharge.get(),
            "Battery Capacity": self.entry_battery_capacity.get(),
            "Battery Efficiency": self.entry_battery_efficiency.get(),
            "Solar Azimuth": self.entry_solar_azimuth.get(),
            "Solar Tilt": self.entry_solar_tilt.get(),
            "Number of Solar Panels": self.entry_solar_number_of_panels.get(),
            "Solar Efficiency": self.entry_solar_efficiency.get(),
            "Solar Length": self.entry_solar_length.get(),
            "Solar Width": self.entry_solar_width.get(),
            "EV Charge": self.entry_ev_charge.get(),
            "EV Fast Charge": self.entry_ev_fast_charge.get(),
            "EV Efficiency": self.entry_ev_efficiency.get(),
            "EV Car Capacity": self.entry_ev_capacity_car.get(),
            "Consumer Profile": self.optionmenu_consumer_profile.get().replace(', ', '_'),
            "Latitude": self.entry_general_latitude.get(),
            "Longitude": self.entry_general_longitude.get(),
            "Start Date": self.standardize_date(self.entry_general_start_date.get()),
            "Use Api": self.checkbox_testing.get()
        }

        # Check for empty fields
        empty_fields = [key for key, value in entries.items() if not value.strip()]

        #TODO fixen dat ook consumer en datum checkt
        if empty_fields:
            # Show a warning with the fields that are empty
            warning_message = "Please fill in the following fields: " + ", ".join(empty_fields)
            CTkMessagebox(title="Warning", message=warning_message)
            return  # Stop further processing
        
        dialog = customtkinter.CTkInputDialog(text="Choose a name:", title="Name")

        # If all fields are filled, continue with the operation
        self.db_manager.add_simulation(
            "temp", *entries.values()
        )
        self.db_manager.add_simulation(
            str(dialog.get_input()), *entries.values()
        )
        
        self.destroy()
        return

    def confirm_parameters(self):
        # Collect all entries
        entries = {
            "Battery Charge": self.entry_battery_charge.get(),
            "Battery Discharge": self.entry_battery_discharge.get(),
            "Battery Capacity": self.entry_battery_capacity.get(),
            "Battery Efficiency": self.entry_battery_efficiency.get(),
            "Solar Azimuth": self.entry_solar_azimuth.get(),
            "Solar Tilt": self.entry_solar_tilt.get(),
            "Number of Solar Panels": self.entry_solar_number_of_panels.get(),
            "Solar Efficiency": self.entry_solar_efficiency.get(),
            "Solar Length": self.entry_solar_length.get(),
            "Solar Width": self.entry_solar_width.get(),
            "EV Charge": self.entry_ev_charge.get(),
            "EV Fast Charge": self.entry_ev_fast_charge.get(),
            "EV Efficiency": self.entry_ev_efficiency.get(),
            "EV Car Capacity": self.entry_ev_capacity_car.get(),
            "Consumer Profile": self.optionmenu_consumer_profile.get().replace(', ', '_'),
            "Latitude": self.entry_general_latitude.get(),
            "Longitude": self.entry_general_longitude.get(),
            "Start Date": self.standardize_date(self.entry_general_start_date.get()),
            "Use Api": self.checkbox_testing.get()
        }

        # Check for empty fields
        empty_fields = [key for key, value in entries.items() if not value.strip()]

        #TODO fixen dat ook consumer en datum checkt
        if empty_fields:
            # Show a warning with the fields that are empty
            warning_message = "Please fill in the following fields: " + ", ".join(empty_fields)
            CTkMessagebox(title="Warning", message=warning_message)
            return  # Stop further processing

        # If all fields are filled, continue with the operation
        self.db_manager.add_simulation(
            "temp", *entries.values()
        )
        
        self.destroy()
        return



