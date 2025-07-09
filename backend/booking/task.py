from celery import shared_task
from django.core.mail import send_mail
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
from datetime import datetime, timedelta
from django.conf import settings
import os
import requests
import logging


@shared_task
def send_confirmation_mail(email_patient, confirmation_token, date, hour):
    asunto = "Confirma tu cita"
    enlace_confirmacion = f"http://localhost/api/appointment/confirm/?confirmation_token={confirmation_token}"
    mensaje = f"Por favor, confirma tu cita para {date} a las {hour}. Haz clic aquí: {enlace_confirmacion}"
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [email_patient])

@shared_task
def send_confirmation_final_mail(email_patient, email_doctor, date, hour, confirmation_token):
    asunto = "Cita Confirmada"
    cancellation_link = f'http://localhost:3000/cancelacion-cita?token={confirmation_token}'
    mensaje = (f"Tu cita ha sido confirmada para {date} a las {hour}.\n\n"
               f"Si deseas cancelarla, haz clic aquí: {cancellation_link}"     )
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [email_patient, email_doctor])

@shared_task
def send_cancellation_mail(email_patient, email_doctor, date, hour):
    asunto = "Cita Cancelada"
    mensaje = f"Su cita para {date} a las {hour} ha sido cancelada exitosamente."
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [email_patient, email_doctor])



@shared_task
def send_reminder_email(email, date, hour, reminder_type, form_link = None,  *args, **kwargs):
    print(f"[DEBUG] Enviando recordatorio a {email} para {date} a las {hour} ({reminder_type})")
    try:
        asunto = f"Recordatorio de Cita ({reminder_type})"
        mensaje = (f"Este es un recordatorio de tu cita programada para {date} a las {hour}.\n\n"
                   f"{form_link}")

        send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [email])
        print(f"[DEBUG] Correo enviado correctamente a {email}")
    except Exception as e:
        print(f"[ERROR] Error al enviar correo a {email}: {str(e)}")




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
        from .models import Appointments
        appointment = Appointments.objects.get(id=appointment_id)
        appointment.google_event_id = created_event.get('id')
        appointment.save()

    except Exception as e:
        print(f"Error al crear el evento: {e}")
        raise self.retry(exc=e)
    



 #sends whatsapp task   

#WHATSAPP_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
#WHATSAPP_TOKEN = settings.API_WHATSAPP_ACCESS_TOKEN
#WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
#WHATSAPP_PHONE_ID = settings.API_WHATSAPP_PHONE_ID

WHATSAPP_TOKEN="EAAaZBM7Swk0MBO8rZAu4vbzzls2stWNjbLVRTll8Y5BxozCNgfEawdL0N0C3V0ySM8lEW4WTmNV7c1WKRhsfqdv8et1L3vFGoVK7r5d9Wc7JMoCdCfkBf4kyyD6MucCvLkCuE4nW0MRIC6nU0RnFjqZBIlhR18sRvyTelOgkUWUB10Yx5NJ7EZCXQAPxvwkBbwiBiwZDZD"
WHATSAPP_PHONE_ID='636625479530255'



WHATSAPP_URL = f"https://graph.facebook.com/v22.0/{WHATSAPP_PHONE_ID}/messages"

HEADERS = {
    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
    "Content-Type": "application/json",
}

@shared_task(bind=True, autoretry_for=(requests.exceptions.RequestException,), retry_backoff=5, max_retries=3)
def send_whatsapp_message_task(self, patient_name, doctor_name, appointment_date, appointment_hour, patient_whatsapp):
    """
    Tarea Celery para enviar mensajes de WhatsApp con la plantilla aprobada.
    """

    payload = {
        "messaging_product": "whatsapp",
        "to": patient_whatsapp,
        "type": "template",
        "template": {
            "name": "appointment_confirmation",  # ⚠️ Reemplázalo con el nombre exacto de la plantilla aprobada
            "language": {"code": "es"},  # ⚠️ Ajusta el idioma si es necesario
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": patient_name},  # {{1}} -> Nombre del paciente
                        {"type": "text", "text": doctor_name},   # {{2}} -> Nombre del doctor
                        {"type": "text", "text": appointment_date},  # {{3}} -> Fecha
                        {"type": "text", "text": appointment_hour}  # {{4}} -> Hora
                    ]
                }
            ]
        }
    }

    try:
        response = requests.post(WHATSAPP_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        logging.info(f"✅ Mensaje enviado a {patient_whatsapp}: {payload}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error enviando mensaje a {patient_whatsapp}: {e}")
        raise self.retry(exc=e)  # Reintentar si hay error
    

@shared_task(bind=True, autoretry_for=(requests.exceptions.RequestException,), retry_backoff=5, max_retries=3)
def send_whatsapp_reminder(self, patient_name, doctor_name, appointment_hour, patient_whatsapp, form_link):
    """
    Tarea Celery para enviar mensajes de WhatsApp con la plantilla aprobada.
    """

    payload = {
        "messaging_product": "whatsapp",
        "to": patient_whatsapp,
        "type": "template",
        "template": {
            "name": "whatsapp_rimender_appointment",  # ⚠️ Reemplázalo con el nombre exacto de la plantilla aprobada
            "language": {"code": "es"},  # ⚠️ Ajusta el idioma si es necesario
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": patient_name},  # {{1}} -> Nombre del paciente
                        {"type": "text", "text": doctor_name},   # {{2}} -> Nombre del doctor
                        {"type": "text", "text": appointment_hour} , # {{3}} -> Hora
                        {"type": "text", "text": form_link}  # {{4}} -> Hora
                    ]
                }
            ]
        }
    }

    try:
        response = requests.post(WHATSAPP_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        logging.info(f"✅ Mensaje enviado a {patient_whatsapp}: {payload}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error enviando mensaje a {patient_whatsapp}: {e}")
        raise self.retry(exc=e)  # Reintentar si hay error



    
  
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


