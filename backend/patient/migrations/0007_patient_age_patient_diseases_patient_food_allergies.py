# Generated by Django 5.1.6 on 2025-04-01 14:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0006_patient_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='age',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(150)], verbose_name='Edad'),
        ),
        migrations.AddField(
            model_name='patient',
            name='diseases',
            field=models.TextField(blank=True, null=True, verbose_name='Enfermedades o Lesiones que padece'),
        ),
        migrations.AddField(
            model_name='patient',
            name='food_allergies',
            field=models.TextField(blank=True, null=True, verbose_name='Alimentos que no consume o es alergico'),
        ),
    ]
