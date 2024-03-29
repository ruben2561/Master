import pandas as pd
from entsoe import EntsoePandasClient
import datetime

class dayAheadPricesAPI:
    def __init__(self):
        self = self

    def get_day_ahead_prices(self, latitude, longitude):
        now = datetime.datetime.now()
        start = pd.Timestamp(year=now.year, month=now.month, day=now.day, tz='CET')
        if now.hour < 12:
            end = start + datetime.timedelta(days=1)
        else:
            end = start + datetime.timedelta(days=2)

        start = pd.Timestamp(year=start.year, month=start.month, day=start.day, tz='CET')
        end = pd.Timestamp(year=end.year, month=end.month, day=end.day, tz='CET')
        api_key = self.config.get(["prices", "entsoe-api-key"])
        client = EntsoePandasClient(api_key=api_key)
        da_prices = pd.DataFrame()
        try:
            da_prices = client.query_day_ahead_prices(
                f'{latitude},{longitude}', start=start, end=end)
        except Exception as e:
            print(f"No data from Entsoe: between {start} and {end}")
            return None

        return da_prices
    

# Example usage
if __name__ == "__main__":
    # Example latitude and longitude for Berlin
    latitude = 52.5200
    longitude = 13.4050

    # Create an instance of the dayAheadPricesAPI class
    api = dayAheadPricesAPI()

    # Get day-ahead prices for the specified location
    prices_df = api.get_day_ahead_prices(latitude, longitude)

    # Check if prices are retrieved successfully
    if prices_df is not None:
        # Display the retrieved prices DataFrame
        print("Day-ahead prices for Berlin:")
        print(prices_df)
    else:
        print("Failed to retrieve day-ahead prices.")