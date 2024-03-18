import pybamm

class PyBaMM_Battery:
    def __init__(self, capacity, soc, charge_power, discharge_power, max_soc, min_dod, efficiency):
        #self.capacity = capacity  # in kWh
        #self.soc = soc  # current state of charge
        #self.charge_power = charge_power  # in kW
        #self.discharge_power = discharge_power  # in kW
        #self.max_soc = max_soc  # Maximum State of Charge in percentage
        #self.min_dod = min_dod  # Minimum Depth of Discharge in percentage
        #self.efficiency = efficiency  # efficiency
        self.instructions = []

        model = pybamm.lithium_ion.DFN()
        parameter_values = pybamm.ParameterValues("Chen2020")

        parameter_values["Nominal cell capacity [A.h]"] = capacity
        parameter_values["Open-circuit voltage at 0% SOC [V]"] = 2.5
        parameter_values["Open-circuit voltage at 100% SOC [V]"] = 4.2
        #parameter_values["Typical current [A]"] = 5
        parameter_values["Nominal cell capacity [A.h]"] = capacity

        """ self.parameter_values = {
        'Nominal cell capacity [A.h]': capacity,
        'Open-circuit voltage at 0% SOC [V]': 2.5,
        'Open-circuit voltage at 100% SOC [V]':  4.2,
        'Typical current [A]': 5,
        'Reference temperature [K]': 298.15,
        } """

        # Create PyBaMM parameter
        #self.parameters = pybamm.ParameterValues(chemistry=pybamm.parameter_sets.LithiumIon)
        #self.parameters.update(parameter_values)

        self.model = pybamm.lithium_ion.DFN()
        
    
    def charge(self, power, time):
        new_instruction = "Charge at {}W for {} hours".format(power*1000, time)
        #print(new_instruction + str(self.soc))
        self.instructions.append(new_instruction)
        return
    
    def discharge(self, power, time):
        new_instruction = "Discharge at {}W for {} hours".format(power*1000, time)
        print(new_instruction)
        self.instructions.append(new_instruction)
        return
    
    def simulation(self):
        #print(self.instructions)

        experiment_instructions = [(instruction,) for instruction in self.instructions]

        #print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        #print(experiment_instructions)

        """ experiment = pybamm.Experiment([
            tuple(self.instructions)  # Assuming 'instructions' is your list of instructions
        ]) """

        experiment = pybamm.Experiment(experiment_instructions)

        self.sim = pybamm.Simulation(self.model, experiment=experiment)
        self.sim.solve()
        self.sim.plot()
        
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