import requests
import datetime
import time

# Replace with your AccuWeather API key
api_key = "7IH90mfoKf1kSx1i5CSw48fzEvm2PaMn"

# Function to get weather data
def get_weather_data():
    # Location key for Kewdale, WA
    location_key = "16490"

    # AccuWeather API endpoint for current weather data
    weather_api_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}"

    response = requests.get(weather_api_url)
    data = response.json()
    return data

def get_precipitation_forecast():
    # AccuWeather API endpoint for MinuteCast forecast
    minutecast_api_url = f"http://dataservice.accuweather.com/forecasts/v1/minute/{location_key}?apikey={api_key}"

    response = requests.get(minutecast_api_url)
    forecast_data = response.json()
    return forecast_data

def post_to_discord(data, forecast_data, next_update_time=None):
    # Replace this with your new Discord webhook URL
    webhook_url = "https://discord.com/api/webhooks/1152081939692531792/ge9OfoVVONFOVL_n1HOjMsS_wAThanFyS8d_9wEfv5CD9qZnOnhiQKYU1ED5Dwf93bdx"

    # Extract temperature information from the API response
    if "Temperature" in data[0] and "Imperial" in data[0]["Temperature"]:
        temperature_fahrenheit = data[0]["Temperature"]["Imperial"]["Value"]
        temperature_celsius = (temperature_fahrenheit - 32) * 5/9  # Convert from Fahrenheit to Celsius
        temperature_formatted = f"{temperature_celsius:.2f}°C"
    else:
        temperature_formatted = "N/A"

    # Extract weather condition from the API response
    if "WeatherText" in data[0]:
        condition = data[0]["WeatherText"]
    else:
        condition = "N/A"

    # Extract precipitation forecast from the forecast data
    if "Summary" in forecast_data and "Phrase" in forecast_data["Summary"]:
        precipitation_forecast = forecast_data["Summary"]["Phrase"]
    else:
        precipitation_forecast = "N/A"

    # Get the current date in AWST (Australian Western Standard Time)
    current_time_utc = datetime.datetime.utcnow()
    current_time_awst = current_time_utc + datetime.timedelta(hours=8)
    current_date_awst_str = current_time_awst.strftime("%A %d %B")

    # Format the message with the corrected temperature, condition, wind speed, and additional line
    message_parts = [
        f"{current_date_awst_str}:",
        f"> Expected {condition} with a top of {temperature_formatted}",
        f"> Precipitation forecast: {precipitation_forecast}"
    ]

    if next_update_time is not None:
        message_parts.append(f"> Next weather message is <t:{next_update_time}:R>")

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
    
     # Get the precipitation forecast
     forecast_data = get_precipitation_forecast()

     # Calculate the timestamp for the next run
     current_time_utc = datetime.datetime.utcnow()
     next_run_time_utc = current_time_utc + datetime.timedelta(days=1)
    
     post_to_discord(weather_data, forecast_data, int(next_run_time_utc.timestamp()))

if __name__ == "__main__":
     main()
