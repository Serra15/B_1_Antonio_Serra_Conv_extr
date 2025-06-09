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

# 👇 AÑADE ESTAS NUEVAS IMPORTACIONES PARA LA VISTA DE OPINIONES 👇
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm # Asumimos que has creado ReviewForm en forms.py


# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def destinations(request):
    all_destinations = models.Destination.objects.all()
    return render(request, 'destinations.html', { 'destinations': all_destinations})

class DestinationDetailView(generic.DetailView):
    template_name = 'destination_detail.html'
    model = models.Destination
    context_object_name = 'destination'

class CruiseDetailView(generic.DetailView):
    template_name = 'cruise_detail.html'
    model = models.Cruise
    context_object_name = 'cruise'

class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
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


# 👇 AÑADE ESTA NUEVA VISTA AL FINAL DE TU ARCHIVO 👇
@login_required
def add_review(request, cruise_id):
    # Usamos get_object_or_404 para obtener el crucero. Si no existe, dará un error 404.
    cruise = get_object_or_404(models.Cruise, id=cruise_id)
    
    if request.method == 'POST':
        # Si el formulario se envía, procesamos los datos
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Creamos el objeto Review pero sin guardarlo aún en la base de datos
            review = form.save(commit=False)
            
            # Asignamos el crucero y el usuario (que está en request.user) a la opinión
            review.cruise = cruise
            review.user = request.user
            
            # Ahora guardamos la opinión completa en la base de datos
            review.save()
            
            # Redirigimos al usuario de vuelta a la página de detalle del crucero
            return redirect('cruise_detail', pk=cruise.id)
    else:
        # Si es una petición GET, simplemente mostramos un formulario vacío
        form = ReviewForm()
        
    # Renderizamos la plantilla para el formulario
    return render(request, 'add_review.html', {'form': form, 'cruise': cruise})