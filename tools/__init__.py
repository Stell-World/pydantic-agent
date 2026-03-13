#!/usr/bin/env python3
"""
🛠️ Module d'outils pour KWAME AI
Importation et configuration de tous les outils pour PydanticAI
"""

# Importation des outils
from .tavily_search import tavily_search
from .weather_tool import get_weather, get_weather_forecast
from .link_retriever import online_article_retriever, get_article_metadata

# Liste des outils disponibles
TOOLS_LIST = [
    {
        "name": "tavily_search",
        "function": tavily_search,
        "description": "Recherche web en temps réel avec Tavily",
        "usage": "Quand vous avez besoin d'informations actualisées ou de vérifier des faits"
    },
    {
        "name": "get_weather",
        "function": get_weather,
        "description": "Obtenir la météo actuelle",
        "usage": "Quand vous demandez la météo d'une ville ou d'un lieu"
    },
    {
        "name": "get_weather_forecast",
        "function": get_weather_forecast,
        "description": "Obtenir les prévisions météo",
        "usage": "Quand vous voulez les prévisions météo pour plusieurs jours"
    },
    {
        "name": "online_article_retriever",
        "function": online_article_retriever,
        "description": "Extraire le contenu d'articles en ligne",
        "usage": "Quand vous avez besoin d'analyser le contenu d'une URL spécifique"
    },
    {
        "name": "get_article_metadata",
        "function": get_article_metadata,
        "description": "Extraire les métadonnées d'un article",
        "usage": "Quand vous voulez les informations sur un article (titre, auteur, date)"
    }
]

def get_all_tools():
    """
    Retourne tous les outils configurés pour PydanticAI
    
    Returns:
        Liste des fonctions d'outils à utiliser avec Agent(tools=...)
    """
    return [
        tavily_search,
        get_weather,
        get_weather_forecast,
        online_article_retriever,
        get_article_metadata
    ]

def get_tools_info():
    """
    Retourne les informations sur tous les outils
    
    Returns:
        Chaîne formatée décrivant tous les outils disponibles
    """
    info = "🛠️ **Outils disponibles pour KWAME AI:**\n\n"
    
    for tool in TOOLS_LIST:
        info += f"🔹 **{tool['name']}**\n"
        info += f"   📝 {tool['description']}\n"
        info += f"   💡 Usage: {tool['usage']}\n\n"
    
    return info

if __name__ == "__main__":
    print("🛠️ Test du module d'outils KWAME AI")
    print("=" * 50)
    print(get_tools_info())
    print("\n" + "=" * 50)
    print("Liste des fonctions d'outils:")
    for tool in get_all_tools():
        print(f"  • {tool.__name__}")
