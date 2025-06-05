# 🌤️ Weather Forecast App

This is a simple command-line weather forecast application built in Python that uses the OpenWeatherMap API to provide current weather and 5-day forecasts for any city. The app also maintains a history of recent searches in a local JSON file for easy re-access.

## 🚀 Features

- 🌡️ Get **current weather** details (temperature, humidity, and description)
- 📅 View a **5-day weather forecast** (daily summary at noon)
- 🧠 Stores **recent city searches** in `recent_searches.json`
- 📂 Reads from and writes to a local JSON file
- 🧼 Graceful handling of errors and invalid inputs

## 🛠️ Requirements

- Python 3.6+
- `requests` module

You can install the required module with:

```bash
pip install requests
# weather_forecast
Weather Forecast App
1. Search Weather by City
2. View Recent Searches
3. Exit
Enter choice (1-3): 1
Enter city name: London

Current Weather in London:
Temperature: 16°C
Humidity: 73%
Description: Broken clouds

5-Day Forecast:
2024-06-06: 18°C, Light rain
2024-06-07: 20°C, Few clouds
...
