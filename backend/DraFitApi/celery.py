from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Configurar Celery con los ajustes de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DraFitApi.settings')
app = Celery('DraFitApi')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'America/Santo_Domingo'  # Zona horaria de Celery

# Autodiscover tasks dentro de cada app
app.autodiscover_tasks()
app.conf.worker_pool = 'solo'
app.conf.result_backend = 'redis://172.17.0.2:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'



