# Generated by Django 5.1.6 on 2025-02-28 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_remove_appointments_hour_remove_appointments_status_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='availability',
        ),
    ]
