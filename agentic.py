#!/usr/bin/env python3
"""
🤖 KWAME AI - Agent PydanticAI avec Outils Intégrés
Version réorganisée avec outils importés du dossier tools
"""

import os
import logging
import json
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from pydantic_ai import Agent, ModelMessage
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
from pydantic_ai.models.google import GoogleModel
from langfuse import Langfuse

load_dotenv()

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kwame_ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration Langfuse
try:
    langfuse = Langfuse(
        secret_key=os.getenv('LANGFUSE_SECRET_KEY'),
        public_key=os.getenv('LANGFUSE_PUBLIC_KEY'),
        host=os.getenv('LANGFUSE_BASE_URL')
    )
    logger.info("🚀 Initialisation de KWAME AI")
    logger.info(f"📊 Langfuse connecté: {bool(langfuse)}")
except Exception as e:
    logger.warning(f"⚠️ Erreur initialisation Langfuse: {e}")
    langfuse = None

# Configuration des modèles
logger.info("⚙️ Configuration des modèles IA")
llama_model = GroqModel(
    'llama-3.1-8b-instant',
    provider=GroqProvider(api_key=os.getenv('GROQ_API_KEY'))
)
logger.info("✅ Modèle Llama 3.1 8b Instant configuré")

gpt_model = GroqModel(
    'gpt-oss-120b',
    provider=GroqProvider(api_key=os.getenv('GROQ_API_KEY'))
)
logger.info("✅ Modèle GPT-OSS 120b configuré")

gemini_model = GoogleModel('gemini-1.5-flash')
logger.info("✅ Modèle Gemini 1.5 Flash configuré")

async def keep_recent_messages(messages: list[ModelMessage]) -> list[ModelMessage]:
    """Keep only the last 10 messages to manage token usage."""
    original_count = len(messages)
    filtered_messages = messages[-10:] if len(messages) > 10 else messages
    logger.debug(f"🔄 Filtrage messages: {original_count} -> {len(filtered_messages)}")
    return filtered_messages

# Création de l'agent
logger.info("🤖 Création de l'agent KWAME AI")
agent = Agent(
    llama_model,
    history_processors=[keep_recent_messages]
)
logger.info("✅ Agent créé avec succès")

# ===== IMPORT DES OUTILS =====
logger.info("🔧 Import des outils")
try:
    from tools.tavily_search import tavily_search
    logger.info("✅ Tavily Search importé")
except ImportError as e:
    logger.error(f"❌ Erreur import Tavily Search: {e}")

try:
    from tools.weather_tool import get_weather, get_weather_forecast
    logger.info("✅ Weather Tool importé")
except ImportError as e:
    logger.error(f"❌ Erreur import Weather Tool: {e}")

try:
    from tools.link_retriever import online_article_retriever, get_article_metadata
    logger.info("✅ Link Retriever importé")
except ImportError as e:
    logger.error(f"❌ Erreur import Link Retriever: {e}")

try:
    from tools.send_mail import send_email
    logger.info("✅ Send Mail importé")
except ImportError as e:
    logger.error(f"❌ Erreur import Send Mail: {e}")

try:
    from tools.calendar_manager import (
        get_todays_events, create_event, get_events_by_date, 
        get_upcoming_events, delete_event
    )
    logger.info("✅ Calendar Manager importé")
except ImportError as e:
    logger.error(f"❌ Erreur import Calendar Manager: {e}")

# ===== OUTILS RECHERCHE =====
@agent.tool_plain
async def tavily_search_tool(query: str, max_results: int = 5) -> str:
    """Recherche web en temps réel"""
    logger.info(f"🔍 Recherche web: {query} (max_results: {max_results})")
    try:
        result = tavily_search(query, max_results)
        logger.info(f"✅ Recherche web réussie pour: {query}")
        return result
    except Exception as e:
        logger.error(f"❌ Erreur recherche web: {e}")
        return f"Erreur lors de la recherche: {str(e)}"

# ===== OUTILS MÉTÉO =====
@agent.tool_plain
async def get_weather_tool(query: str) -> str:
    """Informations météo actuelles"""
    logger.info(f"🌤️ Recherche météo: {query}")
    try:
        result = get_weather(query)
        logger.info(f"✅ Météo récupérée pour: {query}")
        return result
    except Exception as e:
        logger.error(f"❌ Erreur météo: {e}")
        return f"Erreur lors de la récupération météo: {str(e)}"

@agent.tool_plain
async def get_weather_forecast_tool(query: str, days: int = 3) -> str:
    """Prévisions météo"""
    logger.info(f"📅 Prévisions météo pour {query} ({days} jours)")
    try:
        result = get_weather_forecast(query, days)
        logger.info(f"✅ Prévisions météo récupérées pour: {query}")
        return result
    except Exception as e:
        logger.error(f"❌ Erreur prévisions météo: {e}")
        return f"Erreur lors de la récupération des prévisions: {str(e)}"

