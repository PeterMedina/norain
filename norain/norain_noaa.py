import json
import os

from urllib.request import urlopen

forecast: str = json.load(
    urlopen("https://api.weather.gov/gridpoints/LOX/145,54/forecast"))


def is_day(data: str, pos: int):
    """Check if daytime

    Checks if conditions represent the day or night
    :param data: JSON string containing weather.gov data
    :param pos: The position of the weather forecast to check (0 indexed)
    :return: Bool
    """

    try:
        if data:
            is_day = data["properties"]["periods"][pos]["isDaytime"]
            if is_day:
                return True
            else:
                return False
    except Exception as e:
        print(e)


def advice(temp: int):
    """Give advice depending on weather conditions

    :param temp: Current temperature in degrees; assumes fahrenheit
    :return: Advice string
    """

    try:
        if temp:
            advice: str

            if temp < 50:
                advice = "You should consider bringing a jacket."
            elif temp >= 50 and temp < 70:
                advice = "You should consider bringing a sweater."
            elif temp >= 70 and temp < 85:
                advice = "Wearing layers wouldn't hurt."
            elif temp >= 80 and temp < 95:
                advice = "Keep cool and drink plenty of water."
            else:
                advice = "Limit outdoor activities and stay hydrated."

        return advice

    except Exception as e:
        print(e)


def make_forecast_json(data: str):
    """Generate custom forecast file in JSON format

    :param data: JSON string containing weather.gov data
    """

    try:
        if data:
            # Current conditions
            conditions_now: str = data["properties"]["periods"][0]

            # Determine where in the data object tomorrow's forecast will come from
            if is_day(data, 0):
                conditions_tomorrow: str = data["properties"]["periods"][2]
            else:
                conditions_tomorrow: str = data["properties"]["periods"][1]

            # Currently
            current_temperature: str = conditions_now["temperature"]
            current_wind: str = conditions_now["windSpeed"]
            current_advice: str = advice(current_temperature)

            # Tomorrow
            tomorrow_temperature: str = conditions_tomorrow["temperature"]
            tomorrow_wind: str = conditions_tomorrow["windSpeed"]
            tomorrow_advice: str = advice(tomorrow_temperature)

            weather_forecast: dict = {
                "current_conditions": "It's currently " + str(current_temperature) + "°f. " + current_advice + " Wind speeds are " + current_wind + ".",
                "tomorrow_conditions": "Tomorrow will be " + str(tomorrow_temperature) + "°f. " + tomorrow_advice + " Wind speeds will be " + tomorrow_wind + "."
            }

            # Convert forecast dict to JSON
            forecast_json = json.dumps(weather_forecast)

            # Save JSON file
            output_directory = os.path.sep.join(["json_output", "noaa"])
            forecast_file = open(
                os.path.sep.join(
                    [output_directory, "forecast.json"]), "w+"
            )
            forecast_file.write(forecast_json)
            forecast_file.close()

            return print("Forecast creation complete.")

    except Exception as e:
        print(e)


make_forecast_json(forecast)
