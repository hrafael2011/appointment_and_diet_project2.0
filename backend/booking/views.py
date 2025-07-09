





from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.db import transaction
from rest_framework.response import Response
from datetime import datetime, timedelta

from .models import Appointments, Doctor
from .serializers import AppointmentsSerializer
from patient.serializers import PatientSerializers

from .notifications.email import (
    send_patient_confirmation_mail,
    send_patient_and_doctor_fina_confirmation_mail,
    send_mail_cancelation_appointment
)
from  .notifications.calendar import create_doctor_event_calendar
from  .notifications.whatsapp import whatsapp_appointment
from  .notifications.schedulerRiminder import schedule_reminders

from .tasks.calendar_tasks import update_calendar_event_on_cancellation
from .utils import validate_captcha


class AppointmentsView(viewsets.ModelViewSet):
    queryset = Appointments.objects.filter(is_active=True)
    serializer_class = AppointmentsSerializer

    def create(self, request, *args, **kwargs):
        try:
            validate_captcha(request.data.get("captcha"))

            with transaction.atomic():
                doctor_id = request.data.get("doctor")
                patient_data = {
                    "doctor_id": doctor_id,
                    "name": request.data.get("name"),
                    "last_name": request.data.get("last_name"),
                    "whatsapp": request.data.get("whatsapp"),
                    "email": request.data.get("email"),
                }

                try:
                    patient = self._get_or_create_patient(doctor_id, patient_data)
                except ValueError as e:
                    return self.error_response(e)

                appointment_data = {
                    "patient": patient.id,
                    "date": request.data["date"],
                    "hour": request.data["hour"],
                    "status": "pending",
                }

                serializer = AppointmentsSerializer(data=appointment_data)
                if serializer.is_valid():
                    appointment = serializer.save()
                    send_patient_confirmation_mail(appointment)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Unexpected Error:", str(e))
            return self.error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["get"], url_path="confirm")
    def confirm_appointment(self, request):
        token = request.query_params.get("confirmation_token")
        try:
            appointment = self._get_appointment_by_token(token)
        except Exception as e:
            return self.error_response(str(e), status.HTTP_404_NOT_FOUND)

        if appointment.status == "confirmed":
            return Response(
              
                {
                    "message": "La cita ha sido confirmada satisfactoriamente.",
                    "patient_name": appointment.patient.name
                },
                status=status.HTTP_200_OK,
            )

        if not appointment.patient or not appointment.doctor:
            return self.error_response("Patient or Doctor not assigned.")

        appointment.status = "confirmed"
        appointment.save()

        send_patient_and_doctor_fina_confirmation_mail(appointment)
        create_doctor_event_calendar(appointment)
        schedule_reminders(appointment)
        whatsapp_appointment(appointment)

        return Response(
            
            {
                    "message": "La cita ha sido confirmada satisfactoriamente.",
                    "patient_name": appointment.patient.name
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], url_path="cancel")
    def cancel_appointment(self, request):
        token = request.data.get("token")
        try:
            appointment = self._get_appointment_by_token(token)
            self._validate_cancel_timing(appointment)
        except ValueError as e:
            return self.error_response(str(e))
        except Appointments.DoesNotExist:
            return self.error_response("Token inválido", status.HTTP_404_NOT_FOUND)

        if appointment.status == "canceled":
            return Response(
                {"message": "The appointment has been canceled."},
                status=status.HTTP_200_OK,
            )

        appointment.status = "canceled"
        appointment.save()

        update_calendar_event_on_cancellation(appointment)
        send_mail_cancelation_appointment(appointment)

        return Response(
            {
                "message": f"Señor {appointment.patient.name}, su cita ha sido cancelada."
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"], url_path="validate-cancellation")
    def validate_cancellation(self, request):
        token = request.query_params.get("token")
        try:
            appointment = self._get_appointment_by_token(token)
            self._validate_cancel_timing(appointment)
        except ValueError as e:
            return self.error_response(str(e))
        except Appointments.DoesNotExist:
            return self.error_response("Token inválido", status.HTTP_404_NOT_FOUND)

        return Response(
            {"patient_name": appointment.patient.name}, status=status.HTTP_200_OK
        )

    # ============ MÉTODOS AUXILIARES PRIVADOS ============

    def _get_appointment_by_token(self, token):
        if not token:
            raise ValueError("Token requerido")
        return Appointments.objects.get(confirmation_token=token)

    def _validate_cancel_timing(self, appointment):
        appointment_datetime = datetime.combine(appointment.date, appointment.hour)
        if appointment_datetime - datetime.now() < timedelta(hours=1):
            raise ValueError("La cita no puede cancelarse menos de una hora antes.")

    def _get_or_create_patient(self, doctor_id, patient_data):
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            raise ValueError("Doctor not found")

        serializer = PatientSerializers(data=patient_data)
        if serializer.is_valid():
            return serializer.save(doctor=doctor)
        else:
            raise ValueError(serializer.errors)

    def error_response(self, message, code=status.HTTP_400_BAD_REQUEST):
        return Response({"error": message}, status=code)



