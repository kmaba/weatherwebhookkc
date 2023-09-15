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
def post_to_discord(data):
    # Replace this with your Discord webhook URL
    webhook_url = "https://discord.com/api/webhooks/1152067074995273758/hvW6EvWVcFAo-xvUITxTEbvXEnDxK70rrchKxisccHAc1AZuVewSM-JIrR5OeD_ie58"

    # Extract weather information from the API response
    temperature = data["main"]["temp"]
    condition = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]

    # Format the message
    message = f"Saturday 16 September:\nExpected {condition} weather with a top of {temperature}°C\nFew Showers expected at around 2 to 3 a.m\nWind speeds of around {wind_speed}km/h expected, insha'allah."

    payload = {
        "content": message,
    }

    response = requests.post(webhook_url, json=payload)
    return response

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
