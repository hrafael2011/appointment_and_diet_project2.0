

from celery import shared_task
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from django.conf import settings
import os


def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_CALENDAR_CREDENTIALS, scopes=settings.GOOGLE_CALENDAR_SCOPES
    )

    service = build('calendar', 'v3', credentials=credentials)
    return service



@shared_task(bind=True)
def create_calendar_event(self, name, date, hour, appointment_id):
    try:
        service = get_calendar_service()
        calendar_id = 'rafaelacosta0320@gmail.com'

        # Combina la fecha y hora en formato datetime
        appointment_datetime = datetime.strptime(f"{date} {hour}", "%Y-%m-%d %H:%M:%S")

        # Formatea la fecha y hora a formato ISO 8601 con zona horaria
        start_time = appointment_datetime.strftime("%Y-%m-%dT%H:%M:%S-04:00")  # Hora de inicio
        end_time = (appointment_datetime + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S-04:00")  # Hora de fin (1 hora después)


        event = {
            'summary': f'Cita del paciente {name}',
            'location': 'Santo Domingo, RD',
            'description': 'Discusión sobre el nuevo proyecto',
            'start': {
                'dateTime': start_time,
                'timeZone': 'America/Santo_Domingo',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'America/Santo_Domingo',
            },
        }

        created_event  = service.events().insert(calendarId=calendar_id, body=event).execute()
        print("Evento creado con éxito:", created_event .get('htmlLink'))

        # Guardar el ID del evento en la cita
        from ..models import Appointments
        appointment = Appointments.objects.get(id=appointment_id)
        appointment.google_event_id = created_event.get('id')
        appointment.save()

    except Exception as e:
        print(f"Error al crear el evento: {e}")
        raise self.retry(exc=e)




def update_calendar_event_on_cancellation(appointment):
    try:
        service = get_calendar_service()

        if not appointment.google_event_id:
            print("Error: La cita no tiene un ID de evento en Google Calendar.")
            return

        calendar_id = 'rafaelacosta0320@gmail.com'

        # Obtener los detalles del evento antes de actualizarlo
        event = service.events().get(calendarId=calendar_id, eventId=appointment.google_event_id).execute()

        # Actualizar solo el título y la descripción
        event['summary'] = f'CITA CANCELADA - {appointment.patient.name}'
        event['description'] = 'Esta cita ha sido cancelada.'
        event['colorId'] = '11'  # Rojo para indicar cancelación

        updated_event = service.events().update(
            calendarId=calendar_id,
            eventId=appointment.google_event_id,
            body=event
        ).execute()

        print("Evento actualizado con éxito:", updated_event.get('htmlLink'))

    except Exception as e:
        print(f"Error al actualizar el evento en Google Calendar: {e}")


