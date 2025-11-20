from django.db import models
from django.utils import timezone

class Sala(models.Model):
    NombreS = models.CharField(max_length=50)
    CapacidadM = models.IntegerField()
    Disponibilidad = models.BooleanField(default=True)

    def __str__(self):
        return self.NombreS

    def actualizar_disponibilidad(self):
        reservas_activas = Reserva.objects.filter(
            Sala=self,
            FechaHI__lte=timezone.now(),
            FechaHT__gte=timezone.now()
        )
        self.Disponibilidad = not reservas_activas.exists()
        self.save()

class Estudiante(models.Model):
    Rut = models.CharField(max_length=12, unique=True)
    NombreE = models.CharField(max_length=50)
    ApellidoE = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.NombreE} {self.ApellidoE} ({self.Rut})"

class Reserva(models.Model):
    Estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    Sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    FechaHI = models.DateTimeField(auto_now_add=True)  # Fecha y hora de inicio automática
    FechaHT = models.DateTimeField()  # Fecha y hora de término

    def __str__(self):
        return f"Reserva de {self.Estudiante} en {self.Sala}"