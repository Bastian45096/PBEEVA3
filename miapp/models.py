import re
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Sala(models.Model):
    NombreS = models.CharField(max_length=50)
    CapacidadM = models.IntegerField()
    Disponibilidad = models.BooleanField(default=True)

    def __str__(self):
        return self.NombreS

    def puede_reservar(self):
        reservas_activas = Reserva.objects.filter(
            Sala=self, 
            FechaHI__lte=timezone.now(), 
            FechaHT__gte=timezone.now()
        )
        return not reservas_activas.exists()
    
    def actualizar_disponibilidad(self):
        
        reservas_activas = Reserva.objects.filter(
            Sala=self,
            FechaHI__lte=timezone.now(),
            FechaHT__gte=timezone.now()
        )
        if reservas_activas.exists():
            self.Disponibilidad = False
        else:
            self.Disponibilidad = True
        self.save()



class Estudiante(models.Model):
    Rut = models.CharField(max_length=12, unique=True)
    NombreE = models.CharField(max_length=50)
    ApellidoE = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.NombreE} {self.ApellidoE} ({self.Rut})"

    def clean(self):
        rut_pattern = r'^\d{1,8}-[0-9Kk]$'
        if not re.match(rut_pattern, self.Rut):
            raise ValidationError("El RUT debe tener el formato '12345678-9'.")
        

class Reserva(models.Model):
    Estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    Sala = models.ForeignKey(Sala, on_delete=models.CASCADE)

    FechaHI = models.DateTimeField(default=timezone.now)
    FechaHT = models.DateTimeField()

    def save(self, *args, **kwargs):

        # --- Validación de duración (NO más de 2 horas) ---
        if self.FechaHI and self.FechaHT:
            duracion = self.FechaHT - self.FechaHI
            if duracion <= timedelta(0):
                raise ValueError("La hora de término debe ser posterior a la de inicio.")
            if duracion > timedelta(hours=2):
                raise ValueError("La reserva no puede durar más de 2 horas.")
        # ---------------------------------------------------

        # --- Validación de solapamiento ---
        reservas_solapadas = Reserva.objects.filter(
            Sala=self.Sala,
            FechaHI__lt=self.FechaHT,
            FechaHT__gt=self.FechaHI
        )

        if self.pk:
            reservas_solapadas = reservas_solapadas.exclude(pk=self.pk)

        if reservas_solapadas.exists():
            raise ValueError(f"La sala {self.Sala.NombreS} ya está reservada en este horario.")
        # ----------------------------------------

        # --- Validación de reserva duplicada por estudiante ---
        reservas_estudiante = Reserva.objects.filter(
            Estudiante=self.Estudiante,
            Sala=self.Sala
        )

        if self.pk:
            reservas_estudiante = reservas_estudiante.exclude(pk=self.pk)

        if reservas_estudiante.exists():
            raise ValueError("Este estudiante ya reservó esta sala previamente.")
        # -------------------------------------------------------

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva de {self.Estudiante} en {self.Sala}"
