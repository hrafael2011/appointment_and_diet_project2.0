from django.urls import path
from .views import (
    NavView,
    SliderView,
    LogoView,
    IntroductionServiceView,
    BeforeAndAfterView,
    WhoWeAreView,
    AllServiceView,
    TestimonyPatientsView,
    InfoPlansView,
    DetailPlansView
    
)

urlpatterns = [
    path("nav", NavView.as_view(), name="navegation"),
    path("slider", SliderView.as_view(), name="slider"),
    path("logo", LogoView.as_view(), name="logo"),
    path(
        "introduction-services", 
        IntroductionServiceView.as_view(),
        name="introductionServices",
    ),
    path("before-after", BeforeAndAfterView.as_view(), name="beforeAfter"),
    path("whoweare", WhoWeAreView.as_view(), name="whoWeAre"),
    path("all-services", AllServiceView.as_view(), name="allServices"),
    path("testimonial", TestimonyPatientsView.as_view(), name="testimonial"),
    path("info-plan", InfoPlansView.as_view(), name="infoPlnas"),
    path("detail-plan", DetailPlansView.as_view(), name="detailPlnas"),
    
]
