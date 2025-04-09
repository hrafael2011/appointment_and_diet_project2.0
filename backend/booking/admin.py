from django.contrib import admin
from .models import Appointments
from doctor.models import Doctor



# Registro de clases para SoftDeleteMixin
class SoftDeleteMixin:
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_hidden=False)

# Crear el formulario para el modelo de Cita


# Registro de la clase AppointmentsAdmin en el admin de Django
@admin.register(Appointments)
class AppointmetsAdmin(SoftDeleteMixin, admin.ModelAdmin):
   
    list_display = ('patient', 'date', 'hour', 'status')
    fields = ['patient', 'date', 'hour','doctor','status']
    readonly_fields = ['patient','doctor','status']  # Hacer solo lectura para 'doctor'
    search_fields = ('patient',)
    list_filter = ('is_active',)
    exclude = ('is_hidden',)

 # Personalizamos el queryset para que solo el doctor vea sus propias citas
   
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
    



