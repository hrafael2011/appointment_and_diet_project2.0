
from django import forms
from .models import Diet

class DietForm(forms.ModelForm):
    # Campos para los 7 días
    for dia in range(1, 8):
        for comida in ['desayuno', 'almuerzo', 'merienda', 'cena']:
            locals()[f'{comida}{dia}'] = forms.CharField(
                label=f'{comida.capitalize()} Día {dia}',
                required=False,
                widget=forms.Textarea(attrs={'rows': 2, 'style': 'width: 100%'})
            )

    class Meta:
        model = Diet
        fields = ['patient', 'is_active', 'is_hidden']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for dia in range(1, 8):
            day_data = getattr(self.instance, f'day{dia}', {}) or {}
            for comida in ['desayuno', 'almuerzo', 'merienda', 'cena']:
                self.fields[f'{comida}{dia}'].initial = day_data.get(comida, '')

    def save(self, commit=True):
        instance = super().save(commit=False)
        for dia in range(1, 8):
            day = {
                "dia": dia,
                "desayuno": self.cleaned_data.get(f'desayuno{dia}', ''),
                "almuerzo": self.cleaned_data.get(f'almuerzo{dia}', ''),
                "merienda": self.cleaned_data.get(f'merienda{dia}', ''),
                "cena": self.cleaned_data.get(f'cena{dia}', ''),
            }
            setattr(instance, f'day{dia}', day)
        if commit:
            instance.save()
        return instance
