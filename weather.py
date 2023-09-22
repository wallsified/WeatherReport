import requests
import os
import time

API_KEY = os.environ.get("API_KEY")

cache = dict()

def weather_request(lat, long):
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


def get_weather(lat, long):
    weather = cache.get((lat, long))
    if weather == None or (time.time() - weather["age"] > 60*60*3):
        data = weather_request(lat, long)
        data["age"] = time.time()
        cache[(lat, long)] = data

    return cache[(lat, long)]
