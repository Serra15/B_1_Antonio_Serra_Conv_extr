# Generated by Django 5.2.2 on 2025-06-09 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relecloud', '0004_auto_20210331_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='image',
            field=models.ImageField(blank=True, help_text='Imagen representativa del destino.', null=True, upload_to='destination_images/'),
        ),
    ]
