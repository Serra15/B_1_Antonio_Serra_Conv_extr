from django import forms
from .models import InfoRequest, Review # Esta línea asume que tienes un modelo llamado InfoRequest

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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        # Solo mostramos estos dos campos al usuario.
        # El usuario y el crucero se asignarán automáticamente en la vista.
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }