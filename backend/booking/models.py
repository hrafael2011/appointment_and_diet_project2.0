from django.db import models
from patient.models import Patient
from doctor.models import Doctor
import uuid

# Create your models here.

class Appointments(models.Model):
    STATUS_CHOCSES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('canceled', 'Cancelada'),
        ('finished', 'Finalizada'),

    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False, default=1)
    patient = models.ForeignKey(Patient, related_name='appointments', on_delete=models.CASCADE, null=False, default=1)
    date = models.DateField(null=True, blank=True)
    hour = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=120, choices=STATUS_CHOCSES, default='pending', null=True)
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False, blank=True, null=True )  # Token único para confirmar por correo
    google_event_id = models.CharField(max_length=255, blank=True, null=True)  # Para almacenar el ID del evento en Google Calendar
    reminder_12h_sent = models.BooleanField(default=False)
    reminder_1h_sent = models.BooleanField(default=False)
    whatsapp_code = models.CharField(max_length=6, blank=True, null=True)  # Código para confirmar por WhatsApp
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    update_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.patient.name}"
    
    

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'

    
    
    def delete(self, *args, **kwargs):
        self.is_hidden = True
        self.is_active = True
        self.save()

    def save(self, *args, **kwargs):
        # Generar un token único solo si no existe
        if not self.confirmation_token:
            while True:
                new_uuid = uuid.uuid4()
                if not Appointments.objects.filter(confirmation_token=new_uuid).exists():
                    self.confirmation_token = new_uuid
                    break
        super().save(*args, **kwargs)


