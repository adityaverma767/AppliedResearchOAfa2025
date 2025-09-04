#!/usr/bin/env python3
"""
This file is another example of code for the Emotion-Driven Code Review Assistant.
It shows a developer having a good day, with some successes and challenges.
"""

import json
import requests
from datetime import datetime

# Feeling good about this API wrapper class!
class WeatherAPI:
    """A clean API wrapper - I'm actually proud of this structure."""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        # Finally, a constructor that makes sense!
    
    def get_weather(self, city):
        """Fetches weather data - this function brings me joy."""
        url = f"{self.base_url}/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'  # Celsius is the standard, obviously
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Let it crash gracefully
            return response.json()
        except requests.RequestException as e:
            # TODO: add proper logging instead of just printing stuff
            print(f"API call failed: {e}")  # At least I'm handling errors now
            return None

# This data processing function is my masterpiece.
def process_weather_data(raw_data):
    """Transforms raw API data into something useful and readable."""
    if not raw_data:
        return {"error": "No data to process"}  # Defensive programming feels good
    
    # I love how clean this data extraction turned out.
    processed = {
        'city': raw_data.get('name', 'Unknown'),
        'country': raw_data.get('sys', {}).get('country', 'Unknown'),
        'temperature': raw_data.get('main', {}).get('temp', 0),
        'feels_like': raw_data.get('main', {}).get('feels_like', 0),
        'humidity': raw_data.get('main', {}).get('humidity', 0),
        'description': raw_data.get('weather', [{}])[0].get('description', 'No description'),
        'timestamp': datetime.now().isoformat()
    }
    
    # This validation logic is solid - no more crashes from missing data!
    if processed['temperature'] < -273:  # Absolute zero check - science!
        processed['temperature'] = 'Invalid reading'
    
    return processed

# Okay, this caching system is getting complex but it works beautifully.
class WeatherCache:
    """A smart caching system - performance optimization at its finest!"""
    
    def __init__(self, ttl_seconds=300):  # 5 minutes cache
        self.cache = {}
        self.ttl = ttl_seconds
        # I'm becoming a performance optimization wizard!
    
    def get(self, key):
        """Retrieves from cache if still fresh."""
        if key in self.cache:
            data, timestamp = self.cache[key]
            age = (datetime.now() - timestamp).total_seconds()
            
            if age < self.ttl:
                print(f"Cache hit! Saved an API call.")  # Small wins matter
                return data
            else:
                # Expired data cleanup - I love tidy code
                del self.cache[key]
        
        return None
    
    def set(self, key, value):
        """Stores in cache with timestamp."""
        self.cache[key] = (value, datetime.now())
        # TODO: implement cache size limits (maybe LRU?)
        # For now, this simple approach works great

# This function combines everything - integration magic!
def get_weather_with_cache(city, api_key, cache):
    """The main orchestrator function - pulls everything together nicely."""
    
    # Check cache first - efficiency is beautiful.
    cached_result = cache.get(city.lower())
    if cached_result:
        return cached_result
    
    # Cache miss - time for fresh data
    print(f"Fetching fresh weather data for {city}...")
    api = WeatherAPI(api_key)
    raw_data = api.get_weather(city)
    
    if raw_data:
        processed = process_weather_data(raw_data)
        cache.set(city.lower(), processed)  # Store for next time
        print("Successfully processed and cached weather data!")
        return processed
    else:
        # Graceful failure - no crashes here
        return {"error": f"Could not fetch weather for {city}"}

# A utility function that actually makes sense.
def format_weather_report(weather_data):
    """Formats weather data for human consumption - user experience matters!"""
    
    if 'error' in weather_data:
        return f"Error: {weather_data['error']}"
    
    # This template system turned out elegant.
    report = f"""
Weather Report for {weather_data['city']}, {weather_data['country']}
Temperature: {weather_data['temperature']}°C (feels like {weather_data['feels_like']}°C)
Humidity: {weather_data['humidity']}
Conditions: {weather_data['description'].title()}
Updated: {weather_data['timestamp']}
    """.strip()
    
    return report

# Configuration management done right.
def load_config(filename="config.json"):
    """Loads configuration from JSON file - separation of concerns is important."""
    try:
        with open(filename, 'r') as f:
            config = json.load(f)
            print("Configuration loaded successfully!")
            return config
    except FileNotFoundError:
        print("Config file not found, using defaults.")
        # Reasonable defaults instead of crashing - mature error handling
        return {
            "api_key": "your_api_key_here",
            "default_cities": ["London", "Tokyo", "New York"],
            "cache_ttl": 300
        }
    except json.JSONDecodeError:
        print("Invalid JSON in config file.")
        return None

# The main function ties it all together beautifully.
def main():
    """Main application logic - clean and organized."""
    print("Starting Weather Dashboard Application.")
    
    # Load configuration
    config = load_config()
    if not config:
        print("Configuration error - cannot continue.")
        return
    
    # Initialize cache system
    cache = WeatherCache(ttl_seconds=config.get('cache_ttl', 300))
    print("Cache system initialized.")
    
    # Process default cities
    cities = config.get('default_cities', ['London'])
    api_key = config.get('api_key', 'demo_key')
    
    print(f"Getting weather for {len(cities)} cities...")
    
    for city in cities:
        print(f"\n--- Processing {city} ---")
        weather_data = get_weather_with_cache(city, api_key, cache)
        report = format_weather_report(weather_data)
        print(report)
    
    print("Weather dashboard update complete!")
    print("This application architecture feels solid and maintainable.")

# Bonus: A simple CLI interface, why not?
def interactive_mode():
    """Interactive mode for manual city queries - designed to be user-friendly."""
    print("Interactive Weather Mode")
    print("Type city names to get weather, or 'quit' to exit.")
    
    config = load_config()
    cache = WeatherCache()
    api_key = config.get('api_key', 'demo_key')
    
    while True:
        city = input("\nEnter city name: ").strip()
        
        if city.lower() in ['quit', 'exit', 'q']:
            print("Thanks for using the weather app!")
            break
        
        if city:
            weather_data = get_weather_with_cache(city, api_key, cache)
            report = format_weather_report(weather_data)
            print(report)
        else:
            print("Please enter a valid city name.")

if __name__ == "__main__":
    print("Weather Dashboard v2.0 - Now with more confidence!")
    
    # TODO: Add command line argument parsing
    # For now, just run the main demo
    main()
    
    # Uncomment this for interactive mode
    # interactive_mode()
    
    print("\nCode review note: I'm actually quite happy with how this turned out!")