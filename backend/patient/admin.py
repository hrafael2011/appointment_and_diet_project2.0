from django.contrib import admin
from .models import Patient
from doctor.models import Doctor



# Register your models here.

class SoftDeleteMixin:
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_hidden=False)

@admin.register(Patient)
class PatientAdmin(SoftDeleteMixin,admin.ModelAdmin):
    list_display=('name','last_name','is_active')
    search_fields=('name',)
    list_filter = ('is_active',)
    exclude = ('is_hidden',)
    readonly_fields =('doctor',)


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset  # Si el usuario es superusuario, ve todas las citas
        try:
            # Si el usuario tiene asociado un doctor, filtra las citas solo para ese doctor
            doctor = request.user.doctor  # Asumiendo que el usuario tiene una relación OneToOne con Doctor
            return queryset.filter(doctor=doctor)
        except:
            return queryset.none()  # Si el usuario no tiene un doctor asociado, no ve ninguna cita


    def save_model(self, request, obj, form, change):
        # Asignar automáticamente el doctor basado en el usuario que está creando la cita
        if not obj.doctor:
            obj.doctor = Doctor.objects.get(user=request.user)  # Asignar el doctor logueado
        obj.save()
