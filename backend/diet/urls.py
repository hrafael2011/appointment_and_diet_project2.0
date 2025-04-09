

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import DietView

router = DefaultRouter()
router.register('diet', DietView)

urlpatterns = router.urls