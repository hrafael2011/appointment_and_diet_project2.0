# Generated by Django 5.1.6 on 2025-02-28 22:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_availability_doctor'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_hour', models.TimeField()),
                ('end_hour', models.TimeField()),
                ('available', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_hidden', models.BooleanField(default=False)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor')),
            ],
            options={
                'verbose_name': 'Disponibilidad',
                'verbose_name_plural': 'Disponibilidad',
            },
        ),
        migrations.DeleteModel(
            name='Availability',
        ),
    ]
