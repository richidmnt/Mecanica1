from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('guardarUsuario/', views.guardarUsuario, name="guardarUsuario"),
    path('registrarUsuario/', views.registrarUsuario),
    path('eliminarUsuario/<id>', views.eliminarUsuario, name="eliminarUsuario"),
    path('listaClientes/',views.listaClientes,name="listaClientes"),
    path('guardarCliente/',views.guardarCliente, name="guardarCliente"),
    path('registrarCliente/',views.registrarCliente),
    path('eliminarCliente/<id>',views.eliminarCliente),
    path('obtenerCliente/<id>/',views.obtenerClietne),
    path('actualizarCliente/',views.actualizarCliente),
    path('listaServicios/',views.listaServicios,name="listaServicios"),
    path('guardarServicio/',views.guardarServicio,name="guardarServicio"),
    path('registrarServicio/',views.registrarServicio),
    path('eliminarServicio/<id>/',views.eliminarServicio),
    path('obtenerServicio/<id>/',views.obtenerServicio),
    path('actualizarServicio/',views.actualizarServicio),
    path('listaVehiculos/',views.listaVehiculos,name="listaVehiculos"),
    path('guardarVehiculo/',views.guardarVehiculo,name="guardarVehiculo"),
    path('registrarVehiculo/',views.registrarVehiculo),
    path('eliminarVehiculo/<id>/',views.eliminarVehiculo),
    path('obtenerVehiculo/<id>/',views.obtenerVehiculo),
    path('actualizarVehiculo/',views.actualizarVehiculo)
]
