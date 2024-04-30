import sys
import pandas as pd
from entsoe import EntsoePandasClient
import datetime
from nordpool.elspot import Prices

def get_sample_data_prices():
    try:
        with open("sampleData/prices_2023.csv", "r") as file:
            sample_data = file.read()
            return sample_data
    except Exception as e:
        print(f"Error reading sample data prices: {e}")
        return None

def get_prices_data(latitude, longitude, time, source):
    try:
        
        raise Exception("Prices api doesnt work yet")
    
        if source == "entsoe":
            # Parse the input date string to a datetime object
            start = datetime.datetime.strptime(time, "%Y-%m-%d")
            start = pd.Timestamp(start).tz_localize('CET')
            
            # Calculate end date one year further
            end = start + datetime.timedelta(days=1)
            end = pd.Timestamp(end).tz_localize('CET') if end.tzinfo is None else end.tz_convert('CET')

            api_key = "9d3e8de4-4330-4f77-b406-e4fca462f8a7"
            client = EntsoePandasClient(api_key=api_key)
            da_prices = pd.DataFrame()
            
            try:
                da_prices = client.query_day_ahead_prices(
                    'BE', start=start, end=end)
            except Exception as e:
                print(f"No data from Entsoe: between {start} and {end}, {e}")
                return get_sample_data_prices()
        
        if source == "nordpool":
            # ophalen bij Nordpool
            prices_spot = Prices()
            start = datetime.datetime.strptime(time, "%Y-%m-%d")
            start = pd.Timestamp(start).tz_localize('CET')
            hourly_prices_spot = prices_spot.hourly(areas=['BE'], end_date=start)
            hourly_values = hourly_prices_spot['areas']['BE']['values']
            # Convert the list of dictionaries to a DataFrame
            df = pd.DataFrame(hourly_values)

            # Assuming 'start' is the relevant timestamp
            df['timestamp'] = df['start'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            df['price'] = df['value']

            # Select only the required columns
            df = df[['price', 'timestamp']]

            return df
    
    except Exception as e:
        print(f"Error: {e}")
        return get_sample_data_prices()
    

# # Example usage
# if __name__ == "__main__":
#     # Example latitude and longitude for Berlin
#     latitude = 52.5200
#     longitude = 5.4050

#     # Get day-ahead prices for the specified location
#     prices_df = get_prices_data(latitude, longitude, "2023-01-01", "entsoe")

#     # Check if prices are retrieved successfully
#     if prices_df is not None:
#         # Display the retrieved prices DataFrame
#         print("Day-ahead prices:")
#         print(prices_df)
#     else:
#         print("Failed to retrieve day-ahead prices.")