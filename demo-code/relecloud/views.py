# tu_app/views.py

# Imports existentes
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Imports para las vistas de opiniones y popularidad
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.db.models import Avg


# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


def destinations(request):
    """
    Esta vista ahora muestra los 3 destinos más populares basados en la 
    valoración media de las opiniones de sus cruceros.
    """
    # 👇 CAMBIO REALIZADO AQUÍ: Se ha renombrado 'average_rating' a 'avg_rating' para evitar conflictos 👇
    popular_destinations = models.Destination.objects.annotate(
        avg_rating=Avg('cruises__reviews__rating')
    ).filter(
        avg_rating__isnull=False
    ).order_by(
        '-avg_rating'
    )[:3]

    context = {
        'popular_destinations': popular_destinations
    }
    return render(request, 'destinations.html', context)


def all_destinations_list(request):
    """
    Esta vista muestra una lista de todos los destinos, ordenados alfabéticamente.
    """
    all_destinations = models.Destination.objects.order_by('name')
    return render(request, 'all_destinations.html', {'destinations': all_destinations})


class DestinationDetailView(generic.DetailView):
    template_name = 'destination_detail.html'
    model = models.Destination
    context_object_name = 'destination'

class CruiseDetailView(generic.DetailView):
    template_name = 'cruise_detail.html'
    model = models.Cruise
    context_object_name = 'cruise'

class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
    # ... (Tu vista InfoRequestCreate se mantiene igual) ...
    template_name = 'info_request_create.html'
    model = models.InfoRequest
    fields = ['name', 'email', 'cruise', 'notes']
    success_url = reverse_lazy('index')
    success_message = 'Thank you, %(name)s! We will email you when we have more information about %(cruise)s!'

    def form_valid(self, form):
        # ... (tu lógica de correo electrónico aquí, que ya funciona bien) ...
        user_name = form.cleaned_data['name']
        user_email = form.cleaned_data['email']
        subject = 'Confirmación de tu solicitud en Relecloud'
        html_message = render_to_string('email/confirmation_template.html', {'name': user_name})
        plain_message = strip_tags(html_message)
        from_email = 'Relecloud Support <noreply@relecloud.com>'
        to = user_email
        try:
            send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        except Exception as e:
            print(f"Error al enviar el correo: {e}")
        return super().form_valid(form)

@login_required
def add_review(request, cruise_id):
    # ... (Tu vista add_review se mantiene igual) ...
    cruise = get_object_or_404(models.Cruise, id=cruise_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.cruise = cruise
            review.user = request.user
            review.save()
            return redirect('cruise_detail', pk=cruise.id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'cruise': cruise})