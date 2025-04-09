from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializer import DoctorAvailabilitySerializers
from .models import DoctorAvailability


class DoctorAvailabilityView(viewsets.ModelViewSet):
    queryset = DoctorAvailability.objects.filter(available=True)
    serializer_class = DoctorAvailabilitySerializers


    @action(detail=False, methods=['get'], url_path='available')
    def get_schedule_available(self, request):
        '''
        Personalized action to get schedule available according to the date
        '''
        date = request.query_params.get('date')
        print('Esta es la fecha', date)
        if not date:
            return Response(
                {'error': 'The date is required'},
                status=status.HTTP_400_BAD_REQUEST
                
            )
        availability = DoctorAvailability.objects.filter(date=date )

        #Format the response
        schedule_available = [{'hour': available.start_hour.strftime('%H:%M')} for available in availability]

        return Response(schedule_available, status=status.HTTP_200_OK)
        



