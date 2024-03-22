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
        try:
            # Insert a new battery record into the Battery table
            self.cursor.execute("""
                INSERT INTO Battery (name, capacityKWh, chargePowerKW, dischargePowerKW, maxSoc, minDod, efficiency)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, capacity, charge_power, discharge_power, max_soc, min_dod, efficiency))
            self.conn.commit()
            print("Battery added successfully.")
        except sqlite3.Error as e:
            print("Error adding battery:", e)

    def delete_battery_by_name(self, name):
        try:
            # Delete the battery record from the Battery table based on the name
            self.cursor.execute("""
                DELETE FROM Battery
                WHERE name = ?
            """, (name,))
            self.conn.commit()
            print("Battery deleted successfully.")
        except sqlite3.Error as e:
            print("Error deleting battery:", e)

# Usage example:
# db_manager = DatabaseManager("database_master.db")
# battery_data = db_manager.fetch_battery_data()
# print(battery_data)
