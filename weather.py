import requests

import os
import time
import json

API_KEY = os.environ.get("API_KEY")

class WeatherManager():

    def __init__(self, data_manager):
        self.cache = dict()
        self.data_manager = data_manager

    def request(self, iata):
        lat, long = self.data_manager.get_coords(iata)
        data = requests.get(
                "https://api.openweathermap.org/data/2.5/forecast",
                params = {
                    "lat": str(lat),
                    "lon": str(long),
                    "appid": API_KEY,
                    "lang": "es",
                    "units": "metric"
                    }
                )

        return data.json()


    def get(self, iata):
        if len(self.cache) == 0 and os.path.exists("cache.json"):
            file = open("cache.json")
            self.cache = json.load(file)
            file.close()

        weather = self.cache.get(iata)
        if weather == None or (time.time() - weather["age"] > 60*60*3):
            data = self.request(iata)
            data["age"] = time.time()
            self.cache[iata] = data
            file = open("cache.json", "w")
            json.dump(self.cache, file, indent=4)
            file.close()

        return self.cache[iata]
