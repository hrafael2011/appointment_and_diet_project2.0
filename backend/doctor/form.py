from django import forms
from .models import DoctorAvailability
from .widgets import TimePickerWidget

class DisponibilidadForm(forms.ModelForm):
    # Usamos el widget personalizado para los campos de hora
    start_hour = forms.TimeField(widget=TimePickerWidget(attrs={'class': 'vDateField'}))
    end_hour = forms.TimeField(widget=TimePickerWidget(attrs={'class': 'vDateField'}))

    class Meta:
        model = DoctorAvailability
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_hour = cleaned_data.get('start_hour')
        end_hour = cleaned_data.get('end_hour')

        # Verificar las reglas adicionales en el formulario
        if end_hour <= start_hour:
            raise forms.ValidationError('La hora de fin debe ser posterior a la hora de inicio.')

        if (end_hour.hour - start_hour.hour) < 1:  # Duración mínima de 1 hora
            raise forms.ValidationError('La disponibilidad debe durar al menos una hora.')

        # Verificar que no exista otra disponibilidad con la misma hora en el mismo día
        if DoctorAvailability.objects.filter(date=date, start_hour=start_hour).exists():
            raise forms.ValidationError(f"Ya existe una disponibilidad para la hora {start_hour} el {date}.")

        return cleaned_data
