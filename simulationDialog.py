import datetime
from dateutil import parser
import os
import tkinter
import customtkinter
from CTkListbox import *
import tkinter
import customtkinter
from databaseManager import DatabaseManager
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

        # self.logo_label = customtkinter.CTkLabel(
        #     self.frame_3,
        #     text="Saved",
        #     font=customtkinter.CTkFont(size=20, weight="bold"),
        # )
        # self.logo_label.grid(row=13, column=0, padx=25, pady=(25, 30), sticky="w")
        
        self.optionmenu_simulation = customtkinter.CTkOptionMenu(
            self.frame_3,
            command=self.update_simulation_options,
            dynamic_resizing=False
        )
        self.optionmenu_simulation.grid(row=13, column=0, columnspan=2, pady=(0,25))
        
        ###########################################################################
        ###########################################################################
        ###########################################################################

        # Option Menu for Battery
        self.label_battery = customtkinter.CTkLabel(
            self.frame_3, text="Battery", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_battery.grid(row=1, column=0, columnspan=2)
        self.optionmenu_battery = customtkinter.CTkOptionMenu(
            self.frame_3, dynamic_resizing=False, command=self.update_battery_options
        )
        self.optionmenu_battery.grid(row=2, column=0, columnspan=2, pady=(0,15))
        
        #########################
        
        self.switch_battery = customtkinter.CTkSwitch(
            self.frame_3, text="Battery?", command=self.switch_battery_event
        )
        self.switch_battery.grid(row=0, column=0, columnspan=2, pady=(25,0))
        
        self.label_battery_charge = customtkinter.CTkLabel(
            self.frame_3,
            text="Max Charge (kW)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_battery_charge.grid(row=3, column=0, padx=25, sticky='w')
        self.entry_battery_charge = customtkinter.CTkEntry( 
            self.frame_3, width=50,
        )
        self.entry_battery_charge.grid(row=3, column=1)
        
        #########################
        
        self.label_battery_discharge = customtkinter.CTkLabel(
            self.frame_3,
            text="Max Discharge (kW)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_battery_discharge.grid(row=4, column=0, padx=25, sticky='w')
        self.entry_battery_discharge = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_battery_discharge.grid(row=4, column=1)
        
        #########################
        
        self.label_battery_capacity = customtkinter.CTkLabel(
            self.frame_3,
            text="Capacity (kWh)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_battery_capacity.grid(row=5, column=0, padx=25, sticky='w')
        self.entry_battery_capacity = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_battery_capacity.grid(row=5, column=1)
        
        #########################
        
        self.label_battery_efficiency = customtkinter.CTkLabel(
            self.frame_3,
            text="Efficiency (%)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_battery_efficiency.grid(row=6, column=0, padx=25, sticky='w')
        self.entry_battery_efficiency = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_battery_efficiency.grid(row=6, column=1)
        
        #########################
        
        self.label_battery_cycle_life = customtkinter.CTkLabel(
            self.frame_3,
            text="Cycle Life",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_battery_cycle_life.grid(row=7, column=0, padx=25, sticky='w')
        self.entry_battery_cycle_life = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_battery_cycle_life.grid(row=7, column=1)
        
        #########################
        
        self.label_battery_price = customtkinter.CTkLabel(
            self.frame_3,
            text="Battery Price (€)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_battery_price.grid(row=8, column=0, padx=25, sticky='w')
        self.entry_battery_price = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_battery_price.grid(row=8, column=1)
        
        ###########################################################################
        ###########################################################################
        ###########################################################################

        # Option Menu for SolarPanel
        self.label_solar_panel = customtkinter.CTkLabel(
            self.frame_3, text="Solar Panel", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_solar_panel.grid(row=1, column=2, columnspan=2)
        self.optionmenu_solar_panel = customtkinter.CTkOptionMenu(
            self.frame_3,
            dynamic_resizing=False,
            command=self.update_solarpanel_options,
        )
        self.optionmenu_solar_panel.grid(row=2, column=2, columnspan=2, pady=(0,15))
        
        #########################
        
        self.switch_solar = customtkinter.CTkSwitch(
            self.frame_3, command=self.switch_solar_event, text="Solar Panels?"
        )
        self.switch_solar.grid(row=0, column=2, columnspan=2, pady=(25,0))
        
        ########################
        
        self.label_solar_azimuth = customtkinter.CTkLabel(
            self.frame_3,
            text="Azimuth (°)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_solar_azimuth.grid(row=3, column=2, padx=30, sticky='w')
        self.entry_solar_azimuth = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_solar_azimuth.grid(row=3, column=3)
        
        #########################
        
        self.label_solar_tilt = customtkinter.CTkLabel(
            self.frame_3,
            text="Tilt (°)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_solar_tilt.grid(row=4, column=2, padx=30, sticky='w')
        self.entry_solar_tilt = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_solar_tilt.grid(row=4, column=3)
        
        #########################
        
        self.label_solar_number_of_panels = customtkinter.CTkLabel(
            self.frame_3,
            text="Number Of Panels",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_solar_number_of_panels.grid(row=5, column=2, padx=30, sticky='w')
        self.entry_solar_number_of_panels = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_solar_number_of_panels.grid(row=5, column=3)
        
        #########################
        
        self.label_solar_efficiency = customtkinter.CTkLabel(
            self.frame_3,
            text="Efficiency (%)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_solar_efficiency.grid(row=6, column=2, padx=30, sticky='w')
        self.entry_solar_efficiency = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_solar_efficiency.grid(row=6, column=3)
        
        #########################
        
        self.label_solar_length = customtkinter.CTkLabel(
            self.frame_3,
            text="Length (m)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_solar_length.grid(row=7, column=2, padx=30, sticky='w')
        self.entry_solar_length = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_solar_length.grid(row=7, column=3)
        
        #########################
        
        self.label_solar_width = customtkinter.CTkLabel(
            self.frame_3,
            text="Width (m)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_solar_width.grid(row=8, column=2, padx=30, sticky='w')
        self.entry_solar_width = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_solar_width.grid(row=8, column=3)
        
        ###########################################################################
        ###########################################################################
        ###########################################################################

        # Option Menu for EVCharger
        self.label_ev_charger = customtkinter.CTkLabel(
            self.frame_3, text="EV Charger", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_ev_charger.grid(row=1, column=4, columnspan=2)
        self.optionmenu_ev_charger = customtkinter.CTkOptionMenu(
            self.frame_3,
            dynamic_resizing=False,
            command=self.update_ev_options,
        )
        self.optionmenu_ev_charger.grid(row=2, column=4, columnspan=2, pady=(0,15))
        
        #########################
        
        self.switch_ev = customtkinter.CTkSwitch(
            self.frame_3, command=self.switch_ev_event, text="EV Charger?"
        )
        self.switch_ev.grid(row=0, column=4, columnspan=2, pady=(25,0))
        
        ########################
        
        self.label_ev_charge = customtkinter.CTkLabel(
            self.frame_3,
            text="Max Charge (kW)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_ev_charge.grid(row=3, column=4, padx=30, sticky='w')
        self.entry_ev_charge = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_ev_charge.grid(row=3, column=5)
        
        #########################
        
        self.label_ev_number_of_cars = customtkinter.CTkLabel(
            self.frame_3,
            text="Number of Cars",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_ev_number_of_cars.grid(row=4, column=4, padx=30, sticky='w')
        self.entry_ev_number_of_cars = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_ev_number_of_cars.grid(row=4, column=5)
        
        #########################
        
        self.label_ev_distance_year = customtkinter.CTkLabel(
            self.frame_3,
            text="Distance Year (km)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_ev_distance_year.grid(row=5, column=4, padx=30, sticky='w')
        self.entry_ev_distance_year = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_ev_distance_year.grid(row=5, column=5)
        
        #########################
        
        self.label_ev_efficiency = customtkinter.CTkLabel(
            self.frame_3,
            text="Efficiency (%)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_ev_efficiency.grid(row=6, column=4, padx=30, sticky='w')
        self.entry_ev_efficiency = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_ev_efficiency.grid(row=6, column=5)
        
        ###########################################################################
        ###########################################################################
        ###########################################################################

        # Option Menu for Heat Pump
        self.label_heat_pump = customtkinter.CTkLabel(
            self.frame_3, text="Heat Pump", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_heat_pump.grid(row=1, column=6, columnspan=2)
        self.optionmenu_heat_pump = customtkinter.CTkOptionMenu(
            self.frame_3,
            dynamic_resizing=False,
            command=self.update_heat_options,
        )
        self.optionmenu_heat_pump.grid(row=2, column=6, columnspan=2, pady=(0,15))
        
        #########################
        
        self.switch_heat = customtkinter.CTkSwitch(
            self.frame_3, command=self.switch_heat_event, text="Heat Pump?"
        )
        self.switch_heat.grid(row=0, column=6, columnspan=2, pady=(25,0))
        
        #########################
        
        self.label_heat_certificate = customtkinter.CTkLabel(
            self.frame_3,
            text="Energy Eff Certificate",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_heat_certificate.grid(row=3, column=6, padx=30, sticky='w')
        self.optionmenu_certificate = customtkinter.CTkOptionMenu(
            self.frame_3,
            dynamic_resizing=False,
            width=100,
            values=["A+", "A", "B", "C", "D", "E", "F"],
        )
        self.optionmenu_certificate.grid(row=3, column=7)
        
        ########################
        
        self.label_heat_area = customtkinter.CTkLabel(
            self.frame_3,
            text="Area House (m²)",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_heat_area.grid(row=4, column=6, padx=30, sticky='w')
        self.entry_heat_area = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_heat_area.grid(row=4, column=7)
        
        #########################
        
        self.label_heat_cop = customtkinter.CTkLabel(
            self.frame_3,
            text="COP",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_heat_cop.grid(row=5, column=6, padx=30, sticky='w')
        self.entry_heat_cop = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_heat_cop.grid(row=5, column=7)
        
        
        #########################
        
        self.label_heat_temp = customtkinter.CTkLabel(
            self.frame_3,
            text="Desired °C inside",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_heat_temp.grid(row=6, column=6, padx=30, sticky='w')
        self.entry_heat_temp = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_heat_temp.grid(row=6, column=7)
        
        
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
        
        # Option Menu for General values
        self.label_general = customtkinter.CTkLabel(
            self.frame_3, text="General", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.label_general.grid(row=1, column=8, columnspan=2, pady=(0,0))
        
        ########################
        
        self.label_consumer_profile = customtkinter.CTkLabel(
            self.frame_3,
            text="Consumer Profile",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_consumer_profile.grid(row=3, column=8, padx=30, sticky='w')
        self.optionmenu_consumer_profile = customtkinter.CTkOptionMenu(
            self.frame_3,
            dynamic_resizing=False,
            width=100,
        )
        self.optionmenu_consumer_profile.grid(
            row=3, column=9, padx=(0,25)
        )
        
        ########################
        
        self.label_provider = customtkinter.CTkLabel(
            self.frame_3,
            text="Provider",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_provider.grid(row=4, column=8, padx=30, sticky='w')
        self.optionmenu_provider = customtkinter.CTkOptionMenu(
            self.frame_3,
            dynamic_resizing=False,
            width=100,
            values=["Ecopower", "Engie Dynamic", "Octa+Dynamic"],
        )
        self.optionmenu_provider.grid(
            row=4, column=9, padx=(0,25)
        )

        ########################
        
        self.label_general_latitude = customtkinter.CTkLabel(
            self.frame_3,
            text="Latitude",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_general_latitude.grid(row=5, column=8, padx=30, sticky='w')
        self.entry_general_latitude = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_general_latitude.grid(row=5, column=9, padx=(0,25))
        
        ########################
        
        self.label_general_longitude = customtkinter.CTkLabel(
            self.frame_3,
            text="Longitude",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_general_longitude.grid(row=6, column=8, padx=30, sticky='w')
        self.entry_general_longitude = customtkinter.CTkEntry(
            self.frame_3, width=50,
        )
        self.entry_general_longitude.grid(row=6, column=9, padx=(0,25))
        
        ########################
        
        self.label_general_start_date = customtkinter.CTkLabel(
            self.frame_3,
            text="Start Date",
            font=customtkinter.CTkFont(size=15),
        )
        self.label_general_start_date.grid(row=7, column=8, padx=30, sticky='w')
        self.entry_general_start_date = customtkinter.CTkEntry(
            self.frame_3, width=100,
        )
        self.entry_general_start_date.grid(row=7, column=9, padx=(0,25))
        
        ###########################################################################
        ###########################################################################
        ###########################################################################
        
        self.checkbox_testing = customtkinter.CTkCheckBox(self.frame_3, text="Use Testing Data", onvalue="on", offvalue="off")
        self.checkbox_testing.grid(row=11, column=8, columnspan=2, pady=(20,15))
        
        self.button_confirm = customtkinter.CTkButton(
            self.frame_3,
            text="Confirm",
            command=lambda: self.confirm_parameters(bool_save=0),
        )
        self.button_confirm.grid(row=12, column=8, columnspan=2)
        
        self.button_confirm_save = customtkinter.CTkButton(
            self.frame_3,
            text="Confirm And Save",
            command=lambda: self.confirm_parameters(bool_save=1),
        )
        self.button_confirm_save.grid(row=13, column=8, columnspan=2, pady=(0,25))

        self.checkbox_testing.select()
        self.switch_battery.select()
        self.switch_solar.select()
        self.switch_ev.select()
        self.switch_heat.select()
        self.populate_simulation_options()
        self.populate_battery_options()
        self.populate_solarpanel_options()
        self.populate_ev_options()
        self.populate_consumer_profile_options()
        self.populate_heat_options()
        
        # Fetch simulation data from the database
        self.simulation_data = self.db_manager.fetch_simulation_data()
        # Extract simulation names
        self.simulation_options = [simulation[1] for simulation in self.simulation_data]
        
        if "temp" in self.simulation_options:
            self.populate_with_previous_data()
            
        try:
            self.db_manager.delete_simulation_by_name("temp")
        except:
            pass
        
        
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    
    #TODO aparte functie maken
    def switch_battery_event(self):
        if self.switch_battery.get() == 0:
            self.optionmenu_battery.configure(fg_color="grey17", button_color="grey17", text_color_disabled="grey17", state = "disabled")
            self.entry_battery_charge.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_battery_charge.configure(text_color='grey17')
            self.entry_battery_discharge.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_battery_discharge.configure(text_color='grey17')
            self.entry_battery_capacity.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_battery_capacity.configure(text_color='grey17')
            self.entry_battery_efficiency.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_battery_efficiency.configure(text_color='grey17')
            self.entry_battery_cycle_life.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_battery_cycle_life.configure(text_color='grey17')
            self.entry_battery_price.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_battery_price.configure(text_color='grey17')
            
        if self.switch_battery.get() == 1:
            self.optionmenu_battery.configure(fg_color="#AEB74F", button_color="#9fa845", state = "normal")
            self.label_battery_charge.configure(text_color='#DCE4EE')
            self.entry_battery_charge.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            self.label_battery_discharge.configure(text_color='#DCE4EE')
            self.entry_battery_discharge.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            self.label_battery_capacity.configure(text_color='#DCE4EE')
            self.entry_battery_capacity.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            self.label_battery_efficiency.configure(text_color='#DCE4EE')
            self.entry_battery_efficiency.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            self.label_battery_cycle_life.configure(text_color='#DCE4EE')
            self.entry_battery_cycle_life.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            self.label_battery_price.configure(text_color='#DCE4EE')
            self.entry_battery_price.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            
            
    ##############################
    
    
    def switch_solar_event(self):
        if self.switch_solar.get() == 0:
            self.optionmenu_solar_panel.configure(fg_color="grey17", button_color="grey17", text_color_disabled="grey17", state = "disabled")
            self.entry_solar_azimuth.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_solar_azimuth.configure(text_color='grey17')
            self.entry_solar_tilt.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_solar_tilt.configure(text_color='grey17')
            self.entry_solar_number_of_panels.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_solar_number_of_panels.configure(text_color='grey17')
            self.entry_solar_efficiency.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_solar_efficiency.configure(text_color='grey17')
            self.entry_solar_length.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_solar_length.configure(text_color='grey17')
            self.entry_solar_width.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_solar_width.configure(text_color='grey17')
            
            
        if self.switch_solar.get() == 1:
            self.optionmenu_solar_panel.configure(fg_color="#AEB74F", button_color="#9fa845", state = "normal")
            self.label_solar_azimuth.configure(text_color='#DCE4EE')
            self.entry_solar_azimuth.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            self.label_solar_tilt.configure(text_color='#DCE4EE')
            self.entry_solar_tilt.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            self.label_solar_number_of_panels.configure(text_color='#DCE4EE')
            self.entry_solar_number_of_panels.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            self.label_solar_efficiency.configure(text_color='#DCE4EE')
            self.entry_solar_efficiency.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            self.label_solar_length.configure(text_color='#DCE4EE')
            self.entry_solar_length.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            self.label_solar_width.configure(text_color='#DCE4EE')
            self.entry_solar_width.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            
            
    #############################
    
    
    def switch_ev_event(self):
        if self.switch_ev.get() == 0:
            self.optionmenu_ev_charger.configure(fg_color="grey17", button_color="grey17", text_color_disabled="grey17", state = "disabled")
            self.entry_ev_charge.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_ev_charge.configure(text_color='grey17')
            self.entry_ev_number_of_cars.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_ev_number_of_cars.configure(text_color='grey17')
            self.entry_ev_distance_year.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_ev_distance_year.configure(text_color='grey17')
            self.entry_ev_efficiency.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_ev_efficiency.configure(text_color='grey17')
            
            
        if self.switch_ev.get() == 1:
            self.optionmenu_ev_charger.configure(fg_color="#AEB74F", button_color="#9fa845", state = "normal")
            self.label_ev_charge.configure(text_color='#DCE4EE')
            self.entry_ev_charge.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            self.label_ev_number_of_cars.configure(text_color='#DCE4EE')
            self.entry_ev_number_of_cars.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            self.label_ev_distance_year.configure(text_color='#DCE4EE')
            self.entry_ev_distance_year.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            self.label_ev_efficiency.configure(text_color='#DCE4EE')
            self.entry_ev_efficiency.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            
    ############################
    
    def switch_heat_event(self):
        if self.switch_heat.get() == 0:
            self.optionmenu_heat_pump.configure(fg_color="grey17", button_color="grey17", text_color_disabled="grey17", state = "disabled")
            self.optionmenu_certificate.configure(fg_color="grey17", button_color="grey17", text_color_disabled="grey17", state = "disabled")
            self.label_heat_certificate.configure(text_color='grey17')
            self.entry_heat_area.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_heat_area.configure(text_color='grey17')
            self.entry_heat_cop.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_heat_cop.configure(text_color='grey17')
            self.entry_heat_temp.configure(fg_color="grey17", border_color="grey17", text_color="grey17", state = "disabled")
            self.label_heat_temp.configure(text_color='grey17')
            
            
        if self.switch_heat.get() == 1:
            self.optionmenu_heat_pump.configure(fg_color="#AEB74F", button_color="#9fa845", text_color="black", state = "normal")
            self.label_heat_certificate.configure(text_color='#DCE4EE')
            self.optionmenu_certificate.configure(state = "normal", fg_color="#AEB74F", button_color="#9fa845")
            self.label_heat_area.configure(text_color='#DCE4EE')
            self.entry_heat_area.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            self.label_heat_cop.configure(text_color='#DCE4EE')
            self.entry_heat_cop.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
            self.label_heat_temp.configure(text_color='#DCE4EE')
            self.entry_heat_temp.configure(state = "normal", fg_color="#343638", text_color="#DCE4EE", border_color="#565B5E")
    
    
    
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    
    def update_simulation_options(self, selected_simulation):
        
        selected_simulation = self.optionmenu_simulation.get()
        selected_simulation_data = self.db_manager.fetch_simulation_by_name(selected_simulation)
        
        # Select the switch if selected_simulation_data value is 1
        if selected_simulation_data[2] == 1:
            self.switch_battery.select()
        # Deselect the switch if selected_simulation_data value is 0
        else:
            self.switch_battery.deselect()

        # Repeat the process for switch_solar and switch_ev
        if selected_simulation_data[8] == 1:
            self.switch_solar.select()
        else:
            self.switch_solar.deselect()

        if selected_simulation_data[15] == 1:
            self.switch_ev.select()
        else:
            self.switch_ev.deselect()
            
        if selected_simulation_data[20] == 1:
            self.switch_heat.select()
        else:
            self.switch_heat.deselect()
        
        self.entry_battery_charge.delete(0, tkinter.END)
        self.entry_battery_discharge.delete(0, tkinter.END)
        self.entry_battery_capacity.delete(0, tkinter.END)
        self.entry_battery_efficiency.delete(0, tkinter.END)
        self.entry_battery_cycle_life.delete(0, tkinter.END)
        self.entry_battery_price.delete(0, tkinter.END)
        self.entry_solar_azimuth.delete(0, tkinter.END)
        self.entry_solar_tilt.delete(0, tkinter.END)
        self.entry_solar_number_of_panels.delete(0, tkinter.END)
        self.entry_solar_efficiency.delete(0, tkinter.END)
        self.entry_solar_length.delete(0, tkinter.END)
        self.entry_solar_width.delete(0, tkinter.END)
        self.entry_ev_charge.delete(0, tkinter.END)
        self.entry_ev_number_of_cars.delete(0, tkinter.END)
        self.entry_ev_efficiency.delete(0, tkinter.END)
        self.entry_ev_distance_year.delete(0, tkinter.END)
        self.entry_heat_area.delete(0, tkinter.END)
        self.entry_heat_cop.delete(0, tkinter.END)
        self.entry_heat_temp.delete(0, tkinter.END)
        self.entry_general_latitude.delete(0, tkinter.END)
        self.entry_general_longitude.delete(0, tkinter.END)
        self.entry_general_start_date.delete(0, tkinter.END)
        
        self.entry_battery_charge.insert(0, selected_simulation_data[3])
        self.entry_battery_discharge.insert(0, selected_simulation_data[4])
        self.entry_battery_capacity.insert(0, selected_simulation_data[5])
        self.entry_battery_efficiency.insert(0, selected_simulation_data[6])
        self.entry_battery_cycle_life.insert(0, int(str(selected_simulation_data[7]).split("12345")[0]))
        self.entry_battery_price.insert(0, int(str(selected_simulation_data[7]).split("12345")[1]))
        self.entry_solar_azimuth.insert(0, selected_simulation_data[9])
        self.entry_solar_tilt.insert(0, selected_simulation_data[10])
        self.entry_solar_number_of_panels.insert(0, selected_simulation_data[11])
        self.entry_solar_efficiency.insert(0, selected_simulation_data[12])
        self.entry_solar_length.insert(0, selected_simulation_data[13])
        self.entry_solar_width.insert(0, selected_simulation_data[14])
        self.entry_ev_charge.insert(0, selected_simulation_data[16])
        self.entry_ev_number_of_cars.insert(0, selected_simulation_data[17])
        self.entry_ev_efficiency.insert(0, selected_simulation_data[18])
        self.entry_ev_distance_year.insert(0, selected_simulation_data[19])
        self.optionmenu_certificate.set(selected_simulation_data[21])
        self.entry_heat_area.insert(0, selected_simulation_data[22])
        self.entry_heat_cop.insert(0, selected_simulation_data[23])
        self.entry_heat_temp.insert(0, selected_simulation_data[24])
        self.optionmenu_consumer_profile.set(selected_simulation_data[25])
        self.optionmenu_provider.set(selected_simulation_data[26])
        self.entry_general_latitude.insert(0, selected_simulation_data[27])
        self.entry_general_longitude.insert(0, selected_simulation_data[28])
        self.entry_general_start_date.insert(0, selected_simulation_data[29])
        
        self.switch_battery_event()
        self.switch_solar_event()
        self.switch_ev_event()
        self.switch_heat_event()
            
            
        #TODO fix this from database
        #self.checkbox_testing.
        
    def update_battery_options(self, selected_battery):
        
        selected_battery = self.optionmenu_battery.get()
        selected_battery_data = self.db_manager.fetch_battery_by_name(selected_battery)
        
        self.entry_battery_charge.delete(0, tkinter.END)
        self.entry_battery_discharge.delete(0, tkinter.END)
        self.entry_battery_capacity.delete(0, tkinter.END)
        self.entry_battery_efficiency.delete(0, tkinter.END)
        self.entry_battery_cycle_life.delete(0, tkinter.END)
        self.entry_battery_price.delete(0, tkinter.END)
        
        self.entry_battery_charge.insert(0, selected_battery_data[3])
        self.entry_battery_discharge.insert(0, selected_battery_data[4])
        self.entry_battery_capacity.insert(0, selected_battery_data[2])
        self.entry_battery_efficiency.insert(0, selected_battery_data[7])
        self.entry_battery_cycle_life.insert(0, int(str(selected_battery_data[8]).split("12345")[0]))
        self.entry_battery_price.insert(0, int(str(selected_battery_data[8]).split("12345")[1]))
        
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
        self.entry_ev_number_of_cars.delete(0, tkinter.END)
        self.entry_ev_efficiency.delete(0, tkinter.END)
        self.entry_ev_distance_year.delete(0, tkinter.END)
        
        self.entry_ev_charge.insert(0, selected_ev_data[2])
        self.entry_ev_number_of_cars.insert(0, selected_ev_data[3])
        self.entry_ev_efficiency.insert(0, selected_ev_data[4])
        self.entry_ev_distance_year.insert(0, selected_ev_data[5])
        
    def update_heat_options(self, selected_heat):
        
        selected_heat = self.optionmenu_heat_pump.get()
        selected_heat_data = self.db_manager.fetch_ev_charger_by_name(selected_heat)
        
        self.entry_heat_area.delete(0, tkinter.END)
        self.entry_heat_cop.delete(0, tkinter.END)
        self.entry_heat_temp.delete(0, tkinter.END)
        
        self.optionmenu_certificate.set(selected_heat_data[2])
        self.entry_heat_area.insert(0, selected_heat_data[3])
        self.entry_heat_cop.insert(0, selected_heat_data[4])
        self.entry_heat_temp.insert(0, selected_heat_data[5])
        
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
        simulation_options = [simulation[1] for simulation in simulation_data if simulation[1] != "temp"]
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
        self.optionmenu_battery.configure(values=[])
        self.optionmenu_battery.configure(values=battery_options)
        self.optionmenu_battery.set("Load Battery")
        
    def populate_solarpanel_options(self):
        # Fetch battery data from the database
        solarpanel_data = self.db_manager.fetch_solarpanel_data()
        # Extract battery names
        solarpanel_options = [solarpanel[1] for solarpanel in solarpanel_data]
        # Update option menu with battery names
        self.optionmenu_solar_panel.configure(values=[])
        self.optionmenu_solar_panel.configure(values=solarpanel_options)
        self.optionmenu_solar_panel.set("Load Solar Panel")
        
    def populate_ev_options(self):
        # Fetch ev data from the database
        ev_data = self.db_manager.fetch_ev_charger_data()
        # Extract ev names
        ev_options = [ev[1] for ev in ev_data]
        # Update option menu with ev names
        self.optionmenu_ev_charger.configure(values=[])
        self.optionmenu_ev_charger.configure(values=ev_options)
        self.optionmenu_ev_charger.set("Load Ev Charger")
        
    def populate_heat_options(self):
        # Fetch heat data from the database
        heat_data = self.db_manager.fetch_heat_pump_data()
        # Extract heat names
        heat_options = [heat[1] for heat in heat_data]
        # Update option menu with heat names
        self.optionmenu_heat_pump.configure(values=[])
        self.optionmenu_heat_pump.configure(values=heat_options)
        self.optionmenu_heat_pump.set("Load Heat Pump")
        
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
            
    def populate_with_previous_data(self):
        
        previous_data = self.db_manager.fetch_simulation_by_name("temp")
        
        self.entry_battery_charge.insert(0, previous_data[3])
        self.entry_battery_discharge.insert(0, previous_data[4])
        self.entry_battery_capacity.insert(0, previous_data[5])
        self.entry_battery_efficiency.insert(0, previous_data[6])
        self.entry_battery_cycle_life.insert(0, int(str(previous_data[7]).split("12345")[0]))
        self.entry_battery_price.insert(0, int(str(previous_data[7]).split("12345")[1]))
        self.entry_solar_azimuth.insert(0, previous_data[9])
        self.entry_solar_tilt.insert(0, previous_data[10])
        self.entry_solar_number_of_panels.insert(0, previous_data[11])
        self.entry_solar_efficiency.insert(0, previous_data[12])
        self.entry_solar_length.insert(0, previous_data[13])
        self.entry_solar_width.insert(0, previous_data[14])
        self.entry_ev_charge.insert(0, previous_data[16])
        self.entry_ev_number_of_cars.insert(0, previous_data[17])
        self.entry_ev_efficiency.insert(0, previous_data[18])
        self.entry_ev_distance_year.insert(0, previous_data[19])
        self.optionmenu_certificate.set(previous_data[21])
        self.entry_heat_area.insert(0, previous_data[22])
        self.entry_heat_cop.insert(0, previous_data[23])
        self.entry_heat_temp.insert(0, previous_data[24])
        self.optionmenu_consumer_profile.set(previous_data[25])
        self.optionmenu_provider.set(previous_data[26])
        self.entry_general_latitude.insert(0, previous_data[27])
        self.entry_general_longitude.insert(0, previous_data[28])
        self.entry_general_start_date.insert(0, previous_data[29])
        
        # Select the switch if previous_data value is 1
        if previous_data[2] == 1:
            self.switch_battery.select()
        # Deselect the switch if previous_data value is 0
        else:
            self.switch_battery.deselect()

        # Repeat the process for switch_solar and switch_ev
        if previous_data[8] == 1:
            self.switch_solar.select()
        else:
            self.switch_solar.deselect()

        if previous_data[15] == 1:
            self.switch_ev.select()
        else:
            self.switch_ev.deselect()
            
        if previous_data[20] == 1:
            self.switch_heat.select()
        else:
            self.switch_heat.deselect()
            
        self.switch_battery_event()
        self.switch_solar_event()
        self.switch_ev_event()
        self.switch_heat_event()
        
            
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
    ###########################################################################
        
    def standardize_date(self, date_input):
        try:
            # Parse the date from the given date string
            parsed_date = parser.parse(date_input)
            # Format the date to YYYY-MM-DD
            standardized_date = parsed_date.strftime('%Y-%m-%d')
            return standardized_date
        except ValueError:
            return "Invalid date"
        
        
    def confirm_parameters(self, bool_save):
        # Collect all entries
        entries = {
            "Battery": self.switch_battery.get(),
            "Battery Charge": self.entry_battery_charge.get() if self.switch_battery.get() else "0",
            "Battery Discharge": self.entry_battery_discharge.get() if self.switch_battery.get() else "0",
            "Battery Capacity": self.entry_battery_capacity.get() if self.switch_battery.get() else "0",
            "Battery Efficiency": self.entry_battery_efficiency.get() if self.switch_battery.get() else "0",
            "Battery OPEX": int(str(self.entry_battery_cycle_life.get()) + "12345" + str(self.entry_battery_price.get())) if self.switch_battery.get() else "0",
            "Solar": self.switch_solar.get(),
            "Solar Azimuth": self.entry_solar_azimuth.get() if self.switch_solar.get() else "0",
            "Solar Tilt": self.entry_solar_tilt.get() if self.switch_solar.get() else "0",
            "Number of Solar Panels": self.entry_solar_number_of_panels.get() if self.switch_solar.get() else "0",
            "Solar Efficiency": self.entry_solar_efficiency.get() if self.switch_solar.get() else "0",
            "Solar Length": self.entry_solar_length.get() if self.switch_solar.get() else "0",
            "Solar Width": self.entry_solar_width.get() if self.switch_solar.get() else "0",
            "Ev": self.switch_ev.get(),
            "EV Charge": self.entry_ev_charge.get() if self.switch_ev.get() else "0",
            "EV Number of Cars": self.entry_ev_number_of_cars.get() if self.switch_ev.get() else "0",
            "EV Efficiency": self.entry_ev_efficiency.get() if self.switch_ev.get() else "0",
            "EV Distance Year": self.entry_ev_distance_year.get() if self.switch_ev.get() else "0",
            "Heat": self.switch_heat.get(),
            "Heat certificate": self.optionmenu_certificate.get() if self.switch_heat.get() else "0",
            "Heat Area": self.entry_heat_area.get() if self.switch_heat.get() else "0",
            "Heat COP": self.entry_heat_cop.get() if self.switch_heat.get() else "0",
            "Heat Temp": self.entry_heat_temp.get() if self.switch_heat.get() else "0",
            "Consumer Profile": self.optionmenu_consumer_profile.get().replace(', ', '_'),
            "Provider": self.optionmenu_provider.get(),
            "Latitude": self.entry_general_latitude.get(),
            "Longitude": self.entry_general_longitude.get(),
            "Start Date": self.standardize_date(self.entry_general_start_date.get()),
            "Use Api": self.checkbox_testing.get()
        }
        
        # Define ranges for various entries
        #TODO correct cycle_life values
        ranges = {
            "Battery Charge": (0, 100),
            "Battery Discharge": (0, 100),
            "Battery Capacity": (0, 1000),
            "Battery Efficiency": (0, 100),
            "Battery OPEX": (0, 10000000000000000),
            "Solar Azimuth": (0, 360),
            "Solar Tilt": (0, 90),
            "Number of Solar Panels": (0, 200),
            "Solar Efficiency": (0, 100),
            "Solar Length": (0, 20),
            "Solar Width": (0, 10),
            "EV Charge": (0, 100),
            "EV Number of Cars": (0, 10),
            "EV Efficiency": (0, 100),
            "EV Distance Year": (0, 25000),
            "Heat Area": (0, 1000),
            "Heat COP": (0, 10),
            "Heat Temp": (0, 30),
            "Latitude": (-90, 90),
            "Longitude": (-180, 180)
        }

        # Check for empty or out-of-range fields in one pass
        invalid_fields = {}
        for key, value in entries.items():
            if not str(value).strip():
                invalid_fields[key] = "Empty"
            elif key in ranges and not self.is_within_range(value, *ranges[key]):
                invalid_fields[key] = f"must be between the values: {ranges[key][0]} and {ranges[key][1]}"
                
        if invalid_fields:      
            message = "\n".join([f"{key.replace('_', ' ')} {reason}" for key, reason in invalid_fields.items()])
            CTkMessagebox(title="Warning", message=message)   
            return
        
        # Check for empty fields considering all values as strings
        empty_fields = [key for key, value in entries.items() if not str(value).strip()]
        
        # Check if any fields are empty
        if empty_fields:
            # Show a warning with the fields that are empty
            warning_message = "Please fill in the following fields: " + ", ".join(empty_fields)
            CTkMessagebox(title="Warning", message=warning_message)
            return  # Stop further processing

        # Check for zero values for battery, EV, and solar when their respective switches are selected
        if self.switch_battery.get():
            if float(entries["Battery Charge"]) <= 0 or float(entries["Battery Discharge"]) <= 0 or float(entries["Battery Capacity"]) <= 0 or float(entries["Battery Efficiency"]) <= 0 or float(entries["Battery OPEX"]) <= 0:
                warning_message = "Battery fields cannot be zero when Battery is selected."
                CTkMessagebox(title="Warning", message=warning_message)
                return  # Stop further processing

        if self.switch_solar.get():
            if float(entries["Solar Azimuth"]) <= 0 or float(entries["Solar Tilt"]) <= 0 or float(entries["Number of Solar Panels"]) <= 0 or float(entries["Solar Efficiency"]) <= 0 or float(entries["Solar Length"]) <= 0 or float(entries["Solar Width"]) <= 0:
                warning_message = "Solar fields cannot be zero when Solar is selected."
                CTkMessagebox(title="Warning", message=warning_message)
                return  # Stop further processing

        if self.switch_ev.get():
            if float(entries["EV Charge"]) <= 0 or float(entries["EV Number of Cars"]) <= 0 or float(entries["EV Efficiency"]) <= 0 or float(entries["EV Distance Year"]) <= 0:
                warning_message = "EV fields cannot be zero when EV is selected."
                CTkMessagebox(title="Warning", message=warning_message)
                return  # Stop further processing
            
        if self.switch_heat.get():
            if float(entries["Heat Area"]) <= 0 or float(entries["Heat COP"]) <= 0 or float(entries["Heat Temp"]) <= 0:
                warning_message = "Heat Pump fields cannot be zero when Heat Pump is selected."
                CTkMessagebox(title="Warning", message=warning_message)
                return  # Stop further processing
            
        if(bool_save == 1):

            dialog = customtkinter.CTkInputDialog(text="Choose a name:", title="Name")
            
            self.db_manager.add_simulation(
            str(dialog.get_input()), *entries.values()
            )

        # If all fields are filled, continue with the operation
        self.db_manager.add_simulation(
            "temp", *entries.values()
        )
        
        
        self.destroy()
        return
    
    def is_within_range(self, value, min_val, max_val):
        try:
            num_value = float(value)
            return min_val <= num_value <= max_val
        except ValueError:
            return False



