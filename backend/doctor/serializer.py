
from rest_framework import serializers

from .models import DoctorAvailability




class DoctorAvailabilitySerializers(serializers.ModelSerializer):

    class Meta:
        model = DoctorAvailability
        fields = [
            'date',
            'start_hour',
            'end_hour',
            'available',
        ]