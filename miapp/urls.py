from django.contrib import admin
from django.urls import path
from .views import salasD, reservar, modoAdmin

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin de Django
    path('', salasD, name='salasD'),  # Página principal de salas
    path("reserva/<int:id>/", reservar, name="reserva"),  # Reserva de sala
    path("modoAdmin/", modoAdmin, name="modoAdmin"),  # Página de administrador
]