from django.shortcuts import render
from rest_framework import viewsets

from .models import Patient
from .serializers import PatientSerializers



# Create your views here.

class PatientView(viewsets.ModelViewSet):

    queryset = Patient.objects.filter(is_active=True)
    serializer_class = PatientSerializers
    