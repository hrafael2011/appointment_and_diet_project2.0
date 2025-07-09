from django.shortcuts import render
from django.http import JsonResponse
from .models import Diet
from patient.models import Patient

def esperar_generacion_dieta(request, patient_id):
    return render(request, "dietas/esperar_generacion_dieta.html", {"patient_id": patient_id})

def verificar_dieta_generada(request, patient_id):
    existe_dieta = Diet.objects.filter(patient_id=patient_id).exists()
    return JsonResponse({"generada": existe_dieta})
