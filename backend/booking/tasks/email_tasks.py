
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import os


@shared_task
def send_confirmation_mail(email_patient, confirmation_token, date, hour):
    asunto = "Confirma tu cita"
    #enlace_confirmacion = f"http://localhost/api/appointment/confirm/?confirmation_token={confirmation_token}" 
    enlace_confirmacion = f"http://localhost:3000/confirmacion-cita?token={confirmation_token}"

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