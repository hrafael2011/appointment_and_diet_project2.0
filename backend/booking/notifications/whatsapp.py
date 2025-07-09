
#from ..task import send_whatsapp_message_task

from ..tasks.whatsapp_tasks import send_whatsapp_message_task



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