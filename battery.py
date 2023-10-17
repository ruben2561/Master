class LiFePO4Battery:
    def __init__(self, voltage=51.2, capacity=2.5, efficiency=0.95):
        """
        Initialize the LiFePO4 battery simulation.
        
        Parameters:
        - voltage: Nominal voltage of the battery (V)
        - capacity: Total energy capacity of the battery (kWh)
        - efficiency: Efficiency of the battery (0 to 1, where 1 is 100% efficient)
        """
        self.nominal_voltage = voltage
        self.capacity = capacity * 3600 * 1000  # Convert kWh to Wh
        self.efficiency = efficiency
        self.soc = 1.0  # Start with a fully charged battery (SoC of 1)

    def charge(self, power, time):
        """
        Simulate charging the battery.
        
        Parameters:
        - power: Charging power (W)
        - time: Charging duration (hours)
        """
        # Calculate the amount of energy added to the battery
        energy_in = power * time * self.efficiency
        # Update state of charge
        self.soc = min(1.0, self.soc + (energy_in / self.capacity))

    def discharge(self, power, time):
        """
        Simulate discharging the battery.
        
        Parameters:
        - power: Discharging power (W)
        - time: Discharging duration (hours)
        """
        # Calculate the amount of energy taken from the battery
        energy_out = power * time / self.efficiency
        # Update state of charge
        self.soc = max(0.0, self.soc - (energy_out / self.capacity))

    def get_voltage(self):
        """
        Get the current voltage of the battery.
        """
        return self.nominal_voltage * self.soc

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

# Example usage:
if __name__ == "__main__":
    battery = LiFePO4Battery()
    print("Initial SoC:", battery.get_soc())

    # Discharging the battery
    battery.discharge(500, 1)  # Discharging at 500W for 1 hour
    print("SoC after discharging:", battery.get_soc())

    # Charging the battery
    battery.charge(1000, 2)  # Charging at 1000W for 2 hours
    print("SoC after charging:", battery.get_soc())

    
