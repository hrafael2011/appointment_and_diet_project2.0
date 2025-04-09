

import json
import os

import requests
from rest_framework.exceptions import ValidationError
from .task import send_reminder_email

from datetime import datetime, timedelta
from django.utils import timezone


#Catpcha function
def validate_captcha(captcha_response):
    secret_key = "6LdYHOsqAAAAAGRXHmc3T7TRwwbpLFz26CsBDsS7"  # Reemplaza con tu Secret Key
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={"secret": secret_key, "response": captcha_response}
    )
    if not response.json().get("success", False):
        raise ValidationError("CAPTCHA no válido.")
    



#Whatsapp Claude Api config function

WHATSAPP_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN')  # Usa una variable de entorno
WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_ID')  # ID del número de teléfono de WhatsApp Cloud API
WHATSAPP_URL = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_ID}/messages"

HEADERS = {
    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
    "Content-Type": "application/json"
}

def send_whatsapp_message(to, message):
    """
    Envía un mensaje de WhatsApp utilizando la API de WhatsApp Cloud.
    :param to: Número de teléfono en formato internacional (ej. +18091234567)
    :param message: Contenido del mensaje
    """
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    
    response = requests.post(WHATSAPP_URL, headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        print("✅ Mensaje de WhatsApp enviado correctamente")
    else:
        print("❌ Error al enviar mensaje:", response.text)
    
    return response.json()

