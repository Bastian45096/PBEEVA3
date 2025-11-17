from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Sala, Estudiante, Reserva
from miweb.forms import Menu


def salasD(request):
    salas = Sala.objects.all()

    # Actualiza disponibilidad automáticamente
    for s in salas:
        s.actualizar_disponibilidad()

    return render(request, 'salasD.html', {'sala': salas})


def reservar(request, id):
    sala = Sala.objects.get(id=id)
    sala.actualizar_disponibilidad()  # Actualiza antes de tomar decisiones

    # -------------------------------------------------
    # 1) VERIFICAR SI ESTA SALA YA ESTÁ RESERVADA
    # -------------------------------------------------
    reserva_activa = Reserva.objects.filter(
        Sala=sala,
        FechaHI__lte=timezone.now(),
        FechaHT__gte=timezone.now()
    ).first()

    if reserva_activa:
        # Mostrar solo detalles, sin formulario
        return render(request, 'reserva.html', {
            'sala': sala,
            'reserva': reserva_activa,
            'modo_detalle': True
        })

    # -------------------------------------------------
    # 2) PROCESO NORMAL DE RESERVA (sala disponible)
    # -------------------------------------------------
    if request.method == "POST":
        form = Menu(request.POST)

        if form.is_valid():

            # Reconfirmar antes de reservar
            if not sala.puede_reservar():
                form.add_error(None, "Esta sala ya está reservada ahora.")
                return render(request, 'reserva.html', {'sala': sala, 'form': form})

            rut = form.cleaned_data['RutE']
            fechahi = form.cleaned_data['fechahi']
            fechaht = form.cleaned_data['fechaht']

            estudiante, creado = Estudiante.objects.get_or_create(
                Rut=rut,
                defaults={'NombreE': '', 'ApellidoE': ''}
            )

            Reserva.objects.create(
                Estudiante=estudiante,
                Sala=sala,
                FechaHI=fechahi,
                FechaHT=fechaht
            )

            sala.actualizar_disponibilidad()  # Actualiza a False

            return redirect('salasD')

    else:
        form = Menu()

    return render(request, 'reserva.html', {'sala': sala, 'form': form})
