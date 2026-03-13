import datetime
import os.path
import json

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Service initialisé à la demande
service = None

def get_calendar_service():
    """Obtient le service Google Calendar avec authentification"""
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    return service

def get_service():
    """Initialise le service Google Calendar si nécessaire"""
    global service
    if service is None:
        service = get_calendar_service()
    return service

# ===== FONCTIONS POUR PYDANTICAI =====

def get_todays_events() -> str:
    """Affiche les événements du jour"""
    try:
        service = get_service()
        if service is None:
            return "❌ Service Google Calendar non disponible. Veuillez configurer credentials.json"
        
        now = datetime.datetime.now(datetime.UTC).isoformat()
        end_of_day = datetime.datetime.now(datetime.UTC).replace(hour=23, minute=59, second=59).isoformat()
        
        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        
        events = events_result.get("items", [])
        
        if not events:
            return "📅 Aucun événement aujourd'hui"
        
        output = f"📅 **Événements d'aujourd'hui ({len(events)}):**\n\n"
        
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event.get("summary", "Sans titre")
            event_id = event.get("id", "N/A")
            
            if isinstance(start, str) and 'T' in start:
                # Format datetime
                dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
                formatted_time = dt.strftime('%H:%M')
                output += f"🕐 **{formatted_time}** - {summary} (ID: {event_id})\n"
            else:
                output += f"📅 **{start}** - {summary} (ID: {event_id})\n"
        
        return output
        
    except Exception as e:
        return f"❌ Erreur lors de la récupération des événements: {str(e)}"

def create_event(title: str, date: str, start_time: str, end_time: str, description: str = "") -> str:
    """Crée un nouvel événement"""
    try:
        service = get_service()
        if service is None:
            return "❌ Service Google Calendar non disponible. Veuillez configurer credentials.json"
        
        # Combiner date et time
        start_datetime = f"{date}T{start_time}:00"
        end_datetime = f"{date}T{end_time}:00"
        
        event = {
            "summary": title,
            "description": description,
            "start": {
                "dateTime": start_datetime,
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end_datetime,
                "timeZone": "UTC",
            },
        }
        
        created_event = service.events().insert(
            calendarId="primary",
            body=event
        ).execute()
        
        event_id = created_event.get("id", "N/A")
        return f"✅ Événement créé avec succès: {title} (ID: {event_id})"
        
    except Exception as e:
        return f"❌ Erreur lors de la création de l'événement: {str(e)}"

def get_events_by_date(date: str) -> str:
    """Affiche les événements pour une date spécifique"""
    try:
        service = get_service()
        if service is None:
            return "❌ Service Google Calendar non disponible. Veuillez configurer credentials.json"
        
        start_of_day = f"{date}T00:00:00"
        end_of_day = f"{date}T23:59:59"
        
        events_result = service.events().list(
            calendarId="primary",
            timeMin=start_of_day,
            timeMax=end_of_day,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        
        events = events_result.get("items", [])
        
        if not events:
            return f"📅 Aucun événement le {date}"
        
        output = f"📅 **Événements du {date} ({len(events)}):**\n\n"
        
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event.get("summary", "Sans titre")
            event_id = event.get("id", "N/A")
            
            if isinstance(start, str) and 'T' in start:
                dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
                formatted_time = dt.strftime('%H:%M')
                output += f"🕐 **{formatted_time}** - {summary} (ID: {event_id})\n"
            else:
                output += f"📅 **{start}** - {summary} (ID: {event_id})\n"
        
        return output
        
    except Exception as e:
        return f"❌ Erreur lors de la récupération des événements: {str(e)}"

def get_upcoming_events(days: int = 7) -> str:
    """Affiche les événements à venir"""
    try:
        service = get_service()
        if service is None:
            return "❌ Service Google Calendar non disponible. Veuillez configurer credentials.json"
        
        now = datetime.datetime.now(datetime.UTC).isoformat()
        future_date = (datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=days)).isoformat()
        
        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            timeMax=future_date,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        
        events = events_result.get("items", [])
        
        if not events:
            return f"📅 Aucun événement pour les {days} prochains jours"
        
        output = f"📅 **Événements des {days} prochains jours ({len(events)}):**\n\n"
        
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event.get("summary", "Sans titre")
            event_id = event.get("id", "N/A")
            
            if isinstance(start, str) and 'T' in start:
                dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
                formatted_date = dt.strftime('%d/%m %H:%M')
                output += f"🕐 **{formatted_date}** - {summary} (ID: {event_id})\n"
            else:
                output += f"📅 **{start}** - {summary} (ID: {event_id})\n"
        
        return output
        
    except Exception as e:
        return f"❌ Erreur lors de la récupération des événements: {str(e)}"

def delete_event(event_id: int) -> str:
    """Supprime un événement"""
    try:
        service = get_service()
        if service is None:
            return "❌ Service Google Calendar non disponible. Veuillez configurer credentials.json"
        
        service.events().delete(
            calendarId="primary",
            eventId=str(event_id)
        ).execute()
        
        return f"🗑️ Événement {event_id} supprimé avec succès"
        
    except Exception as e:
        return f"❌ Erreur lors de la suppression de l'événement: {str(e)}"

if __name__ == "__main__":
    print("🗓️ Test Calendar Manager")
    print("=" * 40)
    print(get_todays_events())
