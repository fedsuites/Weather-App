# Weather-App
A simple CLI weather app that fetches live weather data using OpenWeather API.

 Weather App

 Features
- Fetch current weather by city name  
- Displays temperature, humidity, and weather condition  
- Saves weather data to a CSV file  
- Uses `.env` for secure API key management  

Technologies Used
- Python 3  
- Requests  
- CSV  
- Python-dotenv  

 Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/fedsuites/Weather-App.git
   cd Weather-App

2. Create a .env file and add your API key:

 OPENWEATHER_API_KEY=your_api_key_here

3. Install dependencies:
pip install requests python-dotenv

4. Run the app:
python weather.py

Example Output
When you run the app and enter a city name (e.g., Lagos), you’ll see:
City: Lagos
Temperature: 30°C
Humidity: 65%
Condition: Clear Sky
Weather data saved to weather.csv

 Notes
Ensure .env is listed in .gitignore before committing.
Get your free API key from OpenWeather(https://openweathermap.org/api)

=======

A simple CLI weather app that fetches live weather data using OpenWeather API. Weather App

Features

 .Fetch current weather by city name
 .Displays temperature, humidity, and weather condition
 .Saves weather data to a CSV file
 .Uses .env for secure API key management

Technologies Used

 .Python 3
 .Requests
 .CSV
 .Python-dotenv
 .Setup Instructions

Clone the repository:
git clone https://github.com/fedsuites/Weather-App.git
cd Weather-App
Create a .env file and add your API key:
OPENWEATHER_API_KEY=your_api_key_here

Install dependencies: pip install requests python-dotenv

Run the app: python weather.py

Example Output When you run the app and enter a city name (e.g., Lagos), you’ll see: City: Lagos Temperature: 30°C Humidity: 65% Condition: Clear Sky Weather data saved to weather.csv

Notes Ensure .env is listed in .gitignore before committing. Get your free API key from OpenWeather(https://openweathermap.org/api)
