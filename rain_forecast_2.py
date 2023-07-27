import datetime
import requests
import geocoder
import os

class WeatherForecast:
    def __init__(self):
        self.forecast_data = {}
        self.file_path = "weather.txt"
        self.read_result()

    def __setitem__(self, key, value):
        self.forecast_data[key] = value
        self.save_result()

    def __getitem__(self, key):
        return self.forecast_data[key]

    def __iter__(self):
        return iter(self.forecast_data)
    
    def items(self):
        for (city, date), precipitation in self.forecast_data.items():
            yield (date, precipitation)

    def save_result(self):
        with open(self.file_path, "w") as fd:
            for (city, date), precipitation in self.forecast_data.items():
                fd.write(f"{city}:{date}:{precipitation}\n")

    def read_result(self):
        if os.path.exists(self.file_path):
            with open(self.file_path) as fd:
                for line in fd:
                    city, date, precipitation = line.strip().split(":")
                    self.forecast_data[(city, date)] = float(precipitation)

def date():
    today = datetime.date.today()
    input_date = input("Enter a date(YYYY-MM-DD) or press 'enter' for tomorrow: ")

    if input_date == "":
        searched_date = today + datetime.timedelta(days=1)
    else:
        try:
            searched_date = datetime.datetime.strptime(input_date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format")
            exit()
        
    return searched_date.strftime("%Y-%m-%d")

def location(city):
    g = geocoder.osm(city)

    return g.latlng

def weather(latitude, longitude, searched_date):
    endpoint_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}"
    response = requests.get(endpoint_url)

    if response.status_code == 200:
        weather_data = response.json()
        precipitation = weather_data["daily"]["precipitation_sum"][0]

        return precipitation
    else:
        return None

def result(prediction):
    try:
        prediction = float(prediction)
    except ValueError:
        return "I don't know"

    if prediction > 0.0:
        return "It will rain"
    elif prediction == 0.0:
        return "It will not rain"
    else:
        return "I don't know"

def main():
    weather_forecast = WeatherForecast()

    searched_date = date()
    city = input("Enter a city: ").lower()

    if city == "":
        print("Please enter a city!")
        exit()

    latitude, longitude = location(city)

    if latitude is None or longitude is None:
        print("Invalid city")
        exit()

    if (city, searched_date) not in weather_forecast:
        prediction = weather(latitude, longitude, searched_date)
        prediction = float(prediction)
        prediction_result = result(prediction)

        print("*****************************************")
        print(f"City: {city}        Date: {searched_date}")
        print(f"{prediction_result}")
        print(f"The precipitation value: {prediction}")
        print("*****************************************")

        weather_forecast[(city, searched_date)] = prediction
    else:
        prediction = weather_forecast[(city, searched_date)]
        prediction_result = result(prediction)
        print("*****************************************")
        print(f"City: {city}        Date: {searched_date}")
        print(f"{prediction_result}")
        print(f"The precipitation value: {prediction}")
        print("*****************************************")

if __name__ == "__main__":
    main()
