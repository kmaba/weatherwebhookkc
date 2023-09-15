import requests
import datetime
import time

# Replace with your OpenWeatherMap API key
api_key = "5628c7dd3703a739cf10c3d5709d257f"

# Function to get weather data
def get_weather_data():
    # Replace with the coordinates of Kewdale, WA
    latitude = -31.9781
    longitude = 115.9556

    # OpenWeatherMap API endpoint for current weather data
    weather_api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"

    response = requests.get(weather_api_url)
    data = response.json()
    return data

def post_to_discord(data, next_update_time=None):
    # Replace this with your new Discord webhook URL
    webhook_url = "https://discord.com/api/webhooks/1152081939692531792/ge9OfoVVONFOVL_n1HOjMsS_wAThanFyS8d_9wEfv5CD9qZnOnhiQKYU1ED5Dwf93bdx"

    # Extract temperature information from the API response
    if "main" in data and "temp" in data["main"]:
        temperature_kelvin = data["main"]["temp"]
        temperature_celsius = temperature_kelvin - 273.15  # Convert from Kelvin to Celsius
        temperature_formatted = f"{temperature_celsius:.2f}°C"
    else:
        temperature_formatted = "N/A"

    # Extract weather condition, wind speed, and other relevant data
    if "weather" in data and len(data["weather"]) > 0 and "description" in data["weather"][0]:
        condition = data["weather"][0]["description"]
    else:
        condition = "N/A"

    if "wind" in data:
        wind_speed = data["wind"]["speed"]
        wind_speed_formatted = f"{wind_speed}km/h"
        wind_direction_degrees = data["wind"]["deg"]
        wind_direction_cardinal = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"][round(wind_direction_degrees / 45) % 8]
    else:
        wind_speed_formatted = "N/A"
        wind_direction_cardinal = "N/A"

    # Get the current date in AWST (Australian Western Standard Time)
    current_time_utc = datetime.datetime.utcnow()
    current_time_awst = current_time_utc + datetime.timedelta(hours=8)
    current_date_awst_str = current_time_awst.strftime("%A %d %B")

    # Format the message with the corrected temperature, condition, wind speed, and additional line
    message_parts = [
        f"{current_date_awst_str}:",
        f"Expected {condition} with a top of {temperature_formatted}",
        f"Wind speeds of around {wind_speed_formatted} expected from the {wind_direction_cardinal}, insha'allah.",
        "Take a look for yourself 😁: <https://openweathermap.org/city/2063523>"
    ]

    if next_update_time is not None:
        message_parts.append(f"Next weather message is <t:{next_update_time}:R>")

    message_parts.append("ᵐᵃᵈᵉ ᵇʸ ᵃᵇᵈᵘˡˡᵃʰ ᵃʳᵃᶠᵃᵗ")
    
    message = "\n".join(message_parts)

    payload = {
        "content": message,
        "allowed_mentions": {
            "parse": []
        }
    }

    response = requests.post(webhook_url, json=payload)

    # Check if the message was posted successfully
    if response.status_code == 200:
        print(f"Message posted successfully. Status code: {response.status_code}")
    else:
        return

# Main function
def main():
    weather_data = get_weather_data()
    
    # Calculate the timestamp for the next run
    current_time_utc = datetime.datetime.utcnow()
    next_run_time_utc = current_time_utc + datetime.timedelta(days=1)
    
    post_to_discord(weather_data, int(next_run_time_utc.timestamp()))

if __name__ == "__main__":
    main()
