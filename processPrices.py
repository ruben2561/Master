import csv
from datetime import datetime

import numpy as np
from APIPrices import get_prices_data

def calculate_injection_and_offtake_prices(pricing_data, provider):
    prices_grid = pricing_data
    
    prices_injection = []
    prices_offtake = []
    
    for x in prices_grid:
        if provider == "Ecopower":
            prices_injection.append(0.85 * x - 4)
            prices_offtake.append(1.02 * x + 4)
        elif provider == "Engie Dynamic":
            prices_injection.append(x)
            prices_offtake.append(x + 2.04)
        elif provider == "Octa+Dynamic":
            prices_injection.append(0.988 * x - 16.83)
            prices_offtake.append(1.038 * x + 3.93)
    
    return {
        "prices_injection": prices_injection, 
        "prices_offtake": prices_offtake,
    }

def process_prices_data(data_points, start_date, provider):
    
    prices_data = get_prices_data(
        start_date, "entsoe"
    )

    prices_list = list(prices_data)
    
    #print(prices_list)
    
    prices = calculate_injection_and_offtake_prices(prices_list, provider)
    
    for i in range(len(data_points) - 1):
        data_points[i]["price_injection"] = float(prices["prices_injection"][i])
        data_points[i]["price_offtake"] = float(prices["prices_offtake"][i])
    
    return data_points