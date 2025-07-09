

from django.contrib import admin
from django.urls import reverse
from django.db.models import Value, CharField
from django.db.models.functions import Concat
from django.utils.html import format_html
from django import forms
from .models import Patient
from diet.models import Diet
from doctor.models import Doctor
from diet.forms import DietForm



# 🔧 Formulario personalizado para mostrar u ocultar el campo 'doctor'
class PatientAdminForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if not user.is_superuser:
            self.fields['doctor'].widget = forms.HiddenInput()
            self.fields['doctor'].required = False


# 🔁 Mixin para filtrar objetos que no estén ocultos
class SoftDeleteMixin:
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_hidden=False)


# 🧠 Admin principal del modelo Patient
@admin.register(Patient)
class PatientAdmin(SoftDeleteMixin, admin.ModelAdmin):
    form = PatientAdminForm
    list_display = ('name', 'last_name', 'is_active', 'historial_dietas_link')
    search_fields = ('name','last_name')
    list_filter = ('is_active',)
    exclude = ('is_hidden',)

    # 🔄 Pasa el usuario logueado al formulario
    def get_form(self, request, obj=None, **kwargs):
        AdminForm = super().get_form(request, obj, **kwargs)

        class WrappedAdminForm(AdminForm):
            def __new__(cls, *args, **kw):
                kw['user'] = request.user
                return AdminForm(*args, **kw)

        return WrappedAdminForm

    # 🔒 Asigna el doctor automáticamente si no es superuser
    def save_model(self, request, obj, form, change):
        if not obj.doctor and not request.user.is_superuser:
            try:
                obj.doctor = Doctor.objects.get(user=request.user)
            except Doctor.DoesNotExist:
                pass  # Puedes mostrar error si quieres forzar la existencia
        obj.save()

    # 🔎 Filtra los pacientes según el doctor logueado
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        try:
            doctor = request.user.doctor
            return queryset.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            return queryset.none()
        
    def get_search_results(self, request, queryset, search_term):
        # Búsqueda por nombre o apellido como siempre
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Añade filtro por nombre completo (name + last_name)
        full_name_queryset = self.model.objects.annotate(
            full_name=Concat('name', Value(' '), 'last_name', output_field=CharField())
        ).filter(full_name__icontains=search_term)

        # Une ambos querysets
        queryset |= full_name_queryset

        return queryset, use_distinct

    # 🔗 Enlace al historial de dietas del paciente
    def historial_dietas_link(self, obj):
        url = reverse('historial_dietas', args=[obj.pk])
        return format_html('<a href="{}">Ver historial de dietas</a>', url)

    historial_dietas_link.short_description = 'Historial de dietas'












"""
    from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Patient
from diet.models  import Diet
from doctor.models import Doctor
from diet.forms import DietForm

from django import forms


class PatientAdminForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if not user.is_superuser:
            self.fields['doctor'].widget = forms.HiddenInput()
            self.fields['doctor'].required = False


# Register your models here.

class SoftDeleteMixin:
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_hidden=False)

"""
#class DietInline(admin.StackedInline):
    #model = Diet
    #extra = 1
    ##fields = ("day1","day2",'create_at', 'is_active', 'is_hidden')
    #readonly_fields = ('create_at','ver_enlace')
    #ordering = ['-create_at']

    #def ver_enlace(self, obj):
        
        #url = reverse('admin:diet_diet_change', args=[obj.pk])
        #return format_html('<a href="{}">Editar dieta</a>', url)

    #ver_enlace.short_description = "Acciones"

"""


    
"""

"""
@admin.register(Patient)
class PatientAdmin(SoftDeleteMixin,admin.ModelAdmin):
    list_display=('name','last_name','is_active','historial_dietas_link')
    search_fields=('name',)
    list_filter = ('is_active',)
    exclude = ('is_hidden',)
    #inlines = [DietInline]
    #form = DietForm
    #readonly_fields =('doctor',)

    def historial_dietas_link(self, obj):
        url = reverse('historial_dietas', args=[obj.pk])
        return format_html('<a href="{}">Ver historial de dietas</a>', url)

    historial_dietas_link.short_description = 'Historial de dietas'

    
   


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


"""
