from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_datetime
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Patient
from diet.models import Diet
from .task import send_pdf_email, send_whatsapp_pdf_task
from django.conf import settings
import os

import copy

def historial_dietas(request, patient_id):
    paciente = get_object_or_404(Patient, pk=patient_id)
    #dietas = paciente.diet.order_by('-create_at')
    # FILTRAR solo las dietas activas y no ocultas
    dietas = paciente.diet.filter(is_active=True, is_hidden=False).order_by('-create_at')
    paginator = Paginator(dietas, 1)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Agrega una propiedad temporal a cada dieta con los días en una lista
    for dieta in page_obj:
        dieta.dias = [
            dieta.day1,
            dieta.day2,
            dieta.day3,
            dieta.day4,
            dieta.day5,
            dieta.day6,
            dieta.day7
        ]

    return render(request, 'dietas/historial.html', {
        'paciente': paciente,
        'page_obj': page_obj
    })


def duplicar_dieta(request, dieta_id):
    dieta_original = get_object_or_404(Diet, pk=dieta_id)
    nueva = copy.copy(dieta_original)
    nueva.pk = None  # Esto le dice a Django: "esto es un nuevo registro"
    nueva.save()
    return redirect('historial_dietas', patient_id=dieta_original.patient.id)



def link_callback(uri, rel):
    """
    Convierte URIs (como los usados por MEDIA_URL o STATIC_URL) en rutas absolutas del sistema de archivos.
    Necesario para que xhtml2pdf pueda acceder a imágenes y estilos.
    """
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = finders.find(uri.replace(settings.STATIC_URL, ""))
    else:
        return uri

    if not os.path.isfile(path):
        raise Exception(f'Media URI must exist: {path}')
    return path

def generar_pdf(request, dieta_id):
    action = request.GET.get('action', 'download')

    #dieta = Diet.objects.get(pk=dieta_id)
    dieta = get_object_or_404(Diet, pk=dieta_id)
    paciente = dieta.patient

    # Prepara los datos para la plantilla
    template = get_template('dietas/dieta_pdf.html')
    html = template.render({
        'dieta': dieta,
        'dias': [
            dieta.day1, dieta.day2, dieta.day3, dieta.day4,
            dieta.day5, dieta.day6, dieta.day7
        ],
        'logo_path': os.path.join(settings.MEDIA_URL, 'logo', 'drafitlogo.png')
    })

    #if action == "email":
       # send_pdf_email.delay(dieta_id)
        #messages.success(request, "✅ El PDF ha sido enviado por correo al paciente.")
        #return redirect('historial_dietas', patient_id=paciente.id)

    if action == "email":
        send_pdf_email.delay(dieta_id)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": True, "message": "📧 El PDF ha sido enviado por correo."})
        return HttpResponse("✅ El PDF ha sido enviado por correo al paciente.", content_type="text/plain")

    
    
    if action == "whatsapp":
        send_whatsapp_pdf_task.delay(paciente.name, paciente.last_name, paciente.doctor.name, paciente.whatsapp, dieta_id)
        return HttpResponse("✅ El PDF ha sido enviado por WhatsApp al paciente.", content_type="text/plain")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Plan_Nutricional_{paciente.name}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    if pisa_status.err:
        return HttpResponse('❌ Error al generar el PDF', content_type='text/plain')

    return response


def esperar_generacion_dieta(request, patient_id):
    return render(request, "dietas/esperar_generacion_dieta.html", {"patient_id": patient_id})


def verificar_dieta_generada(request, patient_id):
    marca = request.session.get("esperando_dieta_inicio")
    if not marca:
        return JsonResponse({"generada": False})

    try:
        marca_dt = parse_datetime(marca)
        dieta_reciente = Diet.objects.filter(
            patient_id=patient_id,
            create_at__gte=marca_dt
        ).exists()
        return JsonResponse({"generada": dieta_reciente})
    except Exception as e:
        return JsonResponse({"generada": False, "error": str(e)})
    
@login_required
def eliminar_dieta(request, dieta_id):
    dieta = get_object_or_404(Diet, pk=dieta_id)

    if request.method == "POST":
        dieta.is_hidden = True
        dieta.is_active = False
        dieta.save()


        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": True})
        else:
            messages.success(request, "✅ La dieta ha sido eliminada correctamente.")
            return redirect('historial_dietas', patient_id=dieta.patient.id)

    return JsonResponse({"success": False, "error": "Método inválido"}, status=400)
        
        #messages.success(request, "✅ La dieta ha sido eliminada correctamente.")
    
   # return redirect('historial_dietas', patient_id=dieta.patient.id)