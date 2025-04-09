import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# El alcance que solicitamos para la API de Gmail (para enviar correos)
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Nombre del archivo donde se guardarán las credenciales de acceso
TOKEN_PICKLE = 'token.pickle'

def get_credentials():
    """Obtiene las credenciales necesarias para acceder a Gmail usando OAuth2."""
    creds = None
    # Si el archivo token.pickle existe, lo cargamos
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)

    # Si las credenciales no son válidas, pedimos autorización al usuario
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Renovamos el token si es necesario
        else:
            # Usamos el archivo credentials.json para pedir permisos al usuario
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)  # Autoriza y genera el token

        # Guardamos las credenciales en un archivo local
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_gmail_service():
    """Obtiene el servicio de Gmail autenticado con las credenciales de OAuth2."""
    creds = get_credentials()  # Obtén las credenciales
    service = build('gmail', 'v1', credentials=creds)  # Constrúye el servicio de Gmail
    return service
