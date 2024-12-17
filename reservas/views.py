from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import (
    Nacionalidad, Pasajero, Pago, Servicios, DetallePago, 
    TipoHabitacion, Habitacion, TipoUsuario, Usuario, Reserva
)

from django.contrib import messages

from .forms import NacionalidadForm, TipoUsuarioForm, UsuarioForm, HabitacionForm, PasajeroForm, PagoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

class ListarReservasView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'reservas/listar_reservas.html'
    context_object_name = 'reservas'

def pagina_principal(request):
    return render(request, 'reservas/pagina_principal.html')

# Vistas para Nacionalidad
@login_required
def listar_nacionalidades(request):
    nacionalidades = Nacionalidad.objects.all()
    return render(request, 'reservas/listar_nacionalidades.html', {'nacionalidades': nacionalidades})

def crear_nacionalidad(request):
    if request.method == 'POST':
        form = NacionalidadForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda la nacionalidad en la base de datos
            return redirect('listar_nacionalidades')  # Redirige a la lista de nacionalidades
    else:
        form = NacionalidadForm()  # Crea un formulario vacío

    return render(request, 'reservas/crear_nacionalidad.html', {'form': form})  # Asegúrate de que el nombre de la plantilla sea correcto

# Vistas para Pasajero
@login_required
def listar_pasajeros(request):
    # Obtener el parámetro de búsqueda 'rut'
    rut_buscar = request.GET.get('rut', '')

    if rut_buscar:
        # Filtrar pasajeros por RUT si se proporciona el parámetro de búsqueda
        pasajeros = Pasajero.objects.filter(rut__icontains=rut_buscar)
    else:
        # Mostrar todos los pasajeros si no se proporciona el parámetro
        pasajeros = Pasajero.objects.all()

    return render(request, 'reservas/listar_pasajeros.html', {'pasajeros': pasajeros})

def crear_pasajero(request):
    nacionalidades = Nacionalidad.objects.all()
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido_paterno = request.POST['apellido_paterno']
        apellido_materno = request.POST['apellido_materno']
        correo = request.POST['correo']
        rut = request.POST['rut']
        codigo_naci = request.POST['codigo_naci']
        
        # Aquí puedes agregar validaciones adicionales si es necesario
        
        pasajero = Pasajero(
            nombre=nombre, apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno, correo=correo,
            rut=rut, codigo_naci_id=codigo_naci
        )
        pasajero.save()
        messages.success(request, 'Pasajero creado exitosamente.')  # Mensaje de éxito
        return redirect('listar_pasajeros')
    
    return render(request, 'reservas/crear_pasajero.html', {'nacionalidades': nacionalidades})

def editar_pasajero(request, id_pasajero):
    pasajero = get_object_or_404(Pasajero, id_pasajero=id_pasajero)  # Cambia 'id' por 'id_pasajero'
    
    if request.method == 'POST':
        form = PasajeroForm(request.POST, instance=pasajero)
        if form.is_valid():
            form.save()
            return redirect('listar_pasajeros')  # Redirige a la lista de pasajeros
    else:
        form = PasajeroForm(instance=pasajero)
    
    return render(request, 'reservas/editar_pasajero.html', {'form': form})

def eliminar_pasajero(request, id_pasajero):
    pasajero = get_object_or_404(Pasajero, id_pasajero=id_pasajero)  # Cambia 'id' por 'id_pasajero'
    
    if request.method == 'POST':
        pasajero.delete()  # Elimina el pasajero
        return redirect('listar_pasajeros')  # Redirige a la lista de pasajeros
    
    return render(request, 'reservas/eliminar_pasajero.html', {'pasajero': pasajero})


# Vistas para Habitacion
def listar_habitaciones(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'reservas/listar_habitaciones.html', {'habitaciones': habitaciones})

def crear_habitacion(request):
    tipos_habitacion = TipoHabitacion.objects.all()
    if request.method == 'POST':
        tipo_habitacion = request.POST['tipo_habitacion']
        estado_habitacion = request.POST['estado_habitacion']
        habitacion = Habitacion(
            tipo_habitacion_id=tipo_habitacion,
            estado_habitacion=estado_habitacion
        )
        habitacion.save()
        return redirect('listar_habitaciones')
    return render(request, 'reservas/crear_habitacion.html', {'tipos_habitacion': tipos_habitacion})

