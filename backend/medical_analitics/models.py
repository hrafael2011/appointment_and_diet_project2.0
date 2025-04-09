from django.db import models
from patient.models import Patient

# Create your models here.


class Analitics(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='Analiticas')
    file = models.FileField(upload_to='analitics/') 
    proccesed = models.BooleanField(default=False)
    createAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient.name}'


class MedicalTest(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Result(models.Model):
    analitics = models.ForeignKey(Analitics, on_delete=models.CASCADE, related_name="resultados")
    medical_text = models.ForeignKey(MedicalTest, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)  # Almacena valores como "58", "100", etc.

    def __str__(self):
        return f"{self.estudio.nombre}: {self.valor}"