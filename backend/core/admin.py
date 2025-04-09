from django.contrib import admin
from .models import (
    Logo,
    Nav,
    Slider,
    IntroductionService,
    AllService,
    BeforeAndAfter,
    WhoWeAre,
    TestimonyPatients,
    InfoPlans,
    DetailPlans,
)

# Register your models here.


# ocuta los datos que yo no unsaremos , pers se quedan en la base de datos
class SoftDeleteMixin:
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_hidden=False)


@admin.register(Nav)
class NavAdmin(SoftDeleteMixin, admin.ModelAdmin):
    list_display = ("name_es", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name_es",)
    exclude = ("is_hidden",)


@admin.register(Slider)
class SliderAdmin(SoftDeleteMixin, admin.ModelAdmin):
    list_display = ("title_es", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)
    exclude = ("is_hidden",)


@admin.register(Logo)
class LogoAdmin(SoftDeleteMixin, admin.ModelAdmin):
    list_display = ("description", "is_active")
    list_filter = ("is_active",)
    search_fields = ("description",)
    exclude = ("is_hidden",)


@admin.register(IntroductionService)
class IntroductionServiceAdmin(SoftDeleteMixin, admin.ModelAdmin):
    list_display = ("title_es", "is_active")
    list_filter = ("title_es",)
    search_fields = ("title_es",)
    exclude = ("is_hidden",)


@admin.register(BeforeAndAfter)
class BeforeAndAfterAdmin(SoftDeleteMixin, admin.ModelAdmin):
    list_display = ("title_es", "is_active")
    list_filter = ("title_es",)
    search_fields = ("title_es",)
    exclude = ("is_hidden",)


@admin.register(WhoWeAre)
class WhoWeAreAdmin(SoftDeleteMixin, admin.ModelAdmin):
    list_display = ("title_es", "is_active")
    list_filter = ("title_es",)
    search_fields = ("title_es",)
    exclude = ("is_hidden",)


@admin.register(AllService)
class AllServicesAdmin(SoftDeleteMixin, admin.ModelAdmin):
    list_display = ("title_es", "is_active")
    list_filter = ("title_es",)
    search_fields = ("title_es",)
    exclude = ("is_hidden",)

@admin.register(TestimonyPatients)
class TestimonyPatientsAdmin(SoftDeleteMixin, admin.ModelAdmin):
    list_display = ("title_es", "is_active")
    list_filter = ("title_es",)
    search_fields = ("title_es",)
    exclude = ("is_hidden",)

@admin.register(InfoPlans)
class InfoPlanssAdmin(SoftDeleteMixin, admin.ModelAdmin):
    list_display = ("title_es", "is_active")
    list_filter = ("title_es",)
    search_fields = ("title_es",)
    exclude = ("is_hidden",)

@admin.register(DetailPlans)
class InfoPlanssAdmin(SoftDeleteMixin, admin.ModelAdmin):
    list_display = ("detail_es", "is_active")
    list_filter = ("detail_es",)
    search_fields = ("detail_es",)
    exclude = ("is_hidden",)