from django import forms
from django.core.exceptions import ValidationError
from datetime import timedelta

class Menu(forms.Form):
    RutE = forms.CharField(max_length=12, label="RUT del Estudiante")
    duracion = forms.DurationField(label="Duración de la Reserva", help_text="Formato: HH:MM:SS (máximo 2 horas)")

    def clean_duracion(self):
        duracion = self.cleaned_data['duracion']
        if duracion < timedelta(minutes=1) or duracion > timedelta(hours=2):
            raise ValidationError("La duración debe ser entre 1 minuto y 2 horas.")
        return duracion