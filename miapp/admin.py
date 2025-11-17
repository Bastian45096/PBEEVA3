from django.contrib import admin
from .models import Estudiante, Sala, Reserva
# Register your models here.


class SalaAdmin(admin.ModelAdmin):

    list_display = ['NombreS', 'CapacidadM', 'Disponibilidad']

class EstudianteAdmin(admin.ModelAdmin):

    list_display = ['Rut', 'NombreE', 'ApellidoE']

class ReservaAdmin(admin.ModelAdmin):

    list_display = ['Estudiante', 'Sala']



admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Sala, SalaAdmin)
admin.site.register(Reserva, ReservaAdmin)
