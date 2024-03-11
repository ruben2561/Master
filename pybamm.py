import pybamm

class PyBaMM_Battery:
    def __init__(self, capacity, soc, charge_power, discharge_power, max_soc, min_dod, efficiency):
        self.capacity = capacity  # in kWh
        self.soc = soc  # current state of charge
        self.charge_power = charge_power  # in kW
        self.discharge_power = discharge_power  # in kW
        self.max_soc = max_soc  # Maximum State of Charge in percentage
        self.min_dod = min_dod  # Minimum Depth of Discharge in percentage
        self.efficiency = efficiency  # efficiency

        parameter_values = {
        'Nominal cell capacity [A.h]': capacity,
        'Open-circuit voltage at 0% SOC [V]': 2.5,
        'Open-circuit voltage at 100% SOC [V]':  4.2,
        'Typical current [A]': 5,
        'Reference temperature [K]': 298.15,
        }

        # Create PyBaMM parameter
        parameters = pybamm.ParameterValues(chemistry=pybamm.parameter_sets.LithiumIon)
        parameters.update(parameter_values)

        model = pybamm.lithium_ion.DFN()
        sim_solver = pybamm.CasadiSolver()
        self.sim = pybamm.Simulation(model, parameter_values=parameters, solver=sim_solver)
        
    
    def charge(self, power, time):
        return
    
    def discharge(self, power, time):
        return
    
    





""" 
"Discharge at 1C for 0.5 hours",
"Discharge at C/20 for 0.5 hours",
"Charge at 0.5 C for 45 minutes",
"Discharge at 1 A for 90 seconds",
"Charge at 200mA for 45 minutes",
"Discharge at 1 W for 0.5 hours",
"Charge at 200 mW for 45 minutes",
"Rest for 10 minutes",
"Hold at 1 V for 20 seconds",
"Charge at 1 C until 4.1V",
"Hold at 4.1 V until 50 mA",
"Hold at 3V until C/50", 
"""