from django.db import models
from patient.models import Patient

# Create your models here.

class Diet(models.Model):
    
    patient = models.ForeignKey(Patient, related_name='diet', on_delete=models.CASCADE)
    diet = models.JSONField(null=True, blank=True)  # JSON completo
    day1 = models.JSONField(null=True, blank=True)
    day2 = models.JSONField(null=True, blank=True)
    day3 = models.JSONField(null=True, blank=True)
    day4 = models.JSONField(null=True, blank=True)
    day5 = models.JSONField(null=True, blank=True)
    day6 = models.JSONField(null=True, blank=True)
    day7 = models.JSONField(null=True, blank=True)
    diet_note = models.TextField(max_length=1000, blank=True, null=True, verbose_name="Instrucciones Extra para la dieta")
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    update_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False)

    class Meta: 
        verbose_name = 'Dieta'
        verbose_name_plural = 'Dieta'

    def __str__(self):
        return f"{self.patient.name} {self.patient.last_name}"

    def delete(self, *args, **kwargs):
        self.is_hidden = True
        self.is_active = False
        self.save()

    def save(self, *args, **kwargs):
        if self.diet and isinstance(self.diet, dict):
            days = self.diet.get("dias", [])
            for day in days:
                num = day.get("dia")
                if num in range(1, 8):
                    setattr(self, f"day{num}", day)
        super().save(*args, **kwargs)


