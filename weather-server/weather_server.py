"""
Simple MCP Weather Server using FastMCP SDK

This server provides weather information for cities using the WeatherAPI service.
It demonstrates how to create a basic MCP server with a single tool.
"""

import os
import requests
from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("Weather Server")

# WeatherAPI configuration
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_BASE_URL = "http://api.weatherapi.com/v1/current.json"

# Validate API key is available
if not WEATHER_API_KEY or WEATHER_API_KEY == "your_weather_api_key_here":
    print("⚠️  Warning: No valid WEATHER_API_KEY found!")
    print("   Please set the WEATHER_API_KEY environment variable or create a .env file")
    print("   See .env.example for reference")


@mcp.tool()
def get_weather(city: str) -> dict[str, str]:
    """
    Get current weather information for a city.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        Dictionary containing temperature, condition, and wind speed
    """
    try:
        # Make API request to WeatherAPI
        params = {
            "key": WEATHER_API_KEY,
            "q": city,
            "aqi": "no"  # We don't need air quality data
        }
        
        response = requests.get(WEATHER_API_BASE_URL, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        
        # Extract the relevant weather information
        current = data["current"]
        location = data["location"]
        
        return {
            "city": f"{location['name']}, {location['country']}",
            "temperature": f"{current['temp_c']}°C",
            "condition": current["condition"]["text"],
            "wind_speed": f"{current['wind_kph']} km/h"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch weather data: {str(e)}",
            "city": city,
            "temperature": "N/A",
            "condition": "N/A",
            "wind_speed": "N/A"
        }
    except KeyError as e:
        return {
            "error": f"Unexpected response format: missing {str(e)}",
            "city": city,
            "temperature": "N/A",
            "condition": "N/A",
            "wind_speed": "N/A"
        }
    except Exception as e:
        return {
            "error": f"An unexpected error occurred: {str(e)}",
            "city": city,
            "temperature": "N/A",
            "condition": "N/A",
            "wind_speed": "N/A"
        }


def main():
    """Entry point for running the weather server directly."""
    print("Starting Weather MCP Server...")
    mcp.run()


if __name__ == "__main__":
    main()
