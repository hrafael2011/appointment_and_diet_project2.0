from celery import shared_task
import requests
import logging


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
    