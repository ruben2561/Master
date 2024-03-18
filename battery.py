# batterij gaat nooit 100% opladen of ontladen
# aan de hand van de soc zal de oplading en ontlading anders worden
# efficienty dus als we in theorie 100% geladen zijn gaat dit minder zijn
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
        #self.max_charge_current = max_charge_current  # in A
        self.efficienty = efficiency
        self.soc = soc  # in kWh, current charge level of the battery

    def charge(self, power, time):
        """
        Simulate the charging of the battery while considering limitations.
        power: charging power in kW
        time: charging time in hours
        """
        if self.charge_power<=power: power = self.charge_power # make sure the power is not above the max charge power

        energy_added = power * time

        if(self.soc + energy_added <= self.capacity * (self.max_soc)):
            self.soc = self.soc + energy_added
            return 0
        else:
            self.soc = self.capacity * (self.max_soc)
            return  (energy_added - ((self.capacity * self.max_soc) - self.soc))

    def charge_kWh(self, energy):
        """
        Simulate the charging of the battery while considering limitations.
        energy: kWh
        """
        if(self.soc + energy <= self.capacity * (self.max_soc)):
            self.soc = self.soc + energy
            return 0
        else:
            self.soc = self.capacity * (self.max_soc)
            return  (energy - ((self.capacity * self.max_soc) - self.soc))

    def discharge(self, power, time):
        """
        Simulate the discharging of the battery while considering limitations.
        power: discharging power in kW
        time: discharging time in hours
        """
        if self.discharge_power<=power: power = self.discharge_power # make sure the power is not above the max discharge charge power

        energy_consumed = power * time

        if(self.soc - energy_consumed >= self.capacity * (self.min_dod)):
            self.soc = self.soc - energy_consumed
            return 0
        else:
            self.soc = self.capacity * (self.min_dod)
            return  (energy_consumed - (self.soc - self.capacity * (self.min_dod)))

    def discharge_kWh(self, energy):
        """
        Simulate the discharging of the battery while considering limitations.
        energy: kWh
        """
        if(self.soc - energy >= self.capacity * (self.min_dod)):
            self.soc = self.soc - energy
            return 0
        else:
            self.soc = self.capacity * (self.min_dod)
            return  (energy - (self.soc - self.capacity * (self.min_dod)))

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

    def is_empty(self):
        """
        Check if the battery is fully discharged.
        """
        return self.soc <= 0.0
    
