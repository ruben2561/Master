import tkinter
import customtkinter
from databaseManager import DatabaseManager  # Import your database manager class

class batteryEditDialog(customtkinter.CTk):
    def __init__(self, db_manager, battery_name):
        super().__init__()

        self.title("Edit Battery")

        self.db_manager = db_manager
        self.battery_name = battery_name

        self.frame_3 = customtkinter.CTkFrame(master=self)
        self.frame_3.pack(pady=20, padx=60, fill="both", expand=True)

        # Input fields for battery parameters
        self.label_name = customtkinter.CTkLabel(
            master=self.frame_3,
            text="Battery Name:",
            justify=tkinter.LEFT,
            anchor="w"
        )
        self.label_name.pack(pady=5, padx=10, anchor="w")

        self.entry_name = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Battery Name",
            justify=tkinter.CENTER,
            width=300,
        )
        self.entry_name.pack(pady=5, padx=10)

        self.label_capacity = customtkinter.CTkLabel(
            master=self.frame_3,
            text="Capacity (kWh):",
            justify=tkinter.LEFT,
            anchor="w"
        )
        self.label_capacity.pack(pady=5, padx=10, anchor="w")

        self.entry_capacity = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Capacity (kWh)",
            justify=tkinter.CENTER,
            width=300,
        )
        self.entry_capacity.pack(pady=5, padx=10)

        self.label_charge_power = customtkinter.CTkLabel(
            master=self.frame_3,
            text="Charge Power (kW):",
            justify=tkinter.LEFT,
            anchor="w"
        )
        self.label_charge_power.pack(pady=5, padx=10, anchor="w")

        self.entry_charge_power = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Charge Power (kW)",
            justify=tkinter.CENTER,
            width=300,
        )
        self.entry_charge_power.pack(pady=5, padx=10)

        self.label_discharge_power = customtkinter.CTkLabel(
            master=self.frame_3,
            text="Discharge Power (kW):",
            justify=tkinter.LEFT,
            anchor="w"
        )
        self.label_discharge_power.pack(pady=5, padx=10, anchor="w")

        self.entry_discharge_power = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Discharge Power (kW)",
            justify=tkinter.CENTER,
            width=300,
        )
        self.entry_discharge_power.pack(pady=5, padx=10)

        self.label_max_soc = customtkinter.CTkLabel(
            master=self.frame_3,
            text="Max State of Charge:",
            justify=tkinter.LEFT,
            anchor="w"
        )
        self.label_max_soc.pack(pady=5, padx=10, anchor="w")

        self.entry_max_soc = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Max State of Charge",
            justify=tkinter.CENTER,
            width=300,
        )
        self.entry_max_soc.pack(pady=5, padx=10)

        self.label_min_dod = customtkinter.CTkLabel(
            master=self.frame_3,
            text="Min Depth of Discharge:",
            justify=tkinter.LEFT,
            anchor="w"
        )
        self.label_min_dod.pack(pady=5, padx=10, anchor="w")

        self.entry_min_dod = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Min Depth of Discharge",
            justify=tkinter.CENTER,
            width=300,
        )
        self.entry_min_dod.pack(pady=5, padx=10)

        self.label_efficiency = customtkinter.CTkLabel(
            master=self.frame_3,
            text="Efficiency:",
            justify=tkinter.LEFT,
            anchor="w"
        )
        self.label_efficiency.pack(pady=5, padx=10, anchor="w")

        self.entry_efficiency = customtkinter.CTkEntry(
            master=self.frame_3,
            placeholder_text="Efficiency",
            justify=tkinter.CENTER,
            width=300,
        )
        self.entry_efficiency.pack(pady=5, padx=10)

        # Fetch current battery parameters from the database
        battery_info = db_manager.fetch_battery_by_name(battery_name)

        # Pre-populate input fields with current battery parameters
        self.entry_name.insert(tkinter.END, battery_info[1])
        self.entry_capacity.insert(tkinter.END, str(battery_info[2]))
        self.entry_charge_power.insert(tkinter.END, str(battery_info[3]))
        self.entry_discharge_power.insert(tkinter.END, str(battery_info[4]))
        self.entry_max_soc.insert(tkinter.END, str(battery_info[5]))
        self.entry_min_dod.insert(tkinter.END, str(battery_info[6]))
        self.entry_efficiency.insert(tkinter.END, str(battery_info[7]))

        self.button_save = customtkinter.CTkButton(
            self.frame_3, text="Save", command=self.save_changes
        )
        self.button_save.pack(side=tkinter.BOTTOM, padx=5, pady=10)

        self.mainloop()

    def save_changes(self):
        new_battery_name = self.entry_name.get()
        capacity_kwh = self.entry_capacity.get()
        charge_power_kw = self.entry_charge_power.get()
        discharge_power_kw = self.entry_discharge_power.get()
        max_soc = self.entry_max_soc.get()
        min_dod = self.entry_min_dod.get()
        efficiency = self.entry_efficiency.get()

        # Update the battery record in the database
        self.db_manager.update_battery(self.battery_name, new_battery_name, capacity_kwh, charge_power_kw, discharge_power_kw, max_soc, min_dod, efficiency)

        # Close the dialog
        self.destroy()
