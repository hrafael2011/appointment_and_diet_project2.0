from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.db import transaction
from rest_framework.response import Response
from datetime import datetime, timedelta

from .models import Appointments, Doctor
from .serializers import AppointmentsSerializer
from patient.serializers import PatientSerializers
from .notifications import (
    send_patient_confirmation_mail,
    send_patient_and_doctor_fina_confirmation_mail,
    create_doctor_event_calendar,
    send_mail_cancelation_appointment,
    schedule_reminders,
    whatsapp_appointment
)
from .task import update_calendar_event_on_cancellation
from .utils import validate_captcha, send_whatsapp_message


# Create your views here.


class AppointmentsView(viewsets.ModelViewSet):
    queryset = Appointments.objects.filter(is_active=True)
    serializer_class = AppointmentsSerializer

    def create(self, request, *args, **kwargs):
        try:
            # CAPTCHA validate
            captcha_response = request.data.get("captcha")
            validate_captcha(captcha_response)

            with transaction.atomic():

                # create patient if not exist
                doctor_id = request.data.get("doctor")
                patient_data = {
                    "doctor_id": doctor_id,
                    "name": request.data.get("name"),
                    "last_name": request.data.get("last_name"),
                    "whatsapp": request.data.get("whatsapp"),
                    "email": request.data.get("email"),
                }

                print("Datos del paciente", patient_data)

                # verify patient if not exist
                try:
                    doctor = Doctor.objects.get(id=doctor_id)
                except Doctor.DoesNotExist:
                    return Response(
                        {"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND
                    )

                # create or update patienet
                patient_serializer = PatientSerializers(data=patient_data)
                if patient_serializer.is_valid():
                    patient = patient_serializer.save(doctor=doctor)
                else:
                    print("Error al validar paciente:", patient_serializer.errors)
                    return Response(
                        patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

                # Create appointment
                appointment_data = {
                    "patient": patient.id,
                    "date": request.data["date"],
                    "hour": request.data["hour"],
                    "status": "pending",
                }

                appointment_serializer = AppointmentsSerializer(data=appointment_data)
                if appointment_serializer.is_valid():
                    appointment = appointment_serializer.save()

                    # Sends confirmation email to the patient
                    send_patient_confirmation_mail(appointment)

                    return Response(
                        appointment_serializer.data, status=status.HTTP_201_CREATED
                    )

                else:
                    print("Error al validar cita:", appointment_serializer.errors)
                    return Response(
                        appointment_serializer.errors, status=status.HTTP_404_NOT_FOUND
                    )

        except Exception as e:
            print("Unexpected Error :", str(e))  # Check the exact error in the conosle
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["get"], url_path="confirm")
    def confirm_appointment(self, request):
        confirmation_token = request.query_params.get("confirmation_token")
        try:
            appointment = Appointments.objects.get(
                confirmation_token=confirmation_token
            )
        except Appointments.DoesNotExist:
            return Response(
                {"error": "Appointment nof found."}, status=status.HTTP_404_NOT_FOUND
            )

        if appointment.status == "confirmed":
            return Response(
                {"message": "The appointment has been confirmed."},
                status=status.HTTP_200_OK,
            )

        # Verify if the doctor and patient are assigned.
        if not appointment.patient or not appointment.doctor:
            return Response(
                {"error": "Patient or Doctor not assigned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = "confirmed"
        appointment.save()

        # sends email confirmation to the patients and doctor
        send_patient_and_doctor_fina_confirmation_mail(appointment)

        # create events in doctor's Google Calendar
        create_doctor_event_calendar(appointment)

        # set reminder
        schedule_reminders(appointment)

        #Whatsapp appoientment
        whatsapp_appointment(appointment)



        return Response(
            {"message": "Appoinment successfully confirmed ."},
            status=status.HTTP_200_OK,
        )


    #Appointment cancel
    @action(detail=False, methods=["post"], url_path="cancel")
    def cancel_appointment(self, request):
        token = request.data.get("token")
        if not token:
            return Response(
                {"error": "Token requerido"}, status=status.HTTP_400_BAD_REQUEST
            )

        appointment = get_object_or_404(Appointments, confirmation_token=token)

        appointment_datetime = datetime.combine(appointment.date, appointment.hour)
        now = datetime.now()

        if appointment_datetime - now < timedelta(hours=1):
            return Response(
                {"error": "The apointment may be canceled up to one hour in advance."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if appointment.status == "canceled":
            return Response(
                {"message": "The appointment has been canceled."},
                status=status.HTTP_200_OK,
            )

        appointment.status = "canceled"
        appointment.save()

        # Updates google calendar
        update_calendar_event_on_cancellation(
            appointment
        )  

        # Sends cancelation email to the doctor and patient
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
        if not token:
            return Response(
                {"error": "Token requerido"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            appointment = Appointments.objects.get(confirmation_token=token)
        except Appointments.DoesNotExist:
            return Response(
                {"error": "Token inválido"}, status=status.HTTP_400_BAD_REQUEST
            )

        appointment_datetime = datetime.combine(appointment.date, appointment.hour)
        now = datetime.now()

        if appointment_datetime - now < timedelta(hours=1):
            return Response(
                {"error": "La cita no puede cancelarse menos de una hora antes."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"patient_name": appointment.patient.name}, status=status.HTTP_200_OK
        )
