# Generated by Django 5.1.6 on 2025-02-21 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='diet',
            options={'verbose_name': 'Dieta', 'verbose_name_plural': 'Dieta'},
        ),
        migrations.AddField(
            model_name='diet',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='diet',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='diet',
            name='update_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='diet',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
