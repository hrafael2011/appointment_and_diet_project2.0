from datetime import datetime, timedelta
from django.utils import timezone


from .task import (
    send_confirmation_mail,
    send_confirmation_final_mail,
    create_calendar_event,
    send_cancellation_mail,
    send_reminder_email,
    send_whatsapp_message_task
)

# It sends appointment by mail
def send_patient_confirmation_mail(appointment):
  
    send_confirmation_mail.delay(
        email_patient=appointment.patient.email,
        confirmation_token=str(appointment.confirmation_token),
        date=str(appointment.date),
        hour=str(appointment.hour),
    )


def send_patient_and_doctor_fina_confirmation_mail(appointment):

    '''
    Sends confirmation final mail to the doctor and patient
    '''
    send_confirmation_final_mail.delay(
        email_patient=appointment.patient.email,
        email_doctor="rafaelacosta0320@gmail.com",
        date=str(appointment.date),
        hour=str(appointment.hour),
        confirmation_token=str(appointment.confirmation_token),
    )

#Create event in doctor's calendar
def create_doctor_event_calendar(appointment):
    
    create_calendar_event.delay(
        name=appointment.patient.name,
        date=str(appointment.date),
        hour=str(appointment.hour),
        appointment_id=appointment.id,
    )

# Sends email canelation to the patient
def send_mail_cancelation_appointment(appointment):
    send_cancellation_mail.delay(
        email_patient=appointment.patient.email,
        email_doctor=appointment.doctor.email,
        date=str(appointment.date),
        hour=str(appointment.hour),
    )



def schedule_reminders(appointment):
    # Verificar si la cita está en el futuro
    appointment_datetime = timezone.make_aware(
        datetime.combine(appointment.date, appointment.hour)
    )
    now = timezone.now()

    if appointment_datetime <= now:
        print("[DEBUG] La cita ya ocurrió. No se programan recordatorios.")
        return

    # Calcular las fechas para los recordatorios
    reminder_12_hours_before = appointment_datetime - timedelta(hours=12)
    reminder_1_hour_before = appointment_datetime - timedelta(hours=1)

    # Programar recordatorio 12 horas antes (si no se ha enviado)
    if not appointment.reminder_12h_sent and reminder_12_hours_before > now:
        send_reminder_email.apply_async(
            args=[
                appointment.patient.email,
                str(appointment.date),
                str(appointment.hour),
                "12 horas antes",
            ],
            eta=reminder_12_hours_before,
        )
        appointment.reminder_12h_sent = True
        print(
            f"[DEBUG] Recordatorio 12 horas antes programado para {reminder_12_hours_before}"
        )

    # Programar recordatorio 1 hora antes (si no se ha enviado)
    form_link = f"http://localhost:3000/informacion-personal-form/{appointment.patient.id}"
    info_form_link = f"Complete sus datos {form_link}"
    if not appointment.reminder_1h_sent and reminder_1_hour_before > now:
        send_reminder_email.apply_async(
            
            args=[
                appointment.patient.email,
                str(appointment.date),
                str(appointment.hour),
                "1 hora antes",
                info_form_link,
            ],
            eta=reminder_1_hour_before,
        )
        appointment.reminder_1h_sent = True
        print(
            f"[DEBUG] Recordatorio 1 hora antes programado para {reminder_1_hour_before}"
        )

    # Guardar los cambios en el modelo
    appointment.save()

def whatsapp_appointment(appointment):
    """
    Confirma la cita y envía el mensaje de WhatsApp en segundo plano.
    """
    send_whatsapp_message_task.delay(
        appointment.patient.name,
        appointment.doctor.name,
        str(appointment.date),  # Convertir a string si es necesario
        str(appointment.hour),  # Convertir a string si es necesario
        appointment.patient.whatsapp
    )
