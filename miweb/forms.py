from django import forms
from django.core.exceptions import ValidationError
import re
from datetime import timedelta

class Menu(forms.Form):
    RutE = forms.CharField(max_length=12, label="RUT del Estudiante")
    fechahi = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label="Fecha y Hora de Inicio")
    fechaht = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label="Fecha y Hora de Término")
    
    def clean_RutE(self):
        """Validar el formato del RUT."""
        rut = self.cleaned_data['RutE']
        rut_pattern = r'^\d{1,8}-[0-9Kk]$'  # Expresión regular para validar el formato
        if not re.match(rut_pattern, rut):
            raise ValidationError("El RUT debe tener el formato '12345678-9', con el guion antes del dígito verificador.")
        return rut

    def clean(self):
        """Validar las fechas de inicio y término."""
        cleaned_data = super().clean()
        fechahi = cleaned_data.get('fechahi')
        fechaht = cleaned_data.get('fechaht')

        # Verificar que la fecha de término no sea anterior a la de inicio
        if fechahi and fechaht:
            if fechaht <= fechahi:
                raise ValidationError("La fecha y hora de término debe ser posterior a la de inicio.")

            # Validar que la duración de la reserva no sea mayor a 2 horas
            if fechaht - fechahi > timedelta(hours=2):
                raise ValidationError("La duración de la reserva no puede ser mayor a 2 horas.")
        
        return cleaned_data