# ===== OUTILS LINK RETRIEVER =====
@agent.tool_plain
async def online_article_retriever_tool(url: str) -> str:
    """Extrait le contenu d'un article en ligne"""
    logger.info(f"📄 Extraction article: {url}")
    try:
        result = online_article_retriever(url)
        logger.info(f"✅ Article extrait: {url}")
        return result
    except Exception as e:
        logger.error(f"❌ Erreur extraction article: {e}")
        return f"Erreur lors de l'extraction de l'article: {str(e)}"

@agent.tool_plain
async def get_article_metadata_tool(url: str) -> str:
    """Extrait les métadonnées d'un article"""
    logger.info(f"📋 Extraction métadonnées: {url}")
    try:
        result = get_article_metadata(url)
        logger.info(f"✅ Métadonnées extraites: {url}")
        return result
    except Exception as e:
        logger.error(f"❌ Erreur extraction métadonnées: {e}")
        return f"Erreur lors de l'extraction des métadonnées: {str(e)}"

# ===== OUTILS CALENDRIER =====
@agent.tool_plain
async def get_todays_events_tool() -> str:
    """Affiche les événements du jour"""
    logger.info("📅 Récupération événements du jour")
    try:
        result = get_todays_events()
        logger.info("✅ Événements du jour récupérés")
        return result
    except Exception as e:
        logger.error(f"❌ Erreur récupération événements: {e}")
        return f"Erreur lors de la récupération des événements: {str(e)}"

@agent.tool_plain
async def create_event_tool(title: str, date: str, start_time: str, end_time: str, description: str = "") -> str:
    """Crée un nouvel événement"""
    logger.info(f"📝 Création événement: {title} le {date} de {start_time} à {end_time}")
    try:
        result = create_event(title, date, start_time, end_time, description)
        logger.info(f"✅ Événement créé: {title}")
        return result
    except Exception as e:
        logger.error(f"❌ Erreur création événement: {e}")
        return f"Erreur lors de la création de l'événement: {str(e)}"

@agent.tool_plain
async def get_events_by_date_tool(date: str) -> str:
    """Affiche les événements pour une date spécifique"""
    logger.info(f"📅 Récupération événements pour: {date}")
    try:
        result = get_events_by_date(date)
        logger.info(f"✅ Événements récupérés pour: {date}")
        return result
    except Exception as e:
        logger.error(f"❌ Erreur récupération événements: {e}")
        return f"Erreur lors de la récupération des événements: {str(e)}"

@agent.tool_plain
async def get_upcoming_events_tool(days: int = 7) -> str:
    """Affiche les événements à venir"""
    logger.info(f"📆 Récupération événements des {days} prochains jours")
    try:
        result = get_upcoming_events(days)
        logger.info(f"✅ Événements à venir récupérés ({days} jours)")
        return result
    except Exception as e:
        logger.error(f"❌ Erreur récupération événements: {e}")
        return f"Erreur lors de la récupération des événements: {str(e)}"

@agent.tool_plain
async def delete_event_tool(event_id: int) -> str:
    """Supprime un événement"""
    logger.info(f"🗑️ Suppression événement ID: {event_id}")
    try:
        result = delete_event(event_id)
        logger.info(f"✅ Événement supprimé: {event_id}")
        return result
    except Exception as e:
        logger.error(f"❌ Erreur suppression événement: {e}")
        return f"Erreur lors de la suppression de l'événement: {str(e)}"

# ===== OUTIL EMAIL =====
@agent.tool_plain
async def send_email_tool(receiver_email: str = "fredyhoundayi@gmail.com", subject: str = "Subject", message: str = "") -> str:
    """Envoie un email avec disclaimer automatique"""
    logger.info(f"📧 Envoi email à: {receiver_email} (sujet: {subject})")
    try:
        send_email(receiver_email, subject, message)
        logger.info(f"✅ Email envoyé avec succès à {receiver_email}")
        return f"✅ Email envoyé avec succès à {receiver_email}"
    except Exception as e:
        logger.error(f"❌ Erreur envoi email: {e}")
        return f"❌ Erreur lors de l'envoi de l'email: {str(e)}"

