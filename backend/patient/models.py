from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from doctor.models import Doctor

# Create your models here.

class Patient(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE, null=True, blank=True )
    name = models.CharField(max_length=150, verbose_name='Nombre',null=True , blank=True)
    last_name = models.CharField(max_length=150, verbose_name='Apellido',null=True , blank=True)
    DOB = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento'),
    sex = models.CharField(null=True, blank=True, verbose_name='Sexo')
    weight = models.IntegerField(verbose_name='Peso', null=True , blank=True)
    height = models.IntegerField(verbose_name='Estatura' ,null=True , blank=True)
    objetive = models.CharField(max_length=100 ,null=True , blank=True)
    whatsapp = models.CharField(max_length=30, verbose_name='Whatsapp' ,null=True , blank=True)
    email = models.EmailField(verbose_name='Correo Electronico' ,null=True , blank=True)
    country = models.CharField(max_length=100, verbose_name='Pais',null=True , blank=True)
    city = models.CharField(max_length=100, verbose_name='Pais',null=True , blank=True)
    food_allergies = models.TextField(null=True, blank=True, verbose_name='Alimentos que no consume o es alergico')
    diseases = models.TextField(null=True, blank=True, verbose_name='Enfermedades o Lesiones que padece')
    medical_history = models.TextField(max_length=500, verbose_name='Historia Clinica',null=True , blank=True)
    create_at = models.DateTimeField(auto_now_add=True ,null=True)
    update_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Pacientes'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        self.is_hidden = True
        self.is_active = False
        self.save()


 


