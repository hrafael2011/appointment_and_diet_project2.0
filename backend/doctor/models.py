from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    whatsapp_number = models.CharField(max_length=20, unique=True)  # Número que usará para el chatbot

    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        if self.user and not self.email:
            self.email = self.user.email
        super().save(*args, **kwargs)
    

    

class DoctorAvailability(models.Model):


    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE, null=True, blank=True )
    date = models.DateField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    available = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    update_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Disponibilidad'
        verbose_name_plural = 'Disponibilidad'

    def __str__(self):
       return f'{self.doctor.name}'
    
    def delete(self, *args, **kwargs):
        self.is_hidden = True
        self.is_active = True
        self.save()