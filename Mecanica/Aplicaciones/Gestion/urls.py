from django.urls import path
from . import views
urlpatterns = [
    path('',views.login_view,name="login"),
    path('home/',views.home,name="home"),
    path('home2/',views.home2,name="home2"),
    path('index/', views.index, name="index"),
    path('guardarUsuario/', views.guardarUsuario, name="guardarUsuario"),
    path('registrarUsuario/', views.registrarUsuario),
    path('actualizarUsuario/<id_usr>/',views.actualizarUsuario,name="actualizarUsuario"),
    path('eliminarUsuario/<id>', views.eliminarUsuario, name="eliminarUsuario"),
    path('listaClientes/',views.listaClientes,name="listaClientes"),
    path('guardarCliente/',views.guardarCliente, name="guardarCliente"),
    path('registrarCliente/',views.registrarCliente),
    path('eliminarCliente/<id>',views.eliminarCliente),
    path('actualizarCliente/<id_cli>/',views.actualizarCliente,name="editarCliente"),
    path('listaServicios/',views.listaServicios,name="listaServicios"),
    path('guardarServicio/',views.guardarServicio,name="guardarServicio"),
    path('registrarServicio/',views.registrarServicio),
    path('eliminarServicio/<id>/',views.eliminarServicio),
    path('obtenerServicio/<id>/',views.obtenerServicio,name='obtenerServicio'),
    path('actualizarServicio/',views.actualizarServicio),
    path('listaVehiculos/',views.listaVehiculos,name="listaVehiculos"),
    path('guardarVehiculo/',views.guardarVehiculo,name="guardarVehiculo"),
    path('registrarVehiculo/',views.registrarVehiculo),
    path('eliminarVehiculo/<id>/',views.eliminarVehiculo),
    path('actualizarVehiculo/<id_veh>/',views.actualizarVehiculo,name="editarVehiculo"),
    path('guardarOrden/',views.guardarOrden,name="ordenCliente"),
    path('registrarOrden/',views.registrarOrden),
    path('listarOrdenesF/',views.listarOrdenesNoFinalizadas,name="listarOrdenes"),
    path('registrarDanios/',views.registrarDanios,name="registrarDanios"),
    path('guardarDanios/',views.guardarDanios),
    path('listarDanios/',views.listarDanios,name="listarDanios"),
    path('editarDanio/<id_ord>/',views.obtenerDanios),
    path('actualizarDanios/',views.actualizarDanios),
    path('eliminarDanio/<id_ins>/',views.eliminarDanios),
    path('listarDetalle/',views.listarDetalleOrden,name="listaDetalle"),
    path('guardarDetalle/',views.guardarDetalle,name="registrarDetalle"),
    path('registrarRepuestos/',views.guardarRepuestos),
    path('obtenerOrden/<id>/',views.obtenerOrden),
    path('editarOrden/',views.editarOrden),
    path('eliminarOrden/<id>/',views.eliminarOrden),
    path('guardarOrden2/',views.guardarOrden2, name="guardarOrden2"),
    path('registrarOrden2/',views.registrarOrden2),
    path('obtenerRepuestos/<id>/',views.obtenerRepuestos),
    path('editarRepuestos/',views.editarRepuestos),
    path('eliminarDetalle/<id>/',views.eliminarRepuestos),
    path('detalleOrden/<id>/',views.detalleOrden),
    path('detalleInspeccion/<id>/',views.reporte_inspeccion),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout,name="logout"),
    path('listaOrdenM/',views.ordenes_mecanico,name="ordenesM"),
    path('aceptar_orden/<int:id_ord>/', views.aceptar_orden, name='aceptar_orden'),
    path('lista-progreso/',views.lista_progreso,name="listaProgreso"),
    path('cambiar_estado_orden/<int:id_ord>/<str:nuevo_estado>/', views.cambiar_estado_orden, name='cambiar_estado_orden'),
    path('listar_inspecciones/',views.listar_inspecciones,name="listarInspeccionM"),
    path('guardarDaniosM/',views.guardarDaniosM),
    path('actualizarDaniosM/',views.actualizarDaniosM),
    path('editarDanioM/<id_ord>/',views.obtenerDaniosM),
    path('actualizarDaniosM/',views.actualizarDaniosM),
    path('eliminarDanioM/<id_ins>/',views.eliminarDaniosM),
    path('ordenesCompletas/',views.listar_ordenes_completadas,name="ordenesCompletas"),
    path('usuariosEliminados/',views.listaUsuariosEliminados,name="usuariosEliminados"),
    path('restaurarUsuario/<id>/',views.restaurarUsuario),
    path('clientesEliminados/', views.clientesEliminados,name="clientesEliminados"),
    path('restaurarCliente/<id>/',views.restaurarCliente),
    path('serviciosEliminados/',views.serviciosEliminados,name="serviciosEliminados"),
    path('restaurarServicio/<id>/',views.restaurarServicio),
    path('ordenesFinalizadas/',views.listarOrdenesFinalizadas,name='ordenesFinalizadas'),
    path('buscar_vehiculo/', views.buscar_vehiculo, name='buscar_vehiculo'),
    path('obtener_nombres_repuestos/', views.obtener_nombres_repuestos, name='obtener_nombres_repuestos'),
]

