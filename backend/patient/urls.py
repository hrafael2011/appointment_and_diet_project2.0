

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PatientView

router = DefaultRouter()
router.register('patient', PatientView)

urlpatterns = router.urls