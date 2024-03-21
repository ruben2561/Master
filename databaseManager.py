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

# Usage example:
# db_manager = DatabaseManager("database_master.db")
# battery_data = db_manager.fetch_battery_data()
# print(battery_data)
