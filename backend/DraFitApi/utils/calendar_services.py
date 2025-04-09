from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_CALENDAR_CREDENTIALS, scopes=settings.GOOGLE_CALENDAR_SCOPES
    )

    service = build('calendar', 'v3', credentials=credentials)
    return service


def create_calendar_event():
    service = get_calendar_service()

    calendar_id = 'inghendrickrafael@gmail.com'  # Tu correo de Gmail
    event = {
        'summary': 'Reunión de prueba',
        'location': 'Santo Domingo, RD',
        'description': 'Discusión sobre el nuevo proyecto',
        'start': {
            'dateTime': '2025-03-26T10:00:00-04:00',  # Hora en formato ISO 8601
            'timeZone': 'America/Santo_Domingo',
        },
        'end': {
            'dateTime': '2025-02-26T11:00:00-04:00',
            'timeZone': 'America/Santo_Domingo',
        },
        
    }

    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f'Evento creado: {event.get("htmlLink")}')