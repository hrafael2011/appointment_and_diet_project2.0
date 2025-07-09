

from ..tasks.email_tasks import (
    send_confirmation_mail,
    send_confirmation_final_mail,
    send_cancellation_mail
    
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

    
    #Sends confirmation final mail to the doctor and patient
    
    send_confirmation_final_mail.delay(
        email_patient=appointment.patient.email,
        email_doctor=appointment.doctor.email,
        date=str(appointment.date),
        hour=str(appointment.hour),
        confirmation_token=str(appointment.confirmation_token),
    )


    # Sends email canelation to the patient
def send_mail_cancelation_appointment(appointment):
    send_cancellation_mail.delay(
        email_patient=appointment.patient.email,
        email_doctor=appointment.doctor.email,
        date=str(appointment.date),
        hour=str(appointment.hour),
    )