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

# Function to post weather data to the Discord webhook
# Function to post weather data to the Discord webhook
# Function to post weather data to the Discord webhook
# Function to post weather data to the Discord webhook
def post_to_discord(data):
    # Replace this with your new Discord webhook URL
    webhook_url = "https://discord.com/api/webhooks/1152075250931073135/-AOJcH8y5KHn5A6yXvk5vmG0eGeL4_DGr2PLrtESLBXnllIvVkM4_WfoXCjbvcHbngdW"

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

    if "wind" in data and "speed" in data["wind"]:
        wind_speed = data["wind"]["speed"]
        wind_speed_formatted = f"{wind_speed}km/h"
    else:
        wind_speed_formatted = "N/A"

    # Format the message with the corrected temperature, condition, wind speed, and additional line
    message = f"Saturday 16 September:\nExpected {condition} with a top of {temperature_formatted}\nWind speeds of around {wind_speed_formatted} expected, insha'allah...\nTake a look for yourself: https://openweathermap.org/city/2063523\nᵐᵃᵈᵉ ᵇʸ ᵃᵇᵈᵘˡˡᵃʰ ᵃʳᵃᶠᵃᵗ"


    payload = {
        "content": message,
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
    response = post_to_discord(weather_data)

    # Calculate the timestamp for the next run
    current_time = int(time.time())
    next_run_time = current_time + 24 * 60 * 60  # 24 hours in seconds

    # Post the timestamp to signify when the next run will happen
    post_to_discord({"next_run_time": next_run_time})

if __name__ == "__main__":
    main()
