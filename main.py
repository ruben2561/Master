#todo
#add the solcast api and try showing wheater
#add the fluvius live prices and try to show it
#make a little ui to showcase everything instead of console
#Peukert's law or the coulombic efficiency model bekijken
#add more items like battery and try to make them work together
#
#
from battery import Battery  

if __name__ == "__main__":
    battery = Battery(capacity=2.5, charge_power=1.0, discharge_power=1.2, max_soc=0.9, min_dod=0.1, max_charge_current=15, efficienty=0.95)
    print(f"Initial battery charge: {battery.soc} kWh")

    # Charging the battery
    battery.charge(1.2, 2)  # charging at 0.8 kW for 2 hours
    print(f"Battery charge after charging: {battery.soc} kWh")

    # Discharging the battery
    battery.discharge(1.0, 1.5)  # discharging at 1.2 kW for 1.5 hours
    print(f"Battery charge after discharging: {battery.soc} kWh")