import csv

import numpy as np
from APIPrices import get_prices_data

def Calculate_injection_and_extraction_prices(pricing_data):
    prices_grid = [float(data_point["price"]) for data_point in pricing_data if float(data_point["price"]) >= 0]
    average_price = sum(prices_grid) / len(prices_grid)
    
    prices_grid = [float(data_point["price"]) if float(data_point['price']) > 10 else 10 for data_point in pricing_data]
    
    prices_injection = []
    prices_extraction = []
    
    for x in prices_grid:
        if x >= 10:
            prices_injection.append(0.85 * x - 4)
            prices_extraction.append(1.02 * x + 4)
        else:
            prices_injection.append(0.85 * 10 - 4)
            prices_extraction.append(1.02 * 10 + 4)
    
    return {
        "prices_injection": prices_injection, 
        "prices_extraction": prices_extraction,
    }

def process_prices_data(data_points, latitude, longitude):
    prices_data = get_prices_data(
        latitude, longitude, "2023-01-05T20:00:00Z"
    )
    
    reader = csv.DictReader(prices_data.splitlines())
    prices_list = list(reader)
    
    prices = Calculate_injection_and_extraction_prices(prices_list)
    
    for i in range(len(data_points) - 1):
        data_points[i]["price_injection"] = float(prices["prices_injection"][i])
        data_points[i]["price_extraction"] = float(prices["prices_extraction"][i])
    
    return data_points