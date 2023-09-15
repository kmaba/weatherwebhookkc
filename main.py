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
    webhook_url = "https://discord.com/api/webhooks/1152075250931073135/-AOJcH8y5KHn5A6yXvk5vmG0eGeL4_DGr2PLrtESLBXnllIvVkM4_WfoXCjbvcHbngdW"

    # Extract weather information from the API response
    if "main" in data and "temp" in data["main"]:
        temperature = data["main"]["temp"]
    else:
        temperature = "N/A"

    if "weather" in data and len(data["weather"]) > 0 and "description" in data["weather"][0]:
        condition = data["weather"][0]["description"]
    else:
        condition = "N/A"

    if "wind" in data and "speed" in data["wind"]:
        wind_speed = data["wind"]["speed"]
    else:
        wind_speed = "N/A"

    # Format the message
    message = f"Saturday 16 September:\nExpected {condition} weather with a top of {temperature}°C\nFew Showers expected at around 2 to 3 a.m\nWind speeds of around {wind_speed}km/h expected, insha'allah."

    payload = {
        "content": message,
    }

    response = requests.post(webhook_url, json=payload)
    
    # Add logging
    if response.status_code == 200:
        print("Message posted successfully.")
    else:
        print(f"Failed to post message. Status code: {response.status_code}")
    
    return response
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
