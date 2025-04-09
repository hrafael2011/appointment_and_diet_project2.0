

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AppointmentsView

router = DefaultRouter()
router.register('appointment', AppointmentsView)

urlpatterns = router.urls