# ===== INSTRUCTIONS DE L'AGENT =====
instructions = """
Je suis KWAME AI, votre assistant intelligent avec outils intégrés.

🎯 CAPACITÉS PRINCIPALES:
• Recherche web en temps réel avec Tavily
• Informations météo actuelles et prévisions
• Extraction et analyse de contenu web
• Gestion du calendrier et événements
• Envoi d'emails automatiques

💡 UTILISATION DES OUTILS:
- **Recherche web:** "cherche [sujet]" ou "trouve des informations sur [topic]"
- **Météo:** "météo à [ville]" ou "quelle température à [ville]"
- **Prévisions:** "prévisions météo pour [ville]"
- **Articles:** "analyse l'article [URL]" ou "extrais le contenu de [URL]"
- **Métadonnées:** "informations sur l'article [URL]"
- **Calendrier aujourd'hui:** "montre mes événements aujourd'hui"
- **Créer événement:** "crée un événement: [titre] le [date] de [heure] à [heure]"
- **Événements par date:** "montre les événements le [date]"
- **Événements à venir:** "montre mes événements pour les [nombre] prochains jours"
- **Supprimer événement:** "supprime l'événement ID [numéro]"
- **Envoyer email:** "envoie un email à [adresse] avec sujet [sujet] et message [message]"

🌐 MODÈLES DISPONIBLES:
• Llama 3.3 70b - Rapide et efficace pour tâches quotidiennes
• GPT 5.2 - Équilibré et puissant pour analyses complexes
• Gemini Flash - Ultra-rapide pour réponses instantanées

🔧 CONFIGURATION DES OUTILS:
• Tavily Search: {'✅' if os.getenv('TAVILY_API_KEY') else '❌ Clé API manquante'}
• WeatherAPI: {'✅' if os.getenv('GETWEATHER_API_KEY') else '❌ Clé API manquante'}
• Article Retriever: {'✅ Toujours disponible'}
• Calendar Tool: {'✅ Stockage JSON local disponible'}
• Email Tool: {'✅ Gmail SMTP disponible'}

⚠️ IMPORTANT: 
- TOUJOURS inclure le contenu des recherches dans les emails envoyés
- Répondre avec les informations réelles obtenues, pas des phrases génériques
- En cas d'erreur, expliquer clairement le problème sans répéter des messages automatiques
- Pour le calendrier, utiliser le stockage JSON local si Google Calendar n'est pas configuré

Je suis prêt à vous aider avec tous vos projets! 🚀
"""

# Mettre à jour les instructions de l'agent
logger.info("📝 Configuration des instructions de l'agent")
agent.instructions = instructions
logger.info("✅ Instructions de l'agent configurées")

# ===== INTERFACE WEB PYDANTIC =====
logger.info("🌐 Configuration de l'interface web")
app = agent.to_web(
    models={
        '🦆 Llama 3.3 70b': llama_model,
        '🧠 GPT 5.2': gpt_model,
        '⚡ Gemini Flash': gemini_model,
    },
    instructions="KWAME AI - Agent complet avec outils de recherche, météo et extraction d'articles",
)
logger.info("✅ Interface web configurée")

def main():
    """Fonction principale avec logging et monitoring"""
    logger.info("🚀 Démarrage de KWAME AI")
    
    # Test question
    test_query = "What is the weather in Paris?"
    logger.info(f"❓ Question de test: {test_query}")
    
    try:
        logger.info("🤖 Exécution de la requête agent...")
        result = agent.run_sync(test_query)
        
        logger.info("✅ Réponse obtenue avec succès")
        print("\n" + "="*50)
        print("🤖 RÉPONSE DE KWAME AI:")
        print("="*50)
        print(result)
        print("="*50)
        
        # Création d'un trace Langfuse pour la session
        try:
            # Démarrer un span pour la session avec contexte
            with langfuse.start_as_current_span(
                name="kwame_ai_session",
                input={"query": test_query},
                metadata={
                    "model": "llama-3.1-8b-instant",
                    "timestamp": datetime.now().isoformat(),
                    "version": "1.0"
                }
            ) as span:
                # Mettre à jour avec la réponse
                langfuse.update_current_trace(
                    output={"response": str(result), "response_length": len(str(result))},
                    metadata={"status": "success"}
                )
            
            logger.info("📊 Session Langfuse terminée avec succès")
        except Exception as langfuse_error:
            logger.warning(f"⚠️ Erreur Langfuse: {langfuse_error}")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'exécution: {e}")
        print(f"\n❌ Erreur: {e}")
        
        # Trace d'erreur Langfuse
        try:
            # Démarrer un span pour l'erreur avec contexte
            with langfuse.start_as_current_span(
                name="kwame_ai_error",
                input={"query": test_query},
                metadata={"status": "error", "error_type": type(e).__name__}
            ) as error_span:
                # Mettre à jour avec l'erreur
                langfuse.update_current_trace(
                    output={"error": str(e)},
                    metadata={"status": "error"}
                )
            
            logger.info("📊 Erreur tracée dans Langfuse")
        except Exception as langfuse_error:
            logger.warning(f"⚠️ Erreur Langfuse: {langfuse_error}")
    
    logger.info("🏁 Fin de la session KWAME AI")

if __name__ == "__main__":
    main()