# Generated by Django 5.1.6 on 2025-03-12 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0013_appointments_google_event_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointments',
            name='is_confirmed',
        ),
    ]
