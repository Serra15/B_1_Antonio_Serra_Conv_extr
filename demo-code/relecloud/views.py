from django.shortcuts import render
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin

# Imports para el correo que vamos a usar
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


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

# --- ESTA ES LA VISTA CORREGIDA Y ÚNICA QUE NECESITAS ---
class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
    template_name = 'info_request_create.html' # Asegúrate que tu formulario usa esta plantilla
    model = models.InfoRequest
    fields = ['name', 'email', 'cruise', 'notes']
    success_url = reverse_lazy('index')
    success_message = 'Thank you, %(name)s! We will email you when we have more information about %(cruise)s!'

    def form_valid(self, form):
        # Este método se llama cuando el formulario es válido.
        # Aquí es donde añadimos nuestra lógica de correo electrónico.
        
        # Obtenemos los datos del formulario que acaba de ser validado
        user_name = form.cleaned_data['name']
        user_email = form.cleaned_data['email']

        subject = 'Confirmación de tu solicitud en Relecloud'
        html_message = render_to_string('email/confirmation_template.html', {'name': user_name})
        plain_message = strip_tags(html_message)
        from_email = 'Relecloud Support <noreply@relecloud.com>'
        to = user_email

        try:
            print("="*20, "INTENTANDO ENVIAR CORREO DESDE CreateView", "="*20)
            send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            print("="*20, "CORREO ENVIADO (A LA CONSOLA)", "="*20)
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

        # Finalmente, dejamos que la vista continúe con su comportamiento normal:
        # guarda el objeto, muestra el mensaje de éxito y redirige.
        return super().form_valid(form)
