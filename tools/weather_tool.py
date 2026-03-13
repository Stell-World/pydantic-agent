#!/usr/bin/env python3
"""
🌤️ Weather Tool pour PydanticAI
Obtention des informations météo avec WeatherAPI
"""

import os
from dotenv import load_dotenv
import requests
from typing import Dict, Any

load_dotenv()

class WeatherTool:
    """Outil météo pour PydanticAI"""
    
    def __init__(self):
        self.api_key = os.getenv("GETWEATHER_API_KEY")
        self.base_url = "http://api.weatherapi.com/v1"
    
    def get_current_weather(self, query: str) -> str:
        """
        Recherche les informations météo actuelles via WeatherAPI
        
        Args:
            query: Nom de la ville ou code postal
            
        Returns:
            Informations météo formatées et détaillées
        """
        if not self.api_key:
            return "❌ GETWEATHER_API_KEY non configurée. Veuillez configurer votre clé API WeatherAPI."
        
        try:
            endpoint = f"{self.base_url}/current.json"
            params = {
                "key": self.api_key,
                "q": query,
                "aqi": "no",
                "lang": "en"
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("location"):
                location = data["location"]
                current = data["current"]
                
                # Formater la réponse de manière lisible
                weather_info = f"""
🌍 **Météo à {location['name']}, {location['country']}**

🌡️ **Température:** {current['temp_c']}°C (ressenti {current['feelslike_c']}°C)
☁️ **Condition:** {current['condition']['text']}
💨 **Vent:** {current['wind_kph']} km/h ({current['wind_dir']})
💧 **Humidité:** {current['humidity']}%
👁️ **Visibilité:** {current['vis_km']} km
🌅 **Heure locale:** {location['localtime']}
🌡️ **Pression:** {current['pressure_mb']} mb
💦 **Indice UV:** {current['uv']}
                """.strip()
                
                return weather_info
            else:
                return f"❌ Ville '{query}' non trouvée. Vérifiez l'orthographe."
                
        except requests.exceptions.RequestException as e:
            return f"❌ Erreur réseau: {str(e)}"
        except Exception as e:
            return f"❌ Erreur lors de l'obtention des données météo: {str(e)}"
    
    def get_forecast(self, query: str, days: int = 3) -> str:
        """
        Obtient les prévisions météo pour plusieurs jours
        
        Args:
            query: Nom de la ville ou code postal
            days: Nombre de jours (1-7)
            
        Returns:
            Prévisions météo formatées
        """
        if not self.api_key:
            return "❌ GETWEATHER_API_KEY non configurée. Veuillez configurer votre clé API WeatherAPI."
        
        try:
            endpoint = f"{self.base_url}/forecast.json"
            params = {
                "key": self.api_key,
                "q": query,
                "days": min(days, 7),
                "aqi": "no",
                "lang": "fr"
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("location"):
                location = data["location"]
                forecast_days = data["forecast"]["forecastday"]
                
                output = f"🌤️ **Prévisions météo pour {location['name']}, {location['country']}**\n\n"
                
                for day in forecast_days:
                    day_data = day["day"]
                    output += f"📅 **{day['date']}**\n"
                    output += f"🌡️ **Max:** {day_data['maxtemp_c']}°C | **Min:** {day_data['mintemp_c']}°C\n"
                    output += f"☁️ **Condition:** {day_data['condition']['text']}\n"
                    output += f"🌧️ **Pluie:** {day_data['daily_chance_of_rain']}%\n"
                    output += f"💨 **Vent max:** {day_data['maxwind_kph']} km/h\n"
                    output += f"☀️ **UV:** {day_data['uv']}\n\n"
                
                return output
            else:
                return f"❌ Ville '{query}' non trouvée. Vérifiez l'orthographe."
                
        except requests.exceptions.RequestException as e:
            return f"❌ Erreur réseau: {str(e)}"
        except Exception as e:
            return f"❌ Erreur lors de l'obtention des prévisions: {str(e)}"

# Fonctions pour PydanticAI
def get_weather(query: str) -> str:
    """
    Recherche les informations météo actuelles pour une ville.
    
    Args:
        query: Nom de la ville ou code postal
        
    Returns:
        Informations météo détaillées (température, conditions, vent, humidité, etc.)
    """
    tool = WeatherTool()
    return tool.get_current_weather(query)

def get_weather_forecast(query: str, days: int = 3) -> str:
    """
    Obtient les prévisions météo pour plusieurs jours.
    
    Args:
        query: Nom de la ville ou code postal
        days: Nombre de jours de prévision (1-7)
        
    Returns:
        Prévisions météo détaillées par jour
    """
    tool = WeatherTool()
    return tool.get_forecast(query, days)

if __name__ == "__main__":
    # Test de l'outil
    print("🌤️ Test Weather Tool")
    print("=" * 40)
    print(get_weather("Paris"))
    print("\n" + "=" * 40)
    print(get_weather_forecast("Paris", 3))
