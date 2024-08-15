import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight

# ==================== Set up the Flight Search ====================

data_manager = DataManager()
flight_search = FlightSearch()
sheet_data = data_manager.get_destination_data()

# Set your origin airport
ORIGIN_CITY_IATA = "LON"

# ==================== Update the Airport Codes in Google Sheet ====================

# for row in sheet_data:
#     if row["iataCode"] == "":
#         row["iataCode"] = flight_search.get_destination_code(row['city'])
#         time.sleep(2)
# print(f"sheet_data:\n {sheet_data}")
#
# data_manager.destination_data = sheet_data
# data_manager.update_destination_codes()

# ==================== Search for Flights ====================

tomorrow = datetime.now() + timedelta(days=1)
week_from_tomorrow = datetime.now() + timedelta(days=7)

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=week_from_tomorrow
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: £{cheapest_flight.price}")
    # Slowing down requests to avoid rate limit
    time.sleep(2)

















