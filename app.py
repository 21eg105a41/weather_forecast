import requests
import json
import os
from datetime import datetime

# Configuration
API_KEY = "bbfa370f2985d6a0a9ede4d1640f6509"  # Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/"
SEARCHES_FILE = "recent_searches.json"


# Load recent searches from JSON file
def load_searches():
    if os.path.exists(SEARCHES_FILE):
        try:
            with open(SEARCHES_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading searches: {e}")
            return []
    return []


# Save recent searches to JSON file
def save_searches(searches):
    try:
        with open(SEARCHES_FILE, 'w', encoding='utf-8') as file:
            json.dump(searches, file, indent=4)
        print("Recent searches saved.")
    except Exception as e:
        print(f"Error saving searches: {e}")


# Fetch current weather for a city
def get_current_weather(city):
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            'city': data['name'],
            'temp': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description']
        }
    except Exception as e:
        print(f"Error fetching current weather: {e}")
        return None


# Fetch 5-day forecast for a city
def get_forecast(city):
    url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # Extract daily forecasts (one per day, at noon)
        daily_forecasts = []
        for entry in data['list']:
            if '12:00:00' in entry['dt_txt']:
                daily_forecasts.append({
                    'date': entry['dt_txt'].split()[0],
                    'temp': entry['main']['temp'],
                    'description': entry['weather'][0]['description']
                })
        return daily_forecasts
    except Exception as e:
        print(f"Error fetching forecast: {e}")
        return []


# Display weather data
def display_weather(current, forecast):
    if not current:
        print("No current weather data available.")
        return
    print(f"\nCurrent Weather in {current['city']}:")
    print(f"Temperature: {current['temp']}°C")
    print(f"Humidity: {current['humidity']}%")
    print(f"Description: {current['description'].capitalize()}")

    if forecast:
        print("\n5-Day Forecast:")
        for day in forecast:
            print(f"{day['date']}: {day['temp']}°C, {day['description'].capitalize()}")


# Main menu
def main():
    searches = load_searches()

    while True:
        print("\nWeather Forecast App")
        print("1. Search Weather by City")
        print("2. View Recent Searches")
        print("3. Exit")

        choice = input("Enter choice (1-3): ").strip()

        if choice == '1':
            city = input("Enter city name: ").strip()
            if not city:
                print("City name cannot be empty.")
                continue

            current_weather = get_current_weather(city)
            forecast = get_forecast(city)

            if current_weather:
                display_weather(current_weather, forecast)
                if city.lower() not in [s.lower() for s in searches]:
                    searches.append(city)
                    save_searches(searches)

        elif choice == '2':
            if not searches:
                print("No recent searches.")
            else:
                print("\nRecent Searches:")
                for i, city in enumerate(searches, 1):
                    print(f"{i}. {city}")
                try:
                    idx = int(input("Select a city (number) or 0 to cancel: ")) - 1
                    if idx == -1:
                        continue
                    if 0 <= idx < len(searches):
                        city = searches[idx]
                        current_weather = get_current_weather(city)
                        forecast = get_forecast(city)
                        display_weather(current_weather, forecast)
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Please enter a valid number.")

        elif choice == '3':
            print("Exiting Weather Forecast App.")
            break

        else:
            print("Invalid choice. Please enter 1-3.")


if __name__ == "__main__":
    main()
