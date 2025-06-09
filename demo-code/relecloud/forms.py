from django import forms
from .models import InfoRequest # Esta línea asume que tienes un modelo llamado InfoRequest

class InfoRequestForm(forms.ModelForm):
    """
    Formulario basado en el modelo InfoRequest.
    Django creará los campos del formulario automáticamente a partir del modelo.
    """
    class Meta:
        model = InfoRequest
        # Lista los campos de tu modelo que quieres que aparezcan en el formulario.
        # Asegúrate de que estos nombres coincidan con los de tu models.py
        fields = ['name', 'email', 'notes', 'cruise']