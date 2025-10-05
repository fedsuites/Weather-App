from dotenv import load_dotenv
import os
import requests
from datetime import datetime
import csv
from colorama import Fore,Style, init
init(autoreset=True)

filename="weather.csv"

locations=[]
load_dotenv()
API_KEY= os.getenv("OPENWEATHER_API_KEY")

def main():
    get_city()

def fetch_weather(location):
    url= f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric" 
    try:
        response= requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as error:
        print(Fore.RED + "Unable to fetch weather, check your internet connection")
        #print(f"Debug info: {error}")
        return None



def parse_weather(data):
    #Extract useful fields from OpenWeather JSON.
    if not data or int(data.get("cod"))!=200:  
        return None
    
    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "temp_min": data["main"]["temp_min"],
        "temp_max": data["main"]["temp_max"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"].title(),
        "wind_speed": data["wind"]["speed"],
        "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p"),
        "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p"),
    }

def display_weather(weather):
    #Display formatted weather data with colors and grouped layout
    
    print(Fore.CYAN + Style.BRIGHT + "\n" + "=" * 45)
    print(Fore.YELLOW + Style.BRIGHT + f"📍 {weather['city']}, {weather['country']}")
    print(Fore.CYAN + "=" * 45)

    print(f"""
{Fore.RED}🌡️ Temp: {weather['temperature']:.1f}°C {Fore.WHITE}(Feels like {weather['feels_like']:.1f}°C)
{Fore.MAGENTA}🔻 Min: {weather['temp_min']:.1f}°C | 🔺 Max: {weather['temp_max']:.1f}°C
{Fore.BLUE}💧 Humidity: {weather['humidity']}%
{Fore.GREEN}🌥️ Condition: {weather['condition']}
{Fore.CYAN}💨 Wind-Speed: {weather['wind_speed']} m/s
{Fore.YELLOW}🌅 Sunrise: {weather['sunrise']}
{Fore.LIGHTBLACK_EX}🌇 Sunset: {weather['sunset']}
""")
    print(Fore.CYAN + "=" * 45 + "\n")
    
#loads saved locations from csv.
def load_locations():
    global locations
    locations=[]
    try:
        with open(filename,"r", newline="") as file:
            reader= csv.DictReader(file)
            for row in reader:
                locations.append(row)
    except FileNotFoundError:
        pass
    return locations

#write/save searched locations into csv
def save_locations(location):
     for row in load_locations():
        if row["Locations"]== location:
            print("You already saved this location. Try searching for another one instead.")
            return
     else:
            print(Fore.GREEN + "✅ Location saved successfully!")         
     with open(filename,"a",newline="") as file:
                writer= csv.DictWriter(file,fieldnames=["Locations"])
                if file.tell()==0:
                    writer.writeheader()
                writer.writerow({f"Locations": location})
     locations.append(location)

def get_city():
    while True:
        load_locations()

        if locations:
            print(Fore.CYAN + Style.BRIGHT + "\nSaved Locations:")
            for index, loc in enumerate(locations):
                print(Fore.YELLOW + f" {index + 1}. {loc['Locations']}")
            print() 

        location = input(Fore.WHITE + Style.BRIGHT + "Enter a location: ").strip().title()
        data = fetch_weather(location)

        if int(data.get("cod")) == 200:
            weather = parse_weather(data)
            display_weather(weather)

            ask_save = input(Fore.CYAN + "Do you want to save this location? (yes(y)/no(n)): ").lower().strip()
            if ask_save in ("yes", "y"):
                save_locations(location)    
        else:
            print(Fore.RED + Style.BRIGHT + "❌ Location not found. Please try again.")

        more = input(Fore.CYAN + "\nCheck another location? (yes(y)/no(n)): ").lower().strip()
        if more not in ("yes", "y"):
            print(Fore.YELLOW + "\n👋 Goodbye! Thanks for using the Weather App.\n")
            break

if __name__=="__main__":
    main()