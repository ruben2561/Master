import csv
import datetime
import pandas as pd
from entsoe import EntsoePandasClient
from nordpool.elspot import Prices

# Function to get sample data prices from a CSV file
def get_sample_data_prices():
    try:
        # Open the sample data file
        with open("sampleData/prices_2023.csv", "r") as file:
            sample_data = file.read()
            reader = csv.DictReader(sample_data.splitlines())
            # Extract the price values from the CSV data
            price_values = [float(entry['price']) for entry in reader]
            return price_values
    except Exception as e:
        # Print an error message if reading fails
        print(f"Error reading sample data prices: {e}")
        return None

# Function to get prices data for a given time and source
def get_prices_data(time, source):
    try:
        try:
            # Attempt to read pre-loaded data for the specified date range
            df = pd.read_csv('sampleData/prices_2017-2024.csv')

            # Parse the provided time and calculate the end date
            start_date = datetime.datetime.strptime(time, "%Y-%m-%d")
            end_date = start_date + datetime.timedelta(days=365)

            # Format the date strings
            start_date_string = str(start_date).replace(' 00:00:00', 'T00:00:00Z')
            end_date_string = str(end_date).replace(' 00:00:00', 'T00:00:00Z')

            # Find the corresponding indices in the DataFrame
            start_index = df.index[df['timestamp'] == start_date_string].tolist()
            end_index = df.index[df['timestamp'] == end_date_string].tolist()

            # Slice the DataFrame to get the relevant price data
            df = df["price"]
            df = df[start_index[0] + 2:end_index[0] + 1]

            return df

        except Exception:
            # If data loading fails, proceed to fetch from external sources
            if source == "entsoe":
                # Fetch data from the Entsoe API
                time = datetime.datetime.strptime(time, "%Y-%m-%d")
                start = pd.Timestamp(year=time.year, month=time.month, day=time.day, tz='CET')
                end = start + datetime.timedelta(days=365)

                # Create a client for the Entsoe API
                api_key = "9d3e8de4-4330-4f77-b406-e4fca462f8a7"
                client = EntsoePandasClient(api_key=api_key)
                da_prices = pd.DataFrame()

                try:
                    # Query the day-ahead prices from the Entsoe API
                    da_prices = client.query_day_ahead_prices('BE', start=start, end=end)
                    return da_prices
                except Exception:
                    # Print an error message if the API call fails
                    print(f"No data from Entsoe: between {start} and {end}")
                    return get_sample_data_prices()

            if source == "nordpool":
                # Fetch data from the Nordpool API
                prices_spot = Prices()
                start = datetime.datetime.strptime(time, "%Y-%m-%d")
                start = pd.Timestamp(start).tz_localize('CET')
                hourly_prices_spot = prices_spot.hourly(areas=['BE'], end_date=start)
                hourly_values = hourly_prices_spot['areas']['BE']['values']
                
                # Convert the list of dictionaries to a DataFrame
                df = pd.DataFrame(hourly_values)

                # Format the timestamp and price columns
                df['timestamp'] = df['start'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
                df['price'] = df['value']

                # Select only the required columns
                df = df[['price', 'timestamp']]

                return df

    except Exception as e:
        # Print an error message if any exception occurs
        print(f"Error: {e}")
        return get_sample_data_prices()
