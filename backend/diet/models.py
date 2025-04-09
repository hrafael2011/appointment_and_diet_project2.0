from django.db import models
from patient.models import Patient

# Create your models here.

class Diet(models.Model):
    STATUS_CHOCSES = [
        ('pendient', 'Pendiente'),
        ('canceled', 'Cancelada'),
        ('rejected', 'Rechazada'),

    ]

    patient = models.ForeignKey(Patient, related_name='diet', on_delete=models.CASCADE)
    plan = models.JSONField(default=dict)
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    update_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)


    class Meta: 
        verbose_name = 'Dieta'
        verbose_name_plural = 'Dieta'

    def __str__(self):
        return self.patient.name
    
    def delete(self, *args, **kwargs):
        self.is_hidden = True
        self.is_active = False
        self.save()