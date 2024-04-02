import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print("Error connecting to the database:", e)

    def disconnect(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()

    def fetch_battery_data(self):
        self.connect()
        try:
            self.cursor.execute("SELECT * FROM Battery")
            battery_data = self.cursor.fetchall()
            return battery_data
        except sqlite3.Error as e:
            print("Error fetching battery data:", e)

    def fetch_battery_by_name(self, battery_name):
        query = "SELECT * FROM Battery WHERE name = ?"
        self.cursor.execute(query, (battery_name,))
        battery_data = self.cursor.fetchone()
        return battery_data
    
    def add_battery(self, name, capacity, charge_power, discharge_power, max_soc, min_dod, efficiency):
        query = f"INSERT INTO Battery (name, capacityKWh, chargePowerKW, dischargePowerKW, maxSoc, minDod, efficiency) VALUES (?, ?, ?, ?, ?, ?, ?)"
        print(query)
        self.cursor.execute(query, (name,capacity,charge_power,discharge_power,max_soc,min_dod,efficiency))
        self.connection.commit()

    def delete_battery_by_name(self, name):
        query = "DELETE FROM Battery WHERE name = ?"
        self.cursor.execute(query, (name,))
        self.connection.commit()

    def update_battery(self, old_name, new_name, capacity, charge_power, discharge_power, max_soc, min_dod, efficiency):
        query = """
                UPDATE Battery 
                SET name=?, capacityKWh=?, chargePowerKW=?, dischargePowerKW=?, maxSoc=?, minDod=?, efficiency=?
                WHERE name=?
                """
        self.cursor.execute(query, (new_name, capacity, charge_power, discharge_power, max_soc, min_dod, efficiency, old_name))
        self.connection.commit()


    def fetch_solar_panel_data(self):
        self.connect()
        try:
            self.cursor.execute("SELECT * FROM SolarPanel")
            solarpanel_data = self.cursor.fetchall()
            return solarpanel_data
        except sqlite3.Error as e:
            print("Error fetching solarpanel data:", e)

    def fetch_solarpanel_by_name(self, solarpanel_name):
        query = "SELECT * FROM SolarPanel WHERE name = ?"
        self.cursor.execute(query, (solarpanel_name,))
        solarpanel_data = self.cursor.fetchone()
        return solarpanel_data
    
    def add_solarpanel(self, name, capacityACkW, capacityDCkW, azimuth, tilt, efficiency):
        query = "INSERT INTO SolarPanel ?,?,?,?,?,?"
        self.cursor.execute(query, (name, capacityACkW, capacityDCkW, azimuth, tilt, efficiency))
        self.connection.commit()

    def delete_solarpanel_by_name(self, name):
        query = "DELETE FROM SolarPanel WHERE name = ?"
        self.cursor.execute(query, (name,))
        self.connection.commit()

# Usage example:
# db_manager = DatabaseManager("database_master.db")
# battery_data = db_manager.fetch_battery_data()
# print(battery_data)
