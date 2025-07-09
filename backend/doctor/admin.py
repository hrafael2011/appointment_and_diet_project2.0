from django.contrib import admin
from .models import Doctor, DoctorAvailability
from .form import DisponibilidadForm

# Registro de clases para SoftDeleteMixin
class SoftDeleteMixin:
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_hidden=False)


# Register your models here.
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'whatsapp_number')  # Campos visibles en la lista
    search_fields = ('name', 'whatsapp_number')  # Buscar por nombre y número de WhatsApp
    list_filter = ('user__is_active',)  # Filtro por estado activo del usuario
    readonly_fields = ("email",)


# Registro de la clase AvailabilityAdmin en el admin de Django
@admin.register(DoctorAvailability)
class DoctorAvailability(SoftDeleteMixin, admin.ModelAdmin):
    form = DisponibilidadForm
    list_display = ('date', 'start_hour', 'end_hour', 'available', 'doctor')
    fields =['date', 'start_hour', 'end_hour', 'available','doctor']
    #readonly_fields = ['doctor'] # Hacer solo lectura para 'doctor'
    exclude = ('is_hidden',)


    def get_start_hour_24(self, obj):
        return obj.start_hour.strftime('%H:%M')
    get_start_hour_24.short_description = 'Hora Inicio'

    def get_end_hour_24(self, obj):
        return obj.end_hour.strftime('%H:%M')
    get_end_hour_24.short_description = 'Hora Fin'

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