# Generated by Django 5.1.6 on 2025-02-28 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_availability_delete_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='availability',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='availability',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='availability',
            name='update_at',
            field=models.DateField(auto_now=True),
        ),
    ]
