from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User 
from django.db.models import Avg 

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
        return reverse('destination_detail', args=[str(self.id)])

    @property
    def average_rating(self):
        # Calcula la media de todas las opiniones de todos los cruceros que van a este destino.
        return Review.objects.filter(cruise__destinations=self).aggregate(Avg('rating'))['rating__avg']


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
        return reverse('cruise_detail', args=[str(self.id)])

    @property
    def average_rating(self):
        # Calcula la media de todas las opiniones ('reviews') asociadas a este crucero.
        # self.reviews.all() funciona gracias al related_name='reviews' del modelo Review
        return self.reviews.aggregate(Avg('rating'))['rating__avg']


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


class Review(models.Model):
    cruise = models.ForeignKey(Cruise, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (4, '⭐⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐')])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Un usuario solo puede dejar una opinión por crucero.
        unique_together = ('cruise', 'user')

    def __str__(self):
        return f'Opinión de {self.user.username} sobre {self.cruise.name}'