
from rest_framework import serializers

from .models import Diet


class DietSerializers(serializers.ModelSerializer):
    class Meta:
        model = Diet
        fields = [
            'id',
            'patient',
            'plan'    
        ]