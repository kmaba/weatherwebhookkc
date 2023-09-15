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

    # OpenWeatherMap One Call API endpoint for forecast data
    weather_api_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude=current,minutely,hourly,alerts&appid={api_key}"

    response = requests.get(weather_api_url)
    data = response.json()
    return data

def post_to_discord(data, next_update_time=None):
    # Replace this with your new Discord webhook URL
    webhook_url = "https://discord.com/api/webhooks/1152075250931073135/-AOJcH8y5KHn5A6yXvk5vmG0eGeL4_DGr2PLrtESLBXnllIvVkM4_WfoXCjbvcHbngdW"

    # Extract temperature information from the API response
    if "daily" in data and len(data["daily"]) > 0:
        temperature_high_kelvin = data["daily"][0]["temp"]["max"]
        temperature_low_kelvin = data["daily"][0]["temp"]["min"]
        temperature_high_celsius = temperature_high_kelvin - 273.15  # Convert from Kelvin to Celsius
        temperature_low_celsius = temperature_low_kelvin - 273.15  # Convert from Kelvin to Celsius
        temperature_high_formatted = f"{temperature_high_celsius:.2f}°C"
        temperature_low_formatted = f"{temperature_low_celsius:.2f}°C"
    else:
        temperature_high_formatted = "N/A"
        temperature_low_formatted = "N/A"

    # Extract weather condition, wind speed, and other relevant data
    if "weather" in data["daily"][0] and len(data["daily"][0]["weather"]) > 0 and "description" in data["daily"][0]["weather"][0]:
        condition = data["daily"][0]["weather"][0]["description"]
    else:
        condition = "N/A"

    if "wind_speed" in data["daily"][0] and "wind_deg" in data["daily"][0]:
        wind_speed = data["daily"][0]["wind_speed"]
        wind_speed_formatted = f"{wind_speed}km/h"
        wind_direction_degrees = data["daily"][0]["wind_deg"]
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
        f"Expected {condition} with a high of {temperature_high_formatted} and a low of {temperature_low_formatted}",
        f"Wind speeds of around {wind_speed_formatted} expected from the {wind_direction_cardinal}, insha'allah...",
        "<https://openweathermap.org/city/2063523>"
    ]

    if next_update_time is not None:
        message_parts.append(f"Next update: <t:{next_update_time}:R>")

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
