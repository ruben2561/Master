# batterij gaat nooit 100% opladen of ontladen
# aan de hand van de soc zal de oplading en ontlading anders worden
# efficiency dus als we in theorie 100% geladen zijn gaat dit minder zijn
# verschil ac en dc laden toevoegen
# 
# 
# 

class Battery:
    def __init__(self, capacity, soc, charge_power, discharge_power, max_soc, min_dod, efficiency):
        self.capacity = capacity  # in kWh
        self.charge_power = charge_power  # in kW
        self.discharge_power = discharge_power  # in kW
        self.max_soc = max_soc  # Maximum State of Charge in percentage (e.g., 1 for fully charged)
        self.min_dod = min_dod  # Minimum Depth of Discharge in percentage (e.g., 1 for fully charged)
        self.efficiency = efficiency
        self.soc = 1  # in kWh, current charge level of the battery

        if(self.efficiency > 1):
            self.efficiency = self.efficiency/100


    # TODO here still need to change error with the efficincy
    def charge(self, power, time):
        """
        Simulate the charging of the battery while considering limitations.
        power: charging power in kW
        time: charging time in hours
        """
        if(self.capacity == 0):
            return 0, time * power
        
        new_power = power
        if self.charge_power <= new_power : new_power = self.charge_power # make sure the power is not above the max charge power
        
        efficiency = self._calculate_efficiency_factor()
        
        time_max = ((self.capacity*self.max_soc)-self.soc) / (new_power * efficiency) # max time battery can charge until full
        
        if(time_max >= 1):
            self.soc += time * new_power * efficiency
            return time * new_power * efficiency, 0
        
        elif(time_max <= 1):
            self.soc += time_max * new_power * efficiency
            return time_max * new_power * efficiency, (time-time_max) * power

    def discharge(self, power, time):
        """
        Simulate the discharging of the battery while considering limitations.
        power: discharging power in kW
        time: discharging time in hours
        """
        if(self.capacity == 0):
            return 0, time * power
        
        new_power = power
        if self.discharge_power <= new_power : new_power = self.discharge_power # make sure the power is not above the max charge power
        
        efficiency = self._calculate_efficiency_factor()
        
        time_max = (self.soc - (self.capacity * self.min_dod)) / (new_power * efficiency) # max time battery can discharge until empty
        
        if(time_max >= 1):
            self.soc -= time * new_power * efficiency
            return time * new_power * efficiency, 0
        
        elif(time_max < 1):
            self.soc -= time_max * new_power * efficiency
            return time_max * new_power * efficiency, (time-time_max) * power
        
    def _calculate_efficiency_factor(self):
        """
        Calculate the efficiency factor based on the state of charge (SoC).
        """
        soc_ratio = self.soc / (self.capacity * self.max_soc)
        return self.efficiency - soc_ratio * (1 - 0.9)  # Example nonlinear efficiency curve

    def get_soc(self):
        """
        Get the current state of charge (SoC) of the battery.
        """
        return self.soc

    def is_full(self):
        """
        Check if the battery is fully charged.
        """
        return self.soc >= 1.0
    
    def get_max_charge(self):
        return self.charge_power
    
    def get_max_discharge(self):
        return self.discharge_power

    def is_empty(self):
        """
        Check if the battery is fully discharged.
        """
        return self.soc <= 0.0
    
