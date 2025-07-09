from ..tasks.calendar_tasks import create_calendar_event


#Create event in doctor's calendar
def create_doctor_event_calendar(appointment):
    
    create_calendar_event.delay(
        name=appointment.patient.name,
        date=str(appointment.date),
        hour=str(appointment.hour),
        appointment_id=appointment.id,
    )