import tkinter
import customtkinter
from CTkListbox import *
import tkinter
import customtkinter
from batteryCreateDialog import batteryCreateDialog
from databaseManager import DatabaseManager
from batteryEditDialog import batteryEditDialog

class BatteryManager(customtkinter.CTk):
    def __init__(self, db_manager, callback):
        super().__init__()
        self.db_manager = db_manager
        self.callback = callback

        w = 350  # width
        h = 500  # height

        # get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the CTk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.geometry("%dx%d+%d+%d" % (w, h, x, y))
        self.title("Battery Manager")

        self.frame_3 = customtkinter.CTkFrame(master=self)
        self.frame_3.pack(pady=20, padx=60, fill="both", expand=True)

        self.label_3 = customtkinter.CTkLabel(
            master=self.frame_3,
            text="Battery List",
            justify=tkinter.LEFT,
        )
        self.label_3.pack(pady=10, padx=10)

        self.listbox = CTkListbox(master=self.frame_3)
        self.listbox.pack(pady=10, padx=10)
        self.listbox.bind("<Double-Button-1>", self.open_edit_dialog)

        self.populate_battery(db_manager)

        self.button_edit = customtkinter.CTkButton(
            self.frame_3, text="Edit", command=lambda: self.open_edit_dialog(db_manager)
        )
        self.button_edit.pack(pady=5, padx=5)

        self.button_delete = customtkinter.CTkButton(
            self.frame_3, text="Delete", command=lambda: self.delete_battery(db_manager)
        )
        self.button_delete.pack(pady=5, padx=5)

        self.button_create_new = customtkinter.CTkButton(
            self.frame_3, text="Create New", command=lambda: self.create_new_battery(db_manager)
        )
        self.button_create_new.pack(pady=20, padx=5)

        self.button_cancel = customtkinter.CTkButton(
            self.frame_3, text="Close", command=self.cancel_changes
        )
        self.button_cancel.pack(padx=5, pady=20)

        self.mainloop()

    def close_dialog(self):
        # Code to close the dialog
        self.destroy()
        # Call the callback function if it's provided
        if self.callback:
            self.callback()

    def populate_battery(self, db_manager):
        # Assuming you have a DatabaseManager class with a method to fetch battery names
        battery_data = db_manager.fetch_battery_data()
        battery_names = [battery[1] for battery in battery_data]

        for battery_name in battery_names:
            self.listbox.insert(tkinter.END, battery_name)

    def open_edit_dialog(self, db_manager):
        selected_battery_index = self.listbox.curselection()
        if selected_battery_index:
            selected_battery_name = self.listbox.get(selected_battery_index)

            edit_dialog = batteryEditDialog(db_manager, selected_battery_name)
            edit_dialog.mainloop()

    def delete_battery(self, db_manager):
        selected_battery_index = self.listbox.curselection()
        if selected_battery_index:
            selected_battery_name = self.listbox.get(selected_battery_index)
            confirmation = tkinter.messagebox.askyesno("Confirmation", f"Are you sure you want to delete {selected_battery_name}?")
            if confirmation:
                # Perform deletion operation
                # Delete the battery record from the database
                db_manager.delete_battery_by_name(selected_battery_name)
                # Refresh the battery list
                self.listbox.delete(selected_battery_index)

    def create_new_battery(self, db_manager):
        edit_dialog = batteryCreateDialog(db_manager)
        edit_dialog.mainloop()

    def save_changes(self):
        # Implement function to save changes made to batteries
        pass

    def cancel_changes(self):
        # Implement function to cancel changes and close the window
        self.destroy()



