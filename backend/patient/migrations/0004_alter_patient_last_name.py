# Generated by Django 5.1.6 on 2025-02-22 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_alter_patient_city_alter_patient_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Nombre'),
        ),
    ]
