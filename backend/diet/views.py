from django.shortcuts import render
from rest_framework import viewsets

from .models import Diet
from .serializers import DietSerializers


# Create your views here.

class DietView(viewsets.ModelViewSet):
    queryset = Diet.objects.filter(is_active=True)
    serializer_class = DietSerializers
