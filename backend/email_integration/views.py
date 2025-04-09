import requests
import time
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)

# Variables globales
access_token_cache = None
token_expiration_time = 0

# 1. Renovar el Access Token usando el Refresh Token
def refresh_access_token(refresh_token):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": settings.ANYMAIL['GOOGLE_OAUTH2_CLIENT_ID'],
        "client_secret": settings.ANYMAIL['GOOGLE_OAUTH2_CLIENT_SECRET'],
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        token_info = response.json()
        logger.info("Nuevo Access Token obtenido correctamente.")
        return token_info["access_token"], time.time() + 3500  # Renueva antes de expirar
    else:
        logger.error(f"Error al renovar el token: {response.status_code}, {response.text}")
        raise Exception(f"Error al renovar el token: {response.text}")

# 2. Obtener un Access Token válido (con renovación automática)
def get_valid_access_token():
    global access_token_cache, token_expiration_time
    current_time = time.time()

    if not access_token_cache or current_time >= token_expiration_time:
        logger.info("Access Token caducado o inexistente. Renovando...")
        refresh_token = settings.GOOGLE_REFRESH_TOKEN
        access_token_cache, token_expiration_time = refresh_access_token(refresh_token)
    else:
        logger.info("Access Token todavía válido.")
    return access_token_cache

# 3. Validar correos electrónicos de los destinatarios
def validate_recipient_emails(recipient_list):
    for recipient in recipient_list:
        try:
            validate_email(recipient)
        except ValidationError:
            logger.error(f"Dirección de correo inválida: {recipient}")
            raise Exception(f"Dirección de correo inválida: {recipient}")

# 4. Enviar un correo de prueba
def send_test_email():
    subject = "Prueba de Gmail OAuth2"
    message = "Este es un correo de prueba enviado desde Django utilizando Gmail y OAuth2."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ["hendrick_02@hotmail.com"]  # Cambia por el correo del destinatario

    validate_recipient_emails(recipient_list)

    send_mail(subject, message, from_email, recipient_list)
    logger.info("Correo enviado correctamente.")
