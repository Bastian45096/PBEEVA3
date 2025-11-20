from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Sala, Estudiante, Reserva
from miweb.forms import Menu

# Vista para la página principal de salas
def salasD(request):
    salas = Sala.objects.all()
    for s in salas:
        s.actualizar_disponibilidad()
    return render(request, 'salasD.html', {'salas': salas})

# Vista para la página de administrador
def modoAdmin(request):
    if request.method == "POST":
        action = request.POST.get("action")

        # Crear Sala
        if action == "crear_sala":
            nombre_sala = request.POST.get("nombre_sala")
            capacidad = request.POST.get("capacidad")
            Sala.objects.create(NombreS=nombre_sala, CapacidadM=capacidad)
            return redirect("modoAdmin")
        
        # Editar Sala
        elif action == "editar_sala":
            sala_id = request.POST.get("sala_id")
            nombre_sala_edit = request.POST.get("nombre_sala_edit")
            capacidad_edit = request.POST.get("capacidad_edit")
            sala = Sala.objects.get(id=sala_id)
            sala.NombreS = nombre_sala_edit
            sala.CapacidadM = capacidad_edit
            sala.save()
            return redirect("modoAdmin")

        # Eliminar Sala
        elif action == "eliminar_sala":
            sala_id = request.POST.get("sala_id")
            Sala.objects.filter(id=sala_id).delete()
            return redirect("modoAdmin")

        # Crear Estudiante
        elif action == "crear_estudiante":
            rut = request.POST.get("rut")
            nombre = request.POST.get("nombre")
            apellido = request.POST.get("apellido")
            Estudiante.objects.create(Rut=rut, NombreE=nombre, ApellidoE=apellido)
            return redirect("modoAdmin")

        # Editar Estudiante
        elif action == "editar_estudiante":
            estudiante_id = request.POST.get("estudiante_id")
            rut_edit = request.POST.get("rut_edit")
            nombre_edit = request.POST.get("nombre_edit")
            apellido_edit = request.POST.get("apellido_edit")
            estudiante = Estudiante.objects.get(id=estudiante_id)
            estudiante.Rut = rut_edit
            estudiante.NombreE = nombre_edit
            estudiante.ApellidoE = apellido_edit
            estudiante.save()
            return redirect("modoAdmin")

        # Eliminar Estudiante
        elif action == "eliminar_estudiante":
            estudiante_id = request.POST.get("estudiante_id")
            Estudiante.objects.filter(id=estudiante_id).delete()
            return redirect("modoAdmin")

        # Crear Reserva
        elif action == "crear_reserva":
            estudiante_id = request.POST.get("estudiante")
            sala_id = request.POST.get("sala")
            fecha_hi = request.POST.get("fecha_hi")
            fecha_ht = request.POST.get("fecha_ht")
            estudiante = Estudiante.objects.get(id=estudiante_id)
            sala = Sala.objects.get(id=sala_id)
            Reserva.objects.create(Estudiante=estudiante, Sala=sala, FechaHI=fecha_hi, FechaHT=fecha_ht)
            return redirect("modoAdmin")

        # Editar Reserva
        elif action == "editar_reserva":
            reserva_id = request.POST.get("reserva_id")
            estudiante_edit = request.POST.get("estudiante_edit")
            sala_edit = request.POST.get("sala_edit")
            fecha_hi_edit = request.POST.get("fecha_hi_edit")
            fecha_ht_edit = request.POST.get("fecha_ht_edit")
            reserva = Reserva.objects.get(id=reserva_id)
            reserva.Estudiante = Estudiante.objects.get(id=estudiante_edit)
            reserva.Sala = Sala.objects.get(id=sala_edit)
            reserva.FechaHI = fecha_hi_edit
            reserva.FechaHT = fecha_ht_edit
            reserva.save()
            return redirect("modoAdmin")

        # Eliminar Reserva
        elif action == "eliminar_reserva":
            reserva_id = request.POST.get("reserva_id")
            Reserva.objects.filter(id=reserva_id).delete()
            return redirect("modoAdmin")

    # Datos para mostrar en la página
    salas = Sala.objects.all()
    estudiantes = Estudiante.objects.all()
    reservas = Reserva.objects.all()

    return render(request, "modoAdmin.html", {
        "salas": salas,
        "estudiantes": estudiantes,
        "reservas": reservas,
    })

# Vista para la reserva de una sala específica
def reservar(request, id):
    sala = Sala.objects.get(id=id)
    sala.actualizar_disponibilidad()

    if request.method == "POST":
        form = Menu(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['RutE']
            duracion = form.cleaned_data['duracion']

            estudiante, creado = Estudiante.objects.get_or_create(
                Rut=rut,
                defaults={'NombreE': '', 'ApellidoE': ''}
            )

            fecha_hi = timezone.now()  # Fecha y hora actual
            fecha_ht = fecha_hi + duracion  # Fecha y hora de término basado en la duración

            Reserva.objects.create(
                Estudiante=estudiante,
                Sala=sala,
                FechaHI=fecha_hi,
                FechaHT=fecha_ht
            )

            sala.actualizar_disponibilidad()
            return redirect('salasD')
    else:
        form = Menu()

    return render(request, 'reserva.html', {'sala': sala, 'form': form})