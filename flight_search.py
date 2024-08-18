import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()

TOKEN_ENDPOINT = 'https://test.api.amadeus.com/v1/security/oauth2/token'
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"

# current_date = datetime.now()
# tomorrow = current_date + timedelta(1)
# tomorrow_formatted = tomorrow.strftime("%Y-%m-%d")
# six_months = tomorrow + timedelta(days=180)
# six_months_formatted = six_months.strftime("%Y-%m-%d")

class FlightSearch:

    def __init__(self):
        self.amadeus_api = os.getenv('AMADEUS_API')
        self.amadeus_secret = os.getenv('AMADEUS_SECRET')
        self._token = self._get_new_token()

    def _get_new_token(self):
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body = {
            "grant_type": "client_credentials",
            "client_id": self.amadeus_api,
            "client_secret": self.amadeus_secret
        }

        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)
        response.raise_for_status()
        return response.json()['access_token']

    def get_destination_code(self, city_name):
        headers = {
            'Authorization': f'Bearer {self._token}'
        }
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }
        response = requests.get(url=IATA_ENDPOINT, headers=headers, params=query)

        print(f"Status code {response.status_code}. Airport IATA: {response.text}")
        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"

        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        # print(f"Using this token to check_flights() {self._token}")
        headers = {"Authorization": f"Bearer {self._token}"}
        # query = {
        #     "originLocationCode": origin_city_code,
        #     "destinationLocationCode": destination_city_code,
        #     "departureDate": from_time.strftime("%Y-%m-%d"),
        #     "returnDate": to_time.strftime("%Y-%m-%d"),
        #     "adults": 1,
        #     "nonStop": "true",
        #     "currencyCode": "GBP",
        #     "max": "10",
        # }

        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
            "max": "10",
        }

        response = requests.get(
            url=FLIGHT_ENDPOINT,
            headers=headers,
            params=query,
        )

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()



