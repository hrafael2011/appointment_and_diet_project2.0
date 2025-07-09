"""
URL configuration for DraFitApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from patient.viewHistorial import(historial_dietas, 
                                  duplicar_dieta ,
                                  generar_pdf, 
                                  esperar_generacion_dieta,
                                  verificar_dieta_generada,
                                  eliminar_dieta
                                  ) 

from diet.views import actualizar_dieta

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('docs.urls')),
    path('api/', include('core.urls')),
    path('api/', include('booking.urls')),
    path('api/', include('patient.urls')),
    path('api/', include('doctor.urls')),
    path('historial-dietas/<int:patient_id>/', historial_dietas, name='historial_dietas'),
    path('dieta/<int:dieta_id>/pdf/', generar_pdf, name='generar_pdf'),
    path('dieta/<int:dieta_id>/duplicar/', duplicar_dieta, name='duplicar_dieta'),
    path('actualizar-dieta/', actualizar_dieta, name='actualizar_dieta'),
    path('esperar-dieta/<int:patient_id>/', esperar_generacion_dieta, name='esperar_dieta'),
    path('verificar-dieta-generada/<int:patient_id>/', verificar_dieta_generada, name='verificar_dieta_generada'),
    path('dieta/<int:dieta_id>/eliminar/', eliminar_dieta, name='eliminar_dieta'),
    
   
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
