
from rest_framework.routers import DefaultRouter

from .views import DoctorAvailabilityView

router = DefaultRouter()
router.register('doctor', DoctorAvailabilityView)

urlpatterns = router.urls