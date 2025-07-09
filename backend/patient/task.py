
from celery import shared_task
#from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from diet.models import Diet
import logging
import requests
import os

@shared_task
def send_pdf_email(dieta_id):
    """Genera el PDF y lo envía por correo con el archivo adjunto."""
    dieta = Diet.objects.get(pk=dieta_id)
    paciente = dieta.patient

    if not paciente.email:
        return f"❌ No se puede enviar el PDF: el paciente {paciente.name} no tiene un correo registrado."

    # Generar contenido HTML para el PDF
    html_content = render_to_string('dietas/dieta_pdf.html', {'dieta': dieta, 'dias': [
        dieta.day1, dieta.day2, dieta.day3, dieta.day4,
        dieta.day5, dieta.day6, dieta.day7
    ]})

    # Guardar el PDF temporalmente
    pdf_file = f"/tmp/Plan_Nutricional_{paciente.name}.pdf"
    with open(pdf_file, "wb") as output_pdf:
        pisa_status = pisa.CreatePDF(html_content, dest=output_pdf)

    if pisa_status.err:
        return f"❌ Error al generar el PDF para {paciente.name}"

    # Crear el mensaje de correo con el PDF adjunto
    email = EmailMessage(
        subject="Tu Plan Nutricional",
        body="Adjunto encontrarás tu plan nutricional.",
        from_email=settings.EMAIL_HOST_USER,
        to=[paciente.email]
    )

    email.attach_file(pdf_file)  # ✅ Ahora el PDF se adjunta correctamente
    email.send()

    # Eliminar archivo temporal después del envío
    os.remove(pdf_file)




#WHATSAPP_TOKEN="EAAaZBM7Swk0MBO8rZAu4vbzzls2stWNjbLVRTll8Y5BxozCNgfEawdL0N0C3V0ySM8lEW4WTmNV7c1WKRhsfqdv8et1L3vFGoVK7r5d9Wc7JMoCdCfkBf4kyyD6MucCvLkCuE4nW0MRIC6nU0RnFjqZBIlhR18sRvyTelOgkUWUB10Yx5NJ7EZCXQAPxvwkBbwiBiwZDZD"
WHATSAPP_TOKEN="EAAaZBM7Swk0MBO1pIxjgFU79h1HLvSZB9B4kiZBIXQqyJHKLSNRcCCfZCEwB3oY1h6JWHvVzf5bJX6bOHmwmOlSJhIrLuXg2ok5n43sqow2EbyqPyz5G8t4BbZC1SmWRkQ28RbzjGEumLhc17ZAYQrJedD0reaBdYbRirJaSdoUU5tDGS2LQDZCjoWLbmSySFawspPZC1fev2W8SZBCHAyKregZBXZB9nGShmZC7qeaOlAZDZD"

#WHATSAPP_PHONE_ID='636625479530255'

WHATSAPP_URL=f"https://graph.facebook.com/v22.0/636625479530255/messages"

HEADERS = {
    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
    "Content-Type": "application/json",
}

@shared_task(bind=True, autoretry_for=(requests.exceptions.RequestException,), retry_backoff=5, max_retries=3)
def send_whatsapp_pdf_task(self, patient_name, patient_last_name, doctor , patient_whatsapp, dieta_id):
    """Tarea Celery para enviar el PDF de la dieta al paciente por WhatsApp."""

    dieta = Diet.objects.get(pk=dieta_id)

    # Generar el PDF
    html_content = render_to_string('dietas/dieta_pdf.html', {'dieta': dieta, 'dias': [
        dieta.day1, dieta.day2, dieta.day3, dieta.day4,
        dieta.day5, dieta.day6, dieta.day7
    ]})

    pdf_file = f"/tmp/Plan_Nutricional_{patient_name}.pdf"
    with open(pdf_file, "wb") as output_pdf:
        pisa_status = pisa.CreatePDF(html_content, dest=output_pdf)

    if pisa_status.err:
        logging.error(f"❌ Error al generar el PDF para {patient_name}")
        return f"❌ Error al generar el PDF para {patient_name}"

    # URL donde el paciente podrá descargar el PDF (ajusta esto según tu configuración)
    pdf_download_link = f"https://tu-servidor.com/media/pdfs/Plan_Nutricional_{patient_name}.pdf" 

    # 🔥 Enviar el mensaje con el PDF al paciente
    payload = {
        "messaging_product": "whatsapp",
        "to": patient_whatsapp,
        "type": "template",
        "template": {
            "name": "whatsapp_send_pdf",  # ⚠️ Usa el nombre de la plantilla aprobada
            "language": {"code": "en"},  
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": patient_name},  # {{1}} -> Nombre del paciente
                        {"type": "text", "text": pdf_download_link},  # {{2}} -> Link de descarga
                        {"type": "text", "text": patient_last_name},
                        {"type": "text", "text": doctor}
                    ]
                }
            ]
        }
    }

    try:
        response = requests.post(WHATSAPP_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        logging.info(f"✅ PDF enviado a {patient_whatsapp}: {pdf_download_link}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error enviando PDF a {patient_whatsapp}: {e}")
        raise self.retry(exc=e)  # Reintentar si hay error

    # 🗑️ Eliminar el archivo temporal después de enviarlo
    os.remove(pdf_file)