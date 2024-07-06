from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
# Gestion de usuarios
def index(request):
    usuarios = Usuario.objects.all()
    return render(request, 'listaUsuarios.html', {'usuarios': usuarios})

def guardarUsuario(request):
    return render(request, 'registrarDanios.html')

def registrarUsuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rol = request.POST.get('rol')
        is_active = 'is_active' in request.POST

        # Verificar si el username o el email ya existen
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe. Por favor, elige otro.')
            return redirect('guardarUsuario')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El email ya existe. Por favor, ingresa otro.')
            return redirect('guardarUsuario')

        usuario = Usuario.objects.create(
            username=username,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            email=email,
            rol=rol,
            is_active=is_active
        )
        usuario.set_password(password)
        usuario.save()
        
        messages.success(request, 'Usuario guardado correctamente')
        return redirect('index')
    else:
        return render(request, 'guardarUsuario.html')

def eliminarUsuario(request, id):
    try:
        usuario = Usuario.objects.get(id_usr=id)
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente')
    except Usuario.DoesNotExist:
        messages.error(request, 'El usuario no existe')
    
    return redirect('index')


# Gestion de Clientes

def listaClientes(request):
    clientes = Cliente.objects.all()
    return render(request,'listaClientes.html',{'clientes':clientes})
def guardarCliente(request):
    return render(request,'guardarCliente.html')

def registrarCliente(request):
    if request.method == 'POST':
        # Datos de la dirección
        ciudad = request.POST['ciudad_dir']
        barrio = request.POST['barrio_dir']
        calle = request.POST['calle_dir']
        numero = request.POST['numero_dir']

        # Crear la instancia de la dirección y guardarla
        direccion = Direccion(ciudad_dir=ciudad, barrio_dir=barrio, calle_dir=calle, numero_dir=numero)
        direccion.save()

        # Datos del cliente
        nombre = request.POST['nombre_cli']
        apellido = request.POST['apellido_cli']
        ci = request.POST['ci_cli']
        telefono = request.POST['telefono_cli']
        email = request.POST['email_cli']

        # Crear la instancia del cliente y guardarla
        cliente = Cliente(nombre_cli=nombre, apellido_cli=apellido, ci_cli=ci, telefono_cli=telefono, email_cli=email, dir_id=direccion)
        cliente.save()

        return redirect('listaClientes')  # Redirige a la lista de clientes después de registrar

    return render(request, 'registro_cliente.html')

def eliminarCliente(request,id):
    cliente = Cliente.objects.get(id_cli=id)
    cliente.delete()
    messages.success(request, 'Cliente eliminado correctamente')
    return redirect('listaClientes')

def obtenerClietne(request,id):
    cliente = Cliente.objects.get(id_cli=id)
    return render(request,'obtenerCliente.html',{'cliente':cliente})

def actualizarCliente(request):
    
    if request.method == 'POST':
        id_cli = request.POST["id_cli"]
        cliente = Cliente.objects.get(id_cli=id_cli)
        cliente.dir_id.ciudad_dir = request.POST['ciudad_dir']
        cliente.dir_id.barrio_dir = request.POST['barrio_dir']
        cliente.dir_id.calle_dir = request.POST['calle_dir']
        cliente.dir_id.numero_dir = request.POST['numero_dir']
        cliente.dir_id.save()
        
        cliente.nombre_cli = request.POST['nombre_cli']
        cliente.apellido_cli = request.POST['apellido_cli']
        cliente.ci_cli = request.POST['ci_cli']
        cliente.telefono_cli = request.POST['telefono_cli']
        cliente.email_cli = request.POST['email_cli']
        cliente.save()
        messages.success(request, 'Cliente actualizado correctamente')
        return redirect('listaClientes') 
    
# Gestion de servicios

def listaServicios(request):
    servicios = Servicio.objects.all()
    return render(request,'listaServicios.html',{'servicios':servicios})

def guardarServicio(request):
    return render(request,'guardarServicio.html')


def registrarServicio(request):
    if request.method == 'POST':
        nombre = request.POST['nombre_ser']
        descripcion = request.POST['descripcion_ser']
        precio = request.POST['precio_ser']
        servicio = Servicio(nombre_ser=nombre, descripcion_ser=descripcion, precio_ser=precio)
        servicio.save()
        messages.success(request, 'Servicio creado correctamente')
        return redirect('listaServicios')


def eliminarServicio(request,id):
    servicio = Servicio.objects.get(id_ser =id)
    servicio.delete()
    messages.success(request, 'Servicio eliminado correctamente')
    return redirect('listaServicios')

def obtenerServicio(request,id):
    servicio = Servicio.objects.get(id_ser = id)
    return render(request,'obtenerServicio.html',{'servicio':servicio})

def actualizarServicio(request):
    if request.method == 'POST':
        servicio_id = request.POST['id_ser']
        servicio = Servicio.objects.get(id_ser=servicio_id)
        servicio.nombre_ser = request.POST['nombre_ser']
        servicio.descripcion_ser = request.POST['descripcion_ser']
        servicio.precio_ser = request.POST['precio_ser']
        servicio.save()
        messages.success(request, 'Servicio actualizado correctamente')
        return redirect('listaServicios')  # Redirige a la lista de servicios después de actualizar

# Gestion de  Ordenes de trabajo
def listaVehiculos(request):
    vehiculos =Vehiculo.objects.all()
    
    return render(request,'listaVehiculos.html',{'vehiculos':vehiculos})

def guardarVehiculo(request):
    clientes = Cliente.objects.all()
    return render(request,'guardarVehiculo.html',{'clientes':clientes})

def registrarVehiculo(request):
    if request.method == 'POST':
        marca = request.POST['marca_veh']
        modelo = request.POST['modelo_veh']
        placa = request.POST['placa_veh']
        anio = request.POST['anio_veh']
        chasis = request.POST['chasis_veh']
        color = request.POST['color_veh']
        cliente_id = request.POST['id_cli']
        cliente = Cliente.objects.get(id_cli=cliente_id)

        vehiculo = Vehiculo(
            marca_veh=marca,
            modelo_veh=modelo,
            placa_veh=placa,
            anio_veh=anio,
            chasis_veh=chasis,
            color_veh=color,
            cli_id=cliente
        )
        vehiculo.save()
        messages.success(request, 'Vehículo creado correctamente')
        return redirect('listaVehiculos')

def eliminarVehiculo(request,id):
    vehiculo = Vehiculo.objects.get(id_veh=id)
    vehiculo.delete()
    messages.success(request, 'Vehículo eliminado correctamente')
    return redirect("listaVehiculos")

def obtenerVehiculo(request,id):
    vehiculo = Vehiculo.objects.get(id_veh=id)
    clientes = Cliente.objects.all()
    return render(request,'obtenerVehiculo.html',{'vehiculo':vehiculo,'clientes':clientes})

def actualizarVehiculo(request):
    if request.method == 'POST':
        id_veh=request.POST['id_veh']
        vehiculo = Vehiculo.objects.get(id_veh=id_veh)
        vehiculo.marca_veh = request.POST['marca_veh']
        vehiculo.modelo_veh = request.POST['modelo_veh']
        vehiculo.placa_veh = request.POST['placa_veh']
        vehiculo.anio_veh = request.POST['anio_veh']
        vehiculo.chasis_veh = request.POST['chasis_veh']
        vehiculo.color_veh = request.POST['color_veh']
        cliente_id = request.POST['cli_id']
        vehiculo.cli_id = Cliente.objects.get(id_cli=cliente_id)
        vehiculo.save()
        messages.success(request, 'Vehículo actualizado correctamente')
        return redirect('listaVehiculos')