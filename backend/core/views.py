from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    Nav,
    Slider,
    Logo,
    IntroductionService,
    BeforeAndAfter,
    WhoWeAre,
    AllService,
    TestimonyPatients,
    InfoPlans,
    DetailPlans
)
from .serializers import (
    NavSerializers,
    SliderSerializers,
    LogoSerializers,
    IntroductionServiceSerializers,
    BeforeAndAfterSerializers,
    WhoWeAreSerializers,
    AllServiceSerializers,
    TestimonyPatientsSerializers,
    InfoPlansSerializers,
    DetailPlansSerializers
)


# Create your views here.


class LogoView(APIView):
    def get(self, request):
        logo = Logo.objects.filter(is_active=True)
        serializer = LogoSerializers(logo, many=True, context={"request": request})
        return Response(serializer.data)


class NavView(APIView):

    def get(self, request):
        nav = Nav.objects.filter(is_active=True)
        serializer = NavSerializers(nav, many=True)
        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        language = self.request.headers.get('Accept-Language', 'es')[:2]  # Idioma
        context.update({'language': language, 'request': self.request})  # Incluye 'request'
        return context


class SliderView(APIView):

    def get(self, request):
        slider = Slider.objects.filter(is_active=True)
        serializer = SliderSerializers(slider, many=True, context={"request": request})
        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        language = self.request.headers.get('Accept-Language', 'es')[:2]  # Idioma
        context.update({'language': language, 'request': self.request})  # Incluye 'request'
        return context


class IntroductionServiceView(APIView):

    def get(self, request):
        introductionServices = IntroductionService.objects.filter(is_active=True)
        serializer = IntroductionServiceSerializers(
            introductionServices, many=True, context={"request": request}
        )
        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        language = self.request.headers.get('Accept-Language', 'es')[:2]  # Idioma
        context.update({'language': language, 'request': self.request})  # Incluye 'request'
        return context


class BeforeAndAfterView(APIView):

    def get(get, request):
        befoteAfter = BeforeAndAfter.objects.filter(is_active=True)
        serializer = BeforeAndAfterSerializers(
            befoteAfter, many=True, context={"request": request}
        )

        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        language = self.request.headers.get('Accept-Language', 'es')[:2]  # Idioma
        context.update({'language': language, 'request': self.request})  # Incluye 'request'
        return context


class WhoWeAreView(APIView):

    def get(get, request):
        whoWeAre = WhoWeAre.objects.filter(is_active=True)
        serializer = WhoWeAreSerializers(
            whoWeAre, many=True, context={"request": request}
        )

        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        language = self.request.headers.get('Accept-Language', 'es')[:2]  # Idioma
        context.update({'language': language, 'request': self.request})  # Incluye 'request'
        return context


class AllServiceView(APIView):

    def get(get, request):
        allServices = AllService.objects.filter(is_active=True)
        serializer = AllServiceSerializers(
            allServices, many=True, context={"request": request}
        )

        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        language = self.request.headers.get('Accept-Language', 'es')[:2]  # Idioma
        context.update({'language': language, 'request': self.request})  # Incluye 'request'
        return context


class TestimonyPatientsView(APIView):

    def get(get, request):
        testimonial = TestimonyPatients.objects.filter(is_active=True)
        serializer = TestimonyPatientsSerializers(
            testimonial, many=True, context={"request": request}
        )

        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        language = self.request.headers.get('Accept-Language', 'es')[:2]  # Idioma
        context.update({'language': language, 'request': self.request})  # Incluye 'request'
        return context


class InfoPlansView(APIView):

    def get(get, request):
        infoPlans = InfoPlans.objects.filter(is_active=True)
        serializer = InfoPlansSerializers(
            infoPlans, many=True, context={"request": request}
        )

        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        language = self.request.headers.get('Accept-Language', 'es')[:2]  # Idioma
        context.update({'language': language, 'request': self.request})  # Incluye 'request'
        return context
    

class DetailPlansView(APIView):

    def get(get, request):
        detailPlans = DetailPlans.objects.filter(is_active=True)
        serializer = DetailPlansSerializers(
            detailPlans, many=True, context={"request": request}
        )

        return Response(serializer.data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        language = self.request.headers.get('Accept-Language', 'es')[:2]  # Idioma
        context.update({'language': language, 'request': self.request})  # Incluye 'request'
        return context
