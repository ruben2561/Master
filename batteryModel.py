# 
# test klasse
#
#


class BatteryModel:
    def __init__(self, capacity, efficienty):
        self.capacity = capacity  # in kWh
        self.efficienty = efficienty
        self.soc = 0  # in kWh, current charge level of the battery