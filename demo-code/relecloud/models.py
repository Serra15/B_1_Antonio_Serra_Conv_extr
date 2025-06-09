from django.db import models
from django.urls import reverse

class Destination(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    image = models.ImageField(
        upload_to='destination_images/', 
        blank=True, 
        null=True, 
        help_text="Imagen representativa del destino."
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # Devuelve la URL para la página de detalle de este destino.
        # 'destination_detail' debe ser el name= que le diste a la URL en urls.py
        return reverse('destination_detail', args=[str(self.id)])

class Cruise(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    destinations = models.ManyToManyField(
        Destination,
        related_name='cruises'
    )
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Devuelve la URL para la página de detalle de este crucero.
        # 'cruise_detail' debe ser el name= que le diste a la URL en urls.py
        return reverse('cruise_detail', args=[str(self.id)])


class InfoRequest(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    email = models.EmailField()
    notes = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.PROTECT
    )
    def __str__(self):
        return f'Solicitud de {self.name} sobre {self.cruise}'