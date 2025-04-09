# widgets.py
from django import forms

class TimePickerWidget(forms.TimeInput):
    input_type = 'time'  # Esto crea un campo de entrada de tipo "time" con el formato HH:MM.
