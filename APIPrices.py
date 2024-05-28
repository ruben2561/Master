import csv
import datetime
import pandas as pd
import sys
from entsoe import EntsoePandasClient
from nordpool.elspot import Prices


def get_sample_data_prices():
    try:
        with open("sampleData/prices_2023.csv", "r") as file:
            sample_data = file.read()
            reader = csv.DictReader(sample_data.splitlines())
            price_values = [float(entry['price']) for entry in reader]
            return price_values
    except Exception as e:
        print(f"Error reading sample data prices: {e}")
        return None


def get_prices_data(time, source):
    try:
        try:
            # check if data for this date is already loaded 
            df = pd.read_csv('sampleData/prices_2017-2024.csv')

            start_date = datetime.datetime.strptime(time, "%Y-%m-%d")
            end_date = start_date + datetime.timedelta(days=365)

            start_date_string = str(start_date).replace(' 00:00:00', 'T00:00:00Z')
            end_date_string = str(end_date).replace(' 00:00:00', 'T00:00:00Z')

            start_index = df.index[df['timestamp'] == start_date_string].tolist()
            end_index = df.index[df['timestamp'] == end_date_string].tolist()

            df = df["price"]
            df = df[start_index[0] + 2:end_index[0] + 1]

            return df

        except Exception:

            if source == "entsoe":
                time = datetime.datetime.strptime(time, "%Y-%m-%d")
                start = pd.Timestamp(year=time.year, month=time.month, day=time.day, tz='CET')
                end = start + datetime.timedelta(days=365)

                start = pd.Timestamp(year=start.year, month=start.month, day=start.day, tz='CET')
                end = pd.Timestamp(year=end.year, month=end.month, day=end.day, tz='CET')
                api_key = "9d3e8de4-4330-4f77-b406-e4fca462f8a7"
                client = EntsoePandasClient(api_key=api_key)
                da_prices = pd.DataFrame()

                try:
                    da_prices = client.query_day_ahead_prices('BE', start=start, end=end)
                    return da_prices
                except Exception:
                    print(f"Geen data van Entsoe: tussen {start} en {end}")
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
#     # Get day-ahead prices for the specified location
#     prices_df = get_prices_data("2023-01-01", "entsoe")

#     # Check if prices are retrieved successfully
#     if prices_df is not None:
#         # Display the retrieved prices DataFrame
#         print("Day-ahead prices:")
#         #print(prices_df)
#     else:
#         print("Failed to retrieve day-ahead prices.")
