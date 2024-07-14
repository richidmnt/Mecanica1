from gettext import translation
import json
from django.db import transaction, IntegrityError
from django.forms import ValidationError
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist
from .models import *

# Gestion de usuarios
def index(request):
    usuarios = Usuario.objects.all()
    return render(request, 'listaUsuarios.html', {'usuarios': usuarios})

def guardarUsuario(request):
    return render(request, 'guardarUsuario.html')

def registrarUsuario(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        nombre = request.POST.get('nombre').upper()
        apellido = request.POST.get('apellido').upper()
        telefono = request.POST.get('telefono')
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        rol = request.POST.get('rol')
        is_active = 'is_active' in request.POST

        try:
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

        except IntegrityError as e:
            if 'username' in str(e):
                messages.error(request, 'El nombre de usuario ya existe. Por favor, elige otro.')
            elif 'email' in str(e):
                messages.error(request, 'El email ya existe. Por favor, ingresa otro.')
            else:
                messages.error(request, 'Ocurrió un error al guardar el usuario. Por favor, inténtalo de nuevo.')
            return redirect('guardarUsuario')
    else:
        return render(request, 'guardarUsuario.html')

def eliminarUsuario(request, id):
    try:
        usuario = Usuario.objects.get(id_usr=id)
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente')
    except Usuario.DoesNotExist:
        messages.error(request, 'El usuario no existe')
    except ProtectedError as e:
        messages.error(request, 'No se puede eliminar el usuario porque está asociado con una o más órdenes.')
    except IntegrityError as e:
        messages.error(request, 'No se puede eliminar el usuario debido a una restricción de integridad.')
    except Exception as e:
        messages.error(request, f'Ocurrió un error al eliminar el usuario: {str(e)}')
    
    return redirect('index')


# Gestion de Clientes

def listaClientes(request):
    clientes = Cliente.objects.all()
    return render(request,'listaClientes.html',{'clientes':clientes})

def guardarCliente(request):
    return render(request,'guardarCliente.html')

def registrarCliente(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                ciudad = request.POST['ciudad_dir'].strip().upper()
                barrio = request.POST['barrio_dir'].strip().upper()
                calle = request.POST['calle_dir'].strip().upper()
                numero = request.POST['numero_dir']

                # Crear la instancia de la dirección pero no guardarla aún
                direccion = Direccion(ciudad_dir=ciudad, barrio_dir=barrio, calle_dir=calle, numero_dir=numero)

                nombre = request.POST['nombre_cli'].strip().upper()
                apellido = request.POST['apellido_cli'].strip().upper()
                ci = request.POST['ci_cli'].strip()
                telefono = request.POST['telefono_cli'].strip()
                email = request.POST['email_cli'].strip()

                # Verificar si el CI del cliente ya existe
                if Cliente.objects.filter(ci_cli=ci).exists():
                    messages.error(request, 'El cliente con este CI ya existe.')
                    raise IntegrityError('CI del cliente duplicado')

                # Verificar si el email del cliente ya existe
                if Cliente.objects.filter(email_cli=email).exists():
                    messages.error(request, 'El cliente con este email ya existe.')
                    raise IntegrityError('Email del cliente duplicado')

                # Guardar la dirección y luego el cliente
                direccion.save()
                cliente = Cliente(nombre_cli=nombre, apellido_cli=apellido, ci_cli=ci, telefono_cli=telefono, email_cli=email, dir_id=direccion)
                cliente.save()

            messages.success(request, 'Cliente registrado correctamente.')
            return redirect('listaClientes') 

        except IntegrityError as e:
            error_message = str(e)
            if 'ci_cli' in error_message:
                messages.error(request, 'El CI del cliente ya existe. Por favor, ingresa otro.')
            elif 'email_cli' in error_message:
                messages.error(request, 'El email del cliente ya existe. Por favor, ingresa otro.')
            else:
                messages.error(request, f'Error de integridad: {error_message}')
        except Exception as e:
            messages.error(request, f'Error al registrar el cliente: {e}')

        return redirect('guardarCliente')



def eliminarCliente(request, id):
    try:
        cliente = get_object_or_404(Cliente, id_cli=id)
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente')
    except Cliente.DoesNotExist:
        messages.error(request, 'El cliente no existe')
    except ProtectedError as e:
        messages.error(request, f'No se puede eliminar el cliente porque está relacionado con uno  más vehiculos')
    except Exception as e:
        messages.error(request, f'Ocurrió un error al intentar eliminar el cliente: {e}')
    
    return redirect('listaClientes')

def obtenerClietne(request,id):
    cliente = Cliente.objects.get(id_cli=id)
    return render(request,'obtenerCliente.html',{'cliente':cliente})

def actualizarCliente(request):
    
    if request.method == 'POST':
        id_cli = request.POST["id_cli"]
        cliente = Cliente.objects.get(id_cli=id_cli)
        cliente.dir_id.ciudad_dir = request.POST['ciudad_dir'].strip().upper()
        cliente.dir_id.barrio_dir = request.POST['barrio_dir'].strip().upper()
        cliente.dir_id.calle_dir = request.POST['calle_dir'].strip().upper()
        cliente.dir_id.numero_dir = request.POST['numero_dir']
        cliente.dir_id.save()
        
        cliente.nombre_cli = request.POST['nombre_cli'].strip().upper()
        cliente.apellido_cli = request.POST['apellido_cli'].strip().upper()
        cliente.ci_cli = request.POST['ci_cli'].strip()
        cliente.telefono_cli = request.POST['telefono_cli'].strip()
        cliente.email_cli = request.POST['email_cli'].strip()
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
        nombre = request.POST['nombre_ser'].strip().upper()
        descripcion = request.POST['descripcion_ser'].upper()
        precio = request.POST['precio_ser']

        try:
            if Servicio.objects.filter(nombre_ser=nombre).exists():
                messages.error(request, 'El nombre del servicio ya existe. Por favor, elige otro nombre.')
                return redirect('guardarServicio')

            servicio = Servicio(
                nombre_ser=nombre,
                descripcion_ser=descripcion,
                precio_ser=precio
            )
            servicio.save()
            messages.success(request, 'Servicio creado correctamente')
            return redirect('listaServicios')
        except IntegrityError:
            messages.error(request, 'El nombre del servicio ya existe. Por favor, elige otro nombre.')
            return redirect('guardarServicio')
    else:
        return render(request, 'guardarServicio.html')


def eliminarServicio(request, id):
    servicio = get_object_or_404(Servicio, id_ser=id)
    try:
        servicio.delete()
        messages.success(request, 'Servicio eliminado correctamente')
    except ProtectedError:
        messages.error(request, 'No se puede eliminar el servicio porque está referenciado en órdenes existentes.')
    return redirect('listaServicios')

def obtenerServicio(request,id):
    servicio = Servicio.objects.get(id_ser = id)
    return render(request,'obtenerServicio.html',{'servicio':servicio})

def actualizarServicio(request):
    if request.method == 'POST':
        try:
            servicio_id = request.POST['id_ser']
            servicio = Servicio.objects.get(id_ser=servicio_id)
            servicio.nombre_ser = request.POST['nombre_ser'].strip().upper()
            servicio.descripcion_ser = request.POST['descripcion_ser'].upper()
            servicio.precio_ser = request.POST['precio_ser']
            servicio.save()
            messages.success(request, 'Servicio actualizado correctamente')
        except IntegrityError:
            messages.error(request, 'El nombre del servicio ya existe. Por favor, elige otro nombre.')
        except Servicio.DoesNotExist:
            messages.error(request, 'El servicio no existe.')
        except ValueError:
            messages.error(request, 'El precio debe ser un número decimal válido.')
        except Exception as e:
            messages.error(request, f'Error inesperado: {str(e)}')
        
        return redirect('listaServicios')
    else:
        return render(request, 'obtenerServicio') 

# Gestion de  Ordenes de trabajo
def listaVehiculos(request):
    vehiculos =Vehiculo.objects.all()
    
    return render(request,'listaVehiculos.html',{'vehiculos':vehiculos})

def guardarVehiculo(request):
    clientes = Cliente.objects.all()
    return render(request,'guardarVehiculo.html',{'clientes':clientes})

def registrarVehiculo(request):
    if request.method == 'POST':
        try:
            marca = request.POST['marca_veh'].strip().upper()
            modelo = request.POST['modelo_veh'].strip().upper()
            placa = request.POST['placa_veh'].strip().upper()
            anio = request.POST['anio_veh']
            chasis = request.POST['chasis_veh']
            color = request.POST['color_veh'].strip().upper()
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
        except Cliente.DoesNotExist:
            messages.error(request, 'El cliente no existe. Por favor, seleccione un cliente válido.')
        except IntegrityError:
            messages.error(request, 'La placa o el chasis ya están registrados. Por favor, ingrese datos únicos.')
        except Exception as e:
            messages.error(request, f'Error inesperado: {e}')
        return redirect('guardarVehiculo')

        

def eliminarVehiculo(request, id):
    vehiculo = get_object_or_404(Vehiculo, id_veh=id)
    try:
        vehiculo.delete()
        messages.success(request, 'Vehículo eliminado correctamente')
    except ProtectedError as e:
        messages.error(request, f'No se puede eliminar el vehículo porque está asociado a una o más órdenes')
    return redirect('listaVehiculos')

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
    
#Registrar Orden Cliente
 
def guardarOrden(request):
    max_numero_ord = Orden.objects.aggregate(models.Max('numero_ord'))['numero_ord__max']
    next_numero_ord = 1 if max_numero_ord is None else max_numero_ord + 1
    context = {
            'next_numero_ord': next_numero_ord,
            'usuarios': Usuario.objects.all(),
            'servicios': Servicio.objects.all(),
            'ESTADOS': Orden.ESTADOS,
        }
    return render(request,'generarorden.html',context)
"""
def registrarOrden(request):
    if request.method == 'POST':
        # Crear dirección
        direccion = Direccion.objects.create(
            ciudad_dir=request.POST['ciudad_dir'],
            barrio_dir=request.POST['barrio_dir'],
            calle_dir=request.POST['calle_dir'],
            numero_dir=request.POST['numero_dir']
        )
        
        # Crear cliente
        cliente = Cliente.objects.create(
            nombre_cli=request.POST['nombre_cli'],
            apellido_cli=request.POST['apellido_cli'],
            ci_cli=request.POST['ci_cli'],
            telefono_cli=request.POST['telefono_cli'],
            email_cli=request.POST['email_cli'],
            dir_id=direccion
        )
        
        # Crear vehículo
        vehiculo = Vehiculo.objects.create(
            marca_veh=request.POST['marca_veh'],
            modelo_veh=request.POST['modelo_veh'],
            placa_veh=request.POST['placa_veh'],
            anio_veh=request.POST['anio_veh'],
            chasis_veh=request.POST['chasis_veh'],
            color_veh=request.POST['color_veh'],
            cli_id=cliente
        )
        
        # Crear inspección
        inspeccion = Inspeccion.objects.create(
            km=request.POST['km'],
            nivel_gasolina=request.POST['nivel_gasolina'],
            plumas='plumas' in request.POST,
            antena='antena' in request.POST,
            radio='radio' in request.POST,
            encendedor='encendedor' in request.POST,
            espejos='espejos' in request.POST,
            gata='gata' in request.POST,
            llave_de_ruedas='llave_de_ruedas' in request.POST,
            llanta_emergencia='llanta_emergencia' in request.POST,
            parlantes='parlantes' in request.POST,
            direccionales='direccionales' in request.POST,
            manubrios='manubrios' in request.POST,
            parabrisas='parabrisas' in request.POST,
            t_seguridad='t_seguridad' in request.POST,
            tapa_radiador='tapa_radiador' in request.POST,
            mandos_funcionales='mandos_funcionales' in request.POST,
            cenicero='cenicero' in request.POST,
            palanca='palanca' in request.POST,
            herramientas='herramientas' in request.POST,
            botiquin='botiquin' in request.POST,
            tapa_gasolina='tapa_gasolina' in request.POST,
            lunas='lunas' in request.POST,
            faros='faros' in request.POST,
            extintor='extintor' in request.POST,
            tapa_cubas='tapa_cubas' in request.POST,
            triangulos='triangulos' in request.POST,
            emblemas='emblemas' in request.POST,
            placas='placas' in request.POST,
            moquetas='moquetas' in request.POST
        )
         
         # Generar el próximo número de orden
        ultimo_numero_ord = Orden.objects.all().order_by('numero_ord').last()
        if ultimo_numero_ord:
            next_numero_ord = ultimo_numero_ord.numero_ord + 1
        else:
            next_numero_ord = 1

        # Crear la orden
        orden = Orden.objects.create(
            fecha_ord=timezone.now(),
            numero_ord=next_numero_ord,
            observaciones_ord=request.POST['observaciones_ord'],
            estado_ord=request.POST['estado_ord'],
            usuario_id=Usuario.objects.get(id_usr=request.POST['usuario_id']),
            vehiculo_id=vehiculo,
            inspeccion_id=inspeccion
        )
        # Crear servicios de la orden
        servicios_ids = request.POST.getlist('servicio_id[]')
        subtotales = request.POST.getlist('subtotal[]')
        for servicio_id, subtotal in zip(servicios_ids, subtotales):
            OrdenServicio.objects.create(
                orden_id=orden,
                servicio_id=Servicio.objects.get(id_ser=servicio_id),
                subtotal=subtotal
            )
        messages.success(request, 'orden creado correctamente')
        return redirect('/') 
"""
def registrarOrden(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                
                direccion = Direccion.objects.create(
                    ciudad_dir=request.POST['ciudad_dir'].strip().upper(),
                    barrio_dir=request.POST['barrio_dir'].strip().upper(),
                    calle_dir=request.POST['calle_dir'].strip().upper(),
                    numero_dir=request.POST['numero_dir']
                )

                
                if Cliente.objects.filter(ci_cli=request.POST['ci_cli']).exists():
                    raise IntegrityError('ci_cli')

                
                if Cliente.objects.filter(email_cli=request.POST['email_cli']).exists():
                    raise IntegrityError('email_cli')

        
                cliente = Cliente.objects.create(
                    nombre_cli=request.POST['nombre_cli'].strip().upper(),
                    apellido_cli=request.POST['apellido_cli'].strip().upper(),
                    ci_cli=request.POST['ci_cli'].strip(),
                    telefono_cli=request.POST['telefono_cli'].strip(),
                    email_cli=request.POST['email_cli'],
                    dir_id=direccion
                )

                
                if Vehiculo.objects.filter(placa_veh=request.POST['placa_veh']).exists():
                    raise IntegrityError('placa_veh')

            
                if Vehiculo.objects.filter(chasis_veh=request.POST['chasis_veh']).exists():
                    raise IntegrityError('chasis_veh')

                
                vehiculo = Vehiculo.objects.create(
                    marca_veh=request.POST['marca_veh'].strip().upper(),
                    modelo_veh=request.POST['modelo_veh'].strip().upper(),
                    placa_veh=request.POST['placa_veh'].strip().upper(),
                    anio_veh=request.POST['anio_veh'],
                    chasis_veh=request.POST['chasis_veh'],
                    color_veh=request.POST['color_veh'].strip().upper(),
                    cli_id=cliente
                )

                # Generar el próximo número de orden
                ultimo_numero_ord = Orden.objects.all().order_by('numero_ord').last()
                next_numero_ord = ultimo_numero_ord.numero_ord + 1 if ultimo_numero_ord else 1

                # Crear la orden
                orden = Orden.objects.create(
                    fecha_ord=timezone.now(),
                    numero_ord=next_numero_ord,
                    observaciones_ord=request.POST['observaciones_ord'],
                    estado_ord=request.POST['estado_ord'],
                    usuario_id=Usuario.objects.get(id_usr=request.POST['usuario_id']),
                    vehiculo_id=vehiculo,
                )

                # Crear servicios de la orden
                servicios_ids = request.POST.getlist('servicio_id[]')
                subtotales = request.POST.getlist('subtotal[]')

                for servicio_id, subtotal in zip(servicios_ids, subtotales):
                    if servicio_id and subtotal:
                        subtotal = subtotal.replace(',', '.')
                        OrdenServicio.objects.create(
                            orden_id=orden,
                            servicio_id=Servicio.objects.get(id_ser=servicio_id),
                            subtotal=subtotal
                        )

            messages.success(request, 'Orden creada correctamente')
            return redirect('listarOrdenes')

        except IntegrityError as e:
            if str(e) == 'ci_cli':
                messages.error(request, 'El CI del cliente ya existe. Por favor, ingresa otro.')
            elif str(e) == 'email_cli':
                messages.error(request, 'El email del cliente ya existe. Por favor, ingresa otro.')
            elif str(e) == 'placa_veh':
                messages.error(request, 'La placa del vehículo ya existe. Por favor, ingresa otra.')
            elif str(e) == 'chasis_veh':
                messages.error(request, 'El chasis del vehículo ya existe. Por favor, ingresa otro.')
            else:
                messages.error(request, f'Error de integridad: {e}')
        except ValidationError as e:
            messages.error(request, f'Error de validación: {e}')
        except ObjectDoesNotExist as e:
            messages.error(request, f'Error de objeto no encontrado: {e}')
        except Exception as e:
            messages.error(request, f'Error inesperado: {e}')
        
      
        return redirect('ordenCliente')

    

    

   

def guardarOrden2(request):
    max_numero_ord = Orden.objects.aggregate(models.Max('numero_ord'))['numero_ord__max']
    next_numero_ord = 1 if max_numero_ord is None else max_numero_ord + 1
    context = {
            'next_numero_ord': next_numero_ord,
            'usuarios': Usuario.objects.all(),
            'servicios': Servicio.objects.all(),
            'ESTADOS': Orden.ESTADOS,
            'vehiculos': Vehiculo.objects.all()
        }
    return render(request,'guardarOrden2.html',context)


def registrarOrden2(request):
    if request.method == 'POST':
        print("Datos POST recibidos:", request.POST)  # Añadir esta línea
        try:
            vehiculo_id = request.POST['vehiculo_id']
            vehiculo = Vehiculo.objects.get(id_veh = vehiculo_id)
            # Generar el próximo número de orden
            ultimo_numero_ord = Orden.objects.all().order_by('numero_ord').last()
            next_numero_ord = ultimo_numero_ord.numero_ord + 1 if ultimo_numero_ord else 1
            # Crear la orden
            orden = Orden.objects.create(
                fecha_ord=timezone.now(),
                numero_ord=next_numero_ord,
                observaciones_ord=request.POST['observaciones_ord'],
                estado_ord=request.POST['estado_ord'],
                usuario_id=Usuario.objects.get(id_usr=request.POST['usuario_id']),
                vehiculo_id=vehiculo,
            )
          
            servicios_ids = request.POST.getlist('servicio_id[]')
            subtotales = request.POST.getlist('subtotal[]')

            for servicio_id, subtotal in zip(servicios_ids, subtotales):
                if servicio_id and subtotal:
                    subtotal = subtotal.replace(',', '.')
                    OrdenServicio.objects.create(
                        orden_id=orden,
                        servicio_id=Servicio.objects.get(id_ser=servicio_id),
                        subtotal=subtotal
                    )

            messages.success(request, 'Orden creada correctamente')
            return redirect('listarOrdenes')

        except Exception as e:
            messages.error(request, f'Error al crear la orden: {e}')
            return redirect('listarOrdenes')




def listarOrdenesNoFinalizadas(request):
    ordenes_no_finalizadas = Orden.objects.exclude(estado_ord='FINALIZADA')
    context = {
        'ordenes': ordenes_no_finalizadas
    }
    return render(request, 'listarOrdenesF.html', context)

def obtenerOrden(request,id):
    orden = get_object_or_404(Orden, id_ord=id)
    servicios = Servicio.objects.all()
    usuarios = Usuario.objects.filter(is_active=True)
    orden_servicios = OrdenServicio.objects.filter(orden_id=orden)
    vehiculos=Vehiculo.objects.all()
    ESTADOS = Orden.ESTADOS
    context = {
        'orden': orden,
        'servicios': servicios,
        'usuarios': usuarios,
        'ESTADOS': ESTADOS,
        'orden_servicios': orden_servicios,
        'vehiculos':vehiculos
    }
    return render(request, 'obtenerOrden.html', context)

def editarOrden(request):
    if request.method == 'POST':
        vehiculo_id = request.POST['vehiculo_id']
        vehiculo = Vehiculo.objects.get(id_veh=vehiculo_id)
        id_ord =request.POST['id_ord']
        orden = Orden.objects.get(id_ord=id_ord)
        orden.vehiculo_id_id = vehiculo
        orden.fecha_ord = request.POST['fecha_ord']
        orden.numero_ord = request.POST['numero_ord']
        orden.observaciones_ord = request.POST['observaciones_ord']
        orden.estado_ord = request.POST['estado_ord']
        orden.usuario_id_id = request.POST['usuario_id']
        
        orden.save()

        # Eliminar los servicios antiguos y agregar los nuevos
        OrdenServicio.objects.filter(orden_id=orden).delete()
        servicio_ids = request.POST.getlist('servicio_id[]')
        subtotales = request.POST.getlist('subtotal[]')
        
        for servicio_id, subtotal in zip(servicio_ids, subtotales):
            subtotal = subtotal.replace(',', '.')
            OrdenServicio.objects.create(
                orden_id=orden,
                servicio_id_id=servicio_id,
                subtotal=subtotal
            )

        messages.success(request, 'Orden actualizada correctamente.')
        return redirect('listarOrdenes')

def eliminarOrden(request, id):
    orden = get_object_or_404(Orden, id_ord=id)
    try:
        with transaction.atomic():
            OrdenServicio.objects.filter(orden_id=orden).delete()
            orden.delete()
            messages.success(request, 'Orden eliminada correctamente.')
        return redirect('listarOrdenes')   
    except ProtectedError as e:
        messages.error(request, f'No se puede eliminar la orden porque está referenciada por: {e.protected_objects}')
        return redirect('listarOrdenes')  
    except Orden.DoesNotExist:
        messages.error(request, 'La orden no existe.')
        return redirect('listarOrdenes')  
    except IntegrityError:
        messages.error(request, 'Ha ocurrido un error durante la eliminación de la orden.')
        return redirect('listarOrdenes')
   
    


#Registrar Danios
def registrarDanios(request):
    ordenes = Orden.objects.all()
    return render(request,'registrarDanios2.html',{'ordenes':ordenes})

def guardarDanios(request):
    if request.method == 'POST':
        orden_id = request.POST['orden']
        orden = Orden.objects.get(id_ord=orden_id)
        if Inspeccion.objects.filter(orden_id=orden).exists():
            messages.error(request, 'Ya existe una inspección para esta orden.')
            return redirect('registrarDanios')
        # Crear inspección
        inspeccion = Inspeccion.objects.create(
                km=request.POST['km'],
                orden_id =orden,
                nivel_gasolina=request.POST['nivel_gasolina'],
                plumas='plumas' in request.POST,
                antena='antena' in request.POST,
                radio='radio' in request.POST,
                encendedor='encendedor' in request.POST,
                espejos='espejos' in request.POST,
                gata='gata' in request.POST,
                llave_de_ruedas='llave_de_ruedas' in request.POST,
                llanta_emergencia='llanta_emergencia' in request.POST,
                parlantes='parlantes' in request.POST,
                direccionales='direccionales' in request.POST,
                manubrios='manubrios' in request.POST,
                parabrisas='parabrisas' in request.POST,
                t_seguridad='t_seguridad' in request.POST,
                tapa_radiador='tapa_radiador' in request.POST,
                mandos_funcionales='mandos_funcionales' in request.POST,
                cenicero='cenicero' in request.POST,
                palanca='palanca' in request.POST,
                herramientas='herramientas' in request.POST,
                botiquin='botiquin' in request.POST,
                tapa_gasolina='tapa_gasolina' in request.POST,
                lunas='lunas' in request.POST,
                faros='faros' in request.POST,
                extintor='extintor' in request.POST,
                tapa_cubas='tapa_cubas' in request.POST,
                triangulos='triangulos' in request.POST,
                emblemas='emblemas' in request.POST,
                placas='placas' in request.POST,
                moquetas='moquetas' in request.POST
            )

        x_positions = request.POST.getlist('x_pos[]')
        y_positions = request.POST.getlist('y_pos[]')
        descriptions = request.POST.getlist('descripcion_dan[]')

        for x, y, desc in zip(x_positions, y_positions, descriptions):
            Danio.objects.create(
                x_pos=float(x),
                y_pos=float(y),
                descripcion_dan=desc,
                inspeccion_id=inspeccion
            )

        messages.success(request, 'Inspección registrados correctamente')
        return redirect('listarDanios')

def listarDanios(request):
    
    inspecciones = Inspeccion.objects.all()
    return render(request, 'listar_danios.html', {'danios': inspecciones})


def obtenerDanios(request, id_ord):
    inspeccion = get_object_or_404(Inspeccion, id_ins=id_ord)
    danios = Danio.objects.filter(inspeccion_id=inspeccion).values('id_dan', 'x_pos', 'y_pos', 'descripcion_dan')
    ordenes = Orden.objects.all()
    context = {
        'ordenes':ordenes,
        'inspeccion': inspeccion,
        'danios': json.dumps(list(danios)),
    }
    return render(request, 'obtenerDanio.html', context)


def actualizarDanios(request):
    if request.method == 'POST':
        
        # Actualizar inspección
        orden_id = request.POST['orden_id']
        orden = get_object_or_404(Orden, id_ord=orden_id)
        id_ins = request.POST['id_ins']

        # Actualizar inspección
        inspeccion, created = Inspeccion.objects.get_or_create(id_ins=id_ins)
        inspeccion.orden_id = orden  # Asegúrate de asignar el objeto Orden directamente
        inspeccion.km = request.POST.get('km')
        inspeccion.nivel_gasolina = request.POST.get('nivel_gasolina')
        
        checkboxes = [
            'plumas', 'antena', 'radio', 'encendedor', 'espejos',
            'gata', 'llave_de_ruedas', 'llanta_emergencia', 'parlantes',
            'direccionales', 'manubrios', 'parabrisas', 't_seguridad',
            'tapa_radiador', 'mandos_funcionales', 'cenicero', 'palanca',
            'herramientas', 'botiquin', 'tapa_gasolina', 'lunas', 'faros',
            'extintor', 'tapa_cubas', 'triangulos', 'emblemas', 'placas', 'moquetas'
        ]

        for checkbox in checkboxes:
            setattr(inspeccion, checkbox, checkbox in request.POST)

        inspeccion.save()
        id_dan_list = request.POST.getlist('id_dan[]')
        x_pos_list = request.POST.getlist('x_pos[]')
        y_pos_list = request.POST.getlist('y_pos[]')
        descripcion_dan_list = request.POST.getlist('descripcion_dan[]')
        delete_id_dan_list = request.POST.getlist('delete_id_dan[]')

        # Eliminar marcadores
        if delete_id_dan_list:
            Danio.objects.filter(id_dan__in=delete_id_dan_list).delete()

    
        for id_dan, x_pos, y_pos, descripcion_dan in zip(id_dan_list, x_pos_list, y_pos_list, descripcion_dan_list):
            if id_dan.startswith('marker-'):  # Nuevo marcador
                Danio.objects.create(
                    x_pos=float(x_pos),
                    y_pos=float(y_pos),
                    descripcion_dan=descripcion_dan,
                    inspeccion_id=inspeccion,
                )
            else:  
                danio = Danio.objects.get(id_dan=id_dan)
                danio.x_pos = float(x_pos)
                danio.y_pos = float(y_pos)
                danio.descripcion_dan = descripcion_dan
                danio.save()

        messages.success(request, 'Daños actualizados correctamente')
        return redirect('listarDanios')

def eliminarDanios(request,id_ins):
    inspeccion = get_object_or_404(Inspeccion, id_ins=id_ins)
    Danio.objects.filter(inspeccion_id=inspeccion).delete()
    inspeccion.delete()
    messages.success(request, 'Todos los daños asociados a la orden han sido eliminados correctamente')
    return redirect('listarDanios')
    
#DETALLES ORDENES
def listarDetalleOrden(request):
    ordenes_con_repuestos = Orden.objects.filter(ordenrepuesto__isnull=False).distinct()
    return render(request, 'listaDetalle.html', {'ordenes': ordenes_con_repuestos})


def guardarDetalle(request):
    ordenes = Orden.objects.all()
    return render(request,'detallesOrden.html',{'ordenes':ordenes})

def guardarRepuestos(request):
    if request.method == 'POST':
        orden_id = request.POST.get('orden_id')
        orden = Orden.objects.get(id_ord=orden_id)

        if OrdenRepuesto.objects.filter(orden_id=orden).exists():
            messages.error(request, 'Ya existen repuestos registrados para esta orden.')
            return redirect('registrarDetalle')

        nombres_rep = [nombre.upper() for nombre in request.POST.getlist('nombre_rep[]')]
        descripciones_rep = [descripcion.upper() for descripcion in request.POST.getlist('descripcion_rep[]')]
        precios_rep = request.POST.getlist('precio_rep[]')
        cantidades_rep = request.POST.getlist('cantidad_rep[]')
        subtotales_rep = request.POST.getlist('subtotal_rep[]')

        try:
            with transaction.atomic():
                for nombre, descripcion, precio, cantidad, subtotal in zip(nombres_rep, descripciones_rep, precios_rep, cantidades_rep, subtotales_rep):
                    OrdenRepuesto.objects.create(
                        orden_id=orden,
                        nombre_rep=nombre,
                        descripcion_rep=descripcion,
                        precio_rep=precio,
                        cantidad_rep=cantidad,
                        subtotal_rep=subtotal
                    )
            
            messages.success(request, 'Repuesto(s) guardado(s) correctamente')
            return redirect('listaDetalle')

        except Exception as e:
            messages.error(request, f'Error al guardar repuestos: {e}')
            return redirect('registrarDetalle')
    
    
    
def obtenerRepuestos(request, id):
    orden = get_object_or_404(Orden, id_ord=id)
    try:
        repuestos = OrdenRepuesto.objects.filter(orden_id=orden)
    except ObjectDoesNotExist:
        repuestos = []
    
    context = {
        'orden': orden,
        'repuestos': repuestos,
    }
    return render(request, 'obtenerRepuestos.html', context)

def editarRepuestos(request):
    if request.method == 'POST':
        
        orden_id = request.POST['orden_id']
        orden = Orden.objects.get(id_ord=orden_id)
        OrdenRepuesto.objects.filter(orden_id=orden).delete()
        nombre_rep_list = [nombre.upper() for nombre in request.POST.getlist('nombre_rep[]')]
        descripcion_rep_list= [descripcion.upper() for descripcion in request.POST.getlist('descripcion_rep[]')]
        precio_rep_list = request.POST.getlist('precio_rep[]')
        cantidad_rep_list = request.POST.getlist('cantidad_rep[]')
        subtotal_rep_list = request.POST.getlist('subtotal_rep[]')
        
        for nombre_rep, descripcion_rep, precio_rep, cantidad_rep, subtotal_rep in zip(nombre_rep_list, descripcion_rep_list, precio_rep_list, cantidad_rep_list, subtotal_rep_list):
            subtotal_rep = subtotal_rep.replace(',', '.')
            OrdenRepuesto.objects.create(
                orden_id=orden,
                nombre_rep=nombre_rep,
                descripcion_rep=descripcion_rep,
                precio_rep=precio_rep,
                cantidad_rep=cantidad_rep,
                subtotal_rep=subtotal_rep
            )

        messages.success(request, 'Detalle actualizado correctamente.')
        return redirect('listaDetalle')
    
def eliminarRepuestos(request,id):
    orden = get_object_or_404(Orden, id_ord=id)
    try:
        OrdenRepuesto.objects.filter(orden_id=orden).delete()
        messages.success(request, 'Todos los repuestos asociados a la orden han sido eliminados correctamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar repuestos: {str(e)}')
    return redirect('listaDetalle')


def detalleOrden(request, id):
    orden = get_object_or_404(Orden, id_ord=id)
    cliente = orden.vehiculo_id.cli_id
    vehiculo = orden.vehiculo_id
    servicios = OrdenServicio.objects.filter(orden_id=orden)
    repuestos = OrdenRepuesto.objects.filter(orden_id=orden)
    total_servicios = sum(servicio.subtotal for servicio in servicios)
    total_repuestos = sum(repuesto.subtotal_rep for repuesto in repuestos)
    total = total_servicios + total_repuestos
    
    context = {
        'orden': orden,
        'cliente': cliente,
        'vehiculo': vehiculo,
        'servicios': servicios,
        'repuestos': repuestos,
        'total': total,
    }
    
    return render(request, 'detalle_orden.html', context)

def reporte_inspeccion(request, id):
    inspeccion = get_object_or_404(Inspeccion, id_ins=id)
    danios = Danio.objects.filter(inspeccion_id=inspeccion).values('id_dan', 'x_pos', 'y_pos', 'descripcion_dan')
    ordenes = Orden.objects.all()
    context = {
        'ordenes':ordenes,
        'inspeccion': inspeccion,
        'danios': json.dumps(list(danios)),
    }
   
    return render(request, 'reporte_danios.html', context)