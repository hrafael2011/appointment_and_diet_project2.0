# Generated by Django 5.1.6 on 2025-03-11 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0012_appointments_reminder_12h_sent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointments',
            name='google_event_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='status',
            field=models.CharField(choices=[('pending', 'Pendiente'), ('confirmed', 'Confirmada'), ('canceled', 'Cancelada'), ('finished', 'Finalizada')], default='pending', max_length=120, null=True),
        ),
    ]
