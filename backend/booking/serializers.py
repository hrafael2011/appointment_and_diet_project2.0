from rest_framework import serializers
from .models import Appointments

class AppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = [
            'id',
            'doctor',
            'patient',
            'date',
            'hour',

    
    ]
    