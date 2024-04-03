import csv

import numpy as np
from APIEntsoe import get_prices_data

def Calculate_injection_and_extraction_prices(pricing_data):
    prices_grid = []
    
    for data_point in pricing_data:
        prices_grid.append(float(data_point["price"]))
    
    prices_injection = [(0.85 * x) - 4 for x in prices_grid]
    prices_extraction = [(1.02 * x) + 4 for x in prices_grid]
    
    return prices_injection, prices_extraction


def process_prices_data(data_points, latitude, longitude):
    prices_data = get_prices_data(
        latitude, longitude, "2023-01-05T20:00:00Z"
    )
    
    reader = csv.DictReader(prices_data.splitlines())
    prices_list = list(reader)
    
    #pv_data = calculate_pv_power(forecast_list, latitude, longitude, capacity_kW, number_of_panels, azimuth, tilt, efficiency_panels, efficiency_invertor)
    prices_injection, prices_extraction = Calculate_injection_and_extraction_prices(prices_list)
    
    for i in range(len(data_points) - 1):
        data_points[i]["price_injection"] = float(prices_injection[i])
        data_points[i]["price_extraction"] = float(prices_extraction[i])
        
    return data_points