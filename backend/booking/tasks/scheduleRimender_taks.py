from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import os
import requests
import logging



#EMAIL RIMENDER

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


#WHATSAPP RIMENDER


WHATSAPP_TOKEN="EAAaZBM7Swk0MBO8rZAu4vbzzls2stWNjbLVRTll8Y5BxozCNgfEawdL0N0C3V0ySM8lEW4WTmNV7c1WKRhsfqdv8et1L3vFGoVK7r5d9Wc7JMoCdCfkBf4kyyD6MucCvLkCuE4nW0MRIC6nU0RnFjqZBIlhR18sRvyTelOgkUWUB10Yx5NJ7EZCXQAPxvwkBbwiBiwZDZD"
WHATSAPP_PHONE_ID='636625479530255'



WHATSAPP_URL = f"https://graph.facebook.com/v22.0/{WHATSAPP_PHONE_ID}/messages"

HEADERS = {
    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
    "Content-Type": "application/json",
}

@shared_task(bind=True, autoretry_for=(requests.exceptions.RequestException,), retry_backoff=5, max_retries=3)
def send_whatsapp_reminder(self, patient_name, doctor_name,appointment_date, appointment_hour, patient_whatsapp, form_link):
    """
    Tarea Celery para enviar mensajes de WhatsApp con la plantilla aprobada.
    """

    payload = {
        "messaging_product": "whatsapp",
        "to": patient_whatsapp,
        "type": "template",
        "template": {
            "name": "whatsapp_rimender_appointment",  # ⚠️ Reemplázalo con el nombre exacto de la plantilla aprobada
            "language": {"code": "en"},  # ⚠️ Ajusta el idioma si es necesario
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": patient_name},  # {{1}} -> Nombre del paciente
                        {"type": "text", "text": doctor_name},   # {{2}} -> Nombre del doctor
                         {"type": "text", "text": appointment_date} , # {{3}} -> fecha
                        {"type": "text", "text": appointment_hour} , # {{4}} -> Hora
                        {"type": "text", "text": form_link}  # {{5}} -> link
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





