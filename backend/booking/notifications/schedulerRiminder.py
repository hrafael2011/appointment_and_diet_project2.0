
   






from datetime import datetime, timedelta
from django.utils import timezone
from ..tasks.scheduleRimender_taks import send_reminder_email, send_whatsapp_reminder


def schedule_reminders(appointment):
    if not is_future_appointment(appointment):
        print("[DEBUG] La cita ya ocurrió. No se programan recordatorios.")
        return

    reminder_times = get_reminder_times(appointment)

    if should_send_reminder(appointment.reminder_12h_sent, reminder_times["12h"]):
        schedule_all_reminders(appointment, "12 horas antes", reminder_times["12h"])
        appointment.reminder_12h_sent = True

    if should_send_reminder(appointment.reminder_1h_sent, reminder_times["1h"]):
        extra_message = build_info_form_link(appointment)
        schedule_all_reminders(appointment, "1 hora antes", reminder_times["1h"], extra=extra_message)
        appointment.reminder_1h_sent = True

    appointment.save()


# -----------------------
# SUBFUNCIONES
# -----------------------

def is_future_appointment(appointment):
    appointment_datetime = timezone.make_aware(
        datetime.combine(appointment.date, appointment.hour)
    )
    return appointment_datetime > timezone.now()


def get_reminder_times(appointment):
    appointment_datetime = timezone.make_aware(
        datetime.combine(appointment.date, appointment.hour)
    )
    return {
        "12h": appointment_datetime - timedelta(hours=12),
        "1h": appointment_datetime - timedelta(hours=1),
    }


def should_send_reminder(flag_sent, reminder_time):
    return not flag_sent and reminder_time > timezone.now()


def schedule_all_reminders(appointment, timing_label, eta, extra=None):
    send_email_reminder(appointment, timing_label, eta, extra)
    send_whatsapp_reminder_task(appointment, timing_label, eta, extra)


def send_email_reminder(appointment, timing_label, eta, extra=None):
    args = [
        appointment.patient.email,
        str(appointment.date),
        str(appointment.hour),
        timing_label,
    ]
    if extra:
        args.append(extra)

    send_reminder_email.apply_async(args=args, eta=eta)
    print(f"[DEBUG] Email programado para {timing_label} -> {eta}")


def send_whatsapp_reminder_task(appointment, timing_label, eta, extra=None):
    patient_name = appointment.patient.name
    doctor_name = appointment.doctor.name
    appointment_hour = str(appointment.date)
    appointment_date = str(appointment.hour)
    patient_whatsapp = appointment.patient.whatsapp  # debe estar en formato internacional
    form_link = extra if extra else ""

    send_whatsapp_reminder.apply_async(
        args=[
            patient_name,
            doctor_name,
            appointment_date,
            appointment_hour,
            patient_whatsapp,
            form_link,
        ],
        eta=eta
    )
    print(f"[DEBUG] WhatsApp (plantilla oficial) programado para {timing_label} -> {eta}")


def build_info_form_link(appointment):
    return f"Complete sus datos: http://localhost:3000/informacion-personal-form/{appointment.patient.id}"
