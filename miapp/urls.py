from django.contrib import admin
from django.urls import path, include
from .views import salasD, reservar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', salasD, name='salasD'),
    path("reserva/<int:id>/", reservar, name="reserva"),


]
