
from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.timezone import now
from django.db.models import Value, CharField
from django.db.models.functions import Concat

from .models import Diet
from .forms import DietForm
from .task import create_patient_diet


@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    form = DietForm
    list_display = ('get_full_name', 'create_at', 'is_active', 'is_hidden')
    list_display_links = None
    search_fields = ('patient__name', 'patient__last_name')

    fieldsets = (
        ('Paciente y estado', {
            'fields': ('patient', 'is_active', "diet_note", 'is_hidden')
        }),
        
        #*[
         #   (f'Día {dia}', {
          #      'fields': (
           #         f'desayuno{dia}',
            #        f'almuerzo{dia}',
             #       f'merienda{dia}',
              #      f'cena{dia}',
               # ),
                #'classes': ('collapse',)  # Quita esto si no quieres que se colapsen
            #}) for dia in range(1, 8)
        #]
    )

    def get_full_name(self, obj):
        return f"{obj.patient.name} {obj.patient.last_name}"

    get_full_name.short_description = 'Paciente'

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        patient_id = request.GET.get("patient")
        diet_note = request.GET.get("diet_note")
        if patient_id and diet_note:
            initial["patient"] = patient_id
            initial["diet_note"] = diet_note
        return initial

    def save_model(self, request, obj, form, change):
        self.redirect_to_historial = False  # Reset

        try:
            request.session['esperando_dieta_inicio'] = now().isoformat()
            create_patient_diet.delay(patient_id=obj.patient.id, diet_note=obj.diet_note)
            self.message_user(request, "La dieta se está generando en segundo plano.")
            self.redirect_to_historial = True
        except Exception as e:
            self.message_user(request, f"Error al generar la dieta: {str(e)}", level="error")

    def response_post_save(self, request, obj):
        return HttpResponseRedirect(reverse("admin:diet_diet_change", args=[obj.pk]))

    def response_add(self, request, obj, post_url_continue=None):
        if getattr(self, 'redirect_to_historial', False):
            return HttpResponseRedirect(reverse('esperar_dieta', args=[obj.patient.id]))
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if getattr(self, 'redirect_to_historial', False):
            return HttpResponseRedirect(reverse('historial_dietas', args=[obj.patient.id]))
        return super().response_change(request, obj)

    def get_search_results(self, request, queryset, search_term):
        # Permitir búsqueda por nombre completo
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        full_name_matches = self.model.objects.annotate(
            full_name=Concat(
                'patient__name',
                Value(' '),
                'patient__last_name',
                output_field=CharField()
            )
        ).filter(full_name__icontains=search_term)

        queryset |= full_name_matches
        return queryset, use_distinct
