import requests
from dotenv import load_dotenv
import os

load_dotenv()

SHEETY_ENDPOINT = 'https://api.sheety.co/bc6f38f6543a11b5cfa609fc810f343a/joelsFlightSheet/prices'

class DataManager:

    def __init__(self):
        self.get_url = SHEETY_ENDPOINT
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('SHEET_AUTH')}"
        }
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(self.get_url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.text)

