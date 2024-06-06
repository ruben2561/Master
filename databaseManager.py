import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        # Initialize with database file
        self.cursor = None
        self.connection = None
        self.db_file = db_file

    def connect(self):
        # Connect to the SQLite database
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            # Print error if connection fails
            print("Error connecting to the database:", e)

    def disconnect(self):
        # Disconnect from the SQLite database
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()

    ###########################################################################
    ###########################################################################
    ###########################################################################

    def fetch_battery_data(self):
        # Fetch all battery data from the Battery table
        self.connect()
        try:
            self.cursor.execute("SELECT * FROM Battery")
            battery_data = self.cursor.fetchall()
            return battery_data
        except sqlite3.Error as e:
            # Print error if fetching fails
            print("Error fetching battery data:", e)

    def fetch_battery_by_name(self, battery_name):
        # Fetch battery data by name from the Battery table
        query = "SELECT * FROM Battery WHERE name = ?"
        self.cursor.execute(query, (battery_name,))
        battery_data = self.cursor.fetchone()
        return battery_data
    
    def add_battery(self, name, capacity, charge_power, discharge_power, max_soc, min_dod, efficiency, OPEX):
        # Add a new battery entry to the Battery table
        query = f"INSERT INTO Battery (name, capacityKWh, chargePowerKW, dischargePowerKW, maxSoc, minDod, efficiency, opex) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        print(query)
        self.cursor.execute(query, (name,capacity,charge_power,discharge_power,max_soc,min_dod,efficiency,OPEX))
        self.connection.commit()

    def delete_battery_by_name(self, name):
        # Delete a battery entry by name from the Battery table
        query = "DELETE FROM Battery WHERE name = ?"
        self.cursor.execute(query, (name,))
        self.connection.commit()

    ###########################################################################
    ###########################################################################
    ###########################################################################

    def fetch_solarpanel_data(self):
        # Fetch all solar panel data from the SolarPanel table
        self.connect()
        try:
            self.cursor.execute("SELECT * FROM SolarPanel")
            solarpanel_data = self.cursor.fetchall()
            return solarpanel_data
        except sqlite3.Error as e:
            # Print error if fetching fails
            print("Error fetching solarpanel data:", e)

    def fetch_solarpanel_by_name(self, solarpanel_name):
        # Fetch solar panel data by name from the SolarPanel table
        query = "SELECT * FROM SolarPanel WHERE name = ?"
        self.cursor.execute(query, (solarpanel_name,))
        solarpanel_data = self.cursor.fetchone()
        return solarpanel_data
    
    def add_solarpanel(self, name, azimuth, tilt, numberOfPanels, length, width, efficiency, panelCapacity, invertorCapacity):
        # Add a new solar panel entry to the SolarPanel table
        query = "INSERT INTO SolarPanel (name, azimuth, tilt, numberOfPanels, length, width, efficiency, panelCapacity, invertorCapacity) VALUES (?,?,?,?,?,?,?,?,?)"
        self.cursor.execute(query, (name, azimuth, tilt, numberOfPanels, length, width, efficiency, panelCapacity, invertorCapacity))
        self.connection.commit()

    def delete_solarpanel_by_name(self, name):
        # Delete a solar panel entry by name from the SolarPanel table
        query = "DELETE FROM SolarPanel WHERE name = ?"
        self.cursor.execute(query, (name,))
        self.connection.commit()
        
    ###########################################################################
    ###########################################################################
    ###########################################################################

    def fetch_ev_charger_data(self):
        # Fetch all EV charger data from the EVCharger table
        self.connect()
        try:
            self.cursor.execute("SELECT * FROM EVCharger")
            ev_charger_data = self.cursor.fetchall()
            return ev_charger_data
        except sqlite3.Error as e:
            # Print error if fetching fails
            print("Error fetching EV charger data:", e)

    def fetch_ev_charger_by_name(self, ev_charger_name):
        # Fetch EV charger data by name from the EVCharger table
        query = "SELECT * FROM EVCharger WHERE name = ?"
        self.cursor.execute(query, (ev_charger_name,))
        ev_charger_data = self.cursor.fetchone()
        return ev_charger_data
    
    def add_ev_charger(self, name, chargePowerKW, fastChargePowerKW, efficiency, capacityCar):
        # Add a new EV charger entry to the EVCharger table
        query = "INSERT INTO EVCharger (name, chargePowerKW, fastChargePowerKW, efficiency, capacityCar) VALUES (?,?,?,?,?)"
        self.cursor.execute(query, (name, chargePowerKW, fastChargePowerKW, efficiency, capacityCar))
        self.connection.commit()

    def delete_ev_charger_by_name(self, name):
        # Delete an EV charger entry by name from the EVCharger table
        query = "DELETE FROM EVCharger WHERE name = ?"
        self.cursor.execute(query, (name,))
        self.connection.commit()
        
    ###########################################################################
    ###########################################################################
    ###########################################################################

    def fetch_heat_pump_data(self):
        # Fetch all heat pump data from the HeatPump table
        self.connect()
        try:
            self.cursor.execute("SELECT * FROM HeatPump")
            heat_pump_data = self.cursor.fetchall()
            return heat_pump_data
        except sqlite3.Error as e:
            # Print error if fetching fails
            print("Error fetching heat pump data:", e)

    def fetch_heat_pump_by_name(self, heat_pump_name):
        # Fetch heat pump data by name from the HeatPump table
        query = "SELECT * FROM HeatPump WHERE name = ?"
        self.cursor.execute(query, (heat_pump_name,))
        heat_pump_data = self.cursor.fetchone()
        return heat_pump_data
    
    def add_heat_pump(self, name, certificate, areaHouse, COP, desiredTemp):
        # Add a new heat pump entry to the HeatPump table
        query = "INSERT INTO HeatPump (name, certificate, areaHouse, COP, desiredTemp) VALUES (?,?,?,?,?)"
        self.cursor.execute(query, (name, certificate, areaHouse, COP, desiredTemp))
        self.connection.commit()

    def delete_heat_pump_by_name(self, name):
        # Delete a heat pump entry by name from the HeatPump table
        query = "DELETE FROM HeatPump WHERE name = ?"
        self.cursor.execute(query, (name,))
        self.connection.commit()
    
    ###########################################################################
    ###########################################################################
    ###########################################################################

    def fetch_simulation_data(self):
        # Fetch all simulation data from the Simulation table
        self.connect()
        try:
            self.cursor.execute("SELECT * FROM Simulation")
            simulation_data = self.cursor.fetchall()
            return simulation_data
        except sqlite3.Error as e:
            # Print error if fetching fails
            print("Error fetching simulation data:", e)

    def fetch_simulation_by_name(self, simulation_name):
        # Fetch simulation data by name from the Simulation table
        query = "SELECT * FROM Simulation WHERE name = ?"
        self.cursor.execute(query, (simulation_name,))
        simulation_data = self.cursor.fetchone()
        return simulation_data
    
    def add_simulation(
            self, 
            name,
            battery, 
            battery_charge,
            battery_discharge,
            battery_capacity,
            battery_efficiency,
            battery_opex,
            solar,
            solar_azimuth,
            solar_tilt,
            solar_number_of_panels,
            solar_efficiency,
            solar_length,
            solar_width,
            solar_cap,
            solar_inv_cap,
            ev,
            ev_charge,
            ev_number_of_cars,
            ev_efficiency,
            ev_distance_year,
            heat,
            heat_certificate,
            heat_area,
            heat_cop,
            heat_temp,
            consumer_profile,
            provider,
            general_latitude,
            general_longitude,
            general_start_date,
            use_api):
        # Add a new simulation entry to the Simulation table
        query = "INSERT INTO Simulation (name, battery, batteryCharge, batteryDischarge, batteryCapacity, batteryEfficiency, batteryOpex, solar, solarAzimuth, solarTilt, solarNumberOfPanels, solarEfficiency, solarLength, solarWidth, solarPanelCapacity, solarInvertorCapacity, ev, evCharge, evNumberOfCars, evEfficiency, evDistanceYear, heat, heatCertificate, heatArea, heatCOP, heatTemp, consumerProfile, provider, generalLatitude, generalLongitude, generalStartDate, useApi) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        
        self.cursor.execute(query, 
            (
            name,
            battery,
            battery_charge,
            battery_discharge,
            battery_capacity,
            battery_efficiency,
            battery_opex,
            solar,
            solar_azimuth,
            solar_tilt,
            solar_number_of_panels,
            solar_efficiency,
            solar_length,
            solar_width,
            solar_cap,
            solar_inv_cap,
            ev,
            ev_charge,
            ev_number_of_cars,
            ev_efficiency,
            ev_distance_year,
            heat,
            heat_certificate,
            heat_area,
            heat_cop,
            heat_temp,
            consumer_profile,
            provider,
            general_latitude,
            general_longitude,
            general_start_date,
            use_api))
        
        self.connection.commit()

    def delete_simulation_by_name(self, name):
        # Delete a simulation entry by name from the Simulation table
        query = "DELETE FROM Simulation WHERE name = ?"
        self.cursor.execute(query, (name,))
        self.connection.commit()