from django.core.mail.backends.smtp import EmailBackend
from email_integration.views import get_valid_access_token

class GmailOAuth2Backend(EmailBackend):
    def _get_password(self):
        # Obtén un Access Token válido (renueva si es necesario)
        return get_valid_access_token()
