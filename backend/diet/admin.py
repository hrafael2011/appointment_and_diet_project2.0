from django.contrib import admin
from .models import Diet

# Register your models here.

class SoftDeleteMixin:
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_hidden=False)

@admin.register(Diet)
class DietAdmin(SoftDeleteMixin,admin.ModelAdmin):
    list_display=('patient','is_active')
    search_fields=('patient',)
    list_filter=('is_active',)
    exclude=('is_hidden',)

