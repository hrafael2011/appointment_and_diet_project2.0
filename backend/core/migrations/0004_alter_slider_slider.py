# Generated by Django 5.1.6 on 2025-02-17 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_introductionservice_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='slider',
            field=models.ImageField(upload_to='slider', verbose_name='Slider'),
        ),
    ]