# Vistas para Pago
def listar_pagos(request):
    pagos = Pago.objects.all()  # Obtén todos los pagos
    return render(request, 'reservas/listar_pagos.html', {'pagos': pagos})


def crear_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()  # No necesitas especificar id_pago
            return redirect('listar_pagos')
    else:
        form = PagoForm()

    return render(request, 'reservas/crear_pago.html', {'form': form})

# Vistas para Reserva
@login_required
def listar_reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'reservas/listar_reservas.html', {'reservas': reservas})

def crear_reserva(request):
    pasajeros = Pasajero.objects.all()
    usuarios = Usuario.objects.all()
    habitaciones = Habitacion.objects.filter(estado_habitacion='Disponible')
    
    if request.method == 'POST':
        pasajero_id = request.POST['pasajero']
        usuario_id = request.POST['usuario']
        habitacion_id = request.POST['habitacion']
        fecha_reserva = request.POST['fecha_reserva']  # Este es el valor de la fecha ingresada por el usuario
        cantidad_dias = request.POST['cantidad_dias']
        estado_reserva = 'Reservado'  # Puedes establecer un valor predeterminado o capturarlo del formulario
        cantidad_persona = request.POST['cantidad_persona']
        nombre_empresa = request.POST.get('nombre_empresa', '')

        # Crear la reserva
        reserva = Reserva(
            pasajero_id=pasajero_id,
            usuario_id=usuario_id,
            habitacion_id=habitacion_id,
            fecha_reserva=fecha_reserva,  # Aquí se guarda la fecha ingresada
            cantidad_dias=cantidad_dias,
            estado_reserva=estado_reserva,
            cantidad_persona=cantidad_persona,
            nombre_empresa=nombre_empresa
        )
        reserva.save()
        return redirect('listar_reservas')
    
    return render(request, 'reservas/crear_reserva.html', {
        'pasajeros': pasajeros,
        'usuarios': usuarios,
        'habitaciones': habitaciones
    })

# Vistas para Usuario
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'reservas/listar_usuarios.html', {'usuarios': usuarios})

def crear_usuario(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario')  # Cambia esto
        password = request.POST.get('password')  # Si necesitas recoger la contraseña
        tipo_usuario_id = request.POST.get('tipo_usuario')

        # Crea el nuevo usuario
        usuario = Usuario(nombre_usuario=nombre_usuario, password=password, tipo_usuario_id=tipo_usuario_id)
        usuario.save()

        return redirect('listar_usuarios')  # Cambia esto a la URL a la que quieras redirigir

    tipos_usuario = TipoUsuario.objects.all()
    return render(request, 'reservas/crear_usuario.html', {'tipos_usuario': tipos_usuario})

def editar_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')  # Redirige a la lista después de editar
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'reservas/editar_usuario.html', {'form': form})

def eliminar_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)

    if request.method == 'POST':
        usuario.delete()  # Elimina el usuario de la base de datos
        return redirect('listar_usuarios')  # Redirige a la lista de usuarios después de eliminar

    return render(request, 'reservas/eliminar_usuario.html', {'usuario': usuario})


def crear_tipo_usuario(request):
    if request.method == 'POST':
        form = TipoUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_tipos_usuario')  # Cambia esto al nombre de la URL donde redirigir después de guardar
    else:
        form = TipoUsuarioForm()
    
    return render(request, 'crear_tipo_usuario.html', {'form': form})


def editar_habitacion(request, id_habitacion):
    habitacion = get_object_or_404(Habitacion, n_habitacion=id_habitacion)
    if request.method == 'POST':
        form = HabitacionForm(request.POST, instance=habitacion)
        if form.is_valid():
            form.save()
            return redirect('listar_habitaciones')  # Redirige a la lista de habitaciones
    else:
        form = HabitacionForm(instance=habitacion)
    return render(request, 'reservas/editar_habitacion.html', {'form': form})

def eliminar_habitacion(request, id_habitacion):
    habitacion = get_object_or_404(Habitacion, n_habitacion=id_habitacion)
    if request.method == 'POST':
        habitacion.delete()
        return redirect('listar_habitaciones')  # Redirige a la lista de habitaciones
    return render(request, 'reservas/eliminar_habitacion.html', {'habitacion': habitacion})


    pagos = Pago.objects.all()
    return render(request, 'pagos/listar_pagos.html', {'pagos': pagos})