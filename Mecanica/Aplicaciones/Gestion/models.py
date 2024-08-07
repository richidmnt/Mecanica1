from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Taller(models.Model):
    nombre_tall = models.CharField(max_length=255)
    descripcion_tall = models.TextField()
    logo_tall = models.FileField(upload_to="Taller",null=True,blank=True)
    direccion_tall = models.CharField(max_length=100)
    email_tall = models.EmailField()
    telefono_tall = models.CharField(max_length=11)

class Direccion(models.Model):
    id_dir = models.AutoField(primary_key=True)
    ciudad_dir = models.CharField(max_length=255)
    barrio_dir = models.CharField(max_length=255)
    calle_dir = models.CharField(max_length=255)
    numero_dir = models.CharField(max_length=10)

class Usuario(models.Model):
    id_usr = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    
    ADMINISTRADOR = 'ADMINISTRADOR'
    MECANICO = 'MECANICO'
    ROLES = [
        (ADMINISTRADOR, 'Administrador'),
        (MECANICO, 'Mecánico'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES)
    is_active = models.BooleanField(default=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.username})"



class Cliente(models.Model):
    id_cli = models.AutoField(primary_key=True)
    nombre_cli = models.CharField(max_length=255)
    apellido_cli = models.CharField(max_length=255)
    ci_cli = models.CharField(max_length=10,unique=True)
    telefono_cli = models.CharField(max_length=20)
    email_cli = models.EmailField(unique=True)
    dir_id = models.ForeignKey(Direccion, on_delete=models.CASCADE)

class Vehiculo(models.Model):
    id_veh = models.AutoField(primary_key=True)
    marca_veh = models.CharField(max_length=255)
    modelo_veh = models.CharField(max_length=255)
    placa_veh = models.CharField(max_length=20, unique=True)
    anio_veh = models.IntegerField()
    chasis_veh = models.CharField(max_length=255)
    color_veh = models.CharField(max_length=255)
    cli_id = models.ForeignKey(Cliente, on_delete=models.PROTECT)

class Servicio(models.Model):
    id_ser = models.AutoField(primary_key=True)
    nombre_ser = models.CharField(max_length=255)
    descripcion_ser = models.TextField()
    precio_ser = models.DecimalField(max_digits=10, decimal_places=2)

class Inspeccion(models.Model):
    id_ins = models.AutoField(primary_key=True)
    km = models.PositiveIntegerField()
    nivel_gasolina = models.CharField(max_length=50)
    plumas = models.BooleanField(default=False)
    antena = models.BooleanField(default=False)
    radio = models.BooleanField(default=False)
    encendedor = models.BooleanField(default=False)
    espejos = models.BooleanField(default=False)
    gata = models.BooleanField(default=False)
    llave_de_ruedas = models.BooleanField(default=False)
    llanta_emergencia = models.BooleanField(default=False)
    parlantes = models.BooleanField(default=False)
    direccionales = models.BooleanField(default=False)
    manubrios = models.BooleanField(default=False)
    parabrisas = models.BooleanField(default=False)
    t_seguridad = models.BooleanField(default=False)
    tapa_radiador = models.BooleanField(default=False)
    mandos_funcionales = models.BooleanField(default=False)
    cenicero = models.BooleanField(default=False)
    palanca = models.BooleanField(default=False)
    herramientas = models.BooleanField(default=False)
    botiquin = models.BooleanField(default=False)
    tapa_gasolina = models.BooleanField(default=False)
    lunas = models.BooleanField(default=False)
    faros = models.BooleanField(default=False)
    extintor = models.BooleanField(default=False)
    tapa_cubas = models.BooleanField(default=False)
    triangulos = models.BooleanField(default=False)
    emblemas = models.BooleanField(default=False)
    placas = models.BooleanField(default=False)
    moquetas = models.BooleanField(default=False)

    def __str__(self):
        return f"Inspección: {self.id} - KM: {self.km}"
    

class Danio(models.Model):
    id_dan = models.AutoField(primary_key=True)
    imagen_dan = models.FileField(upload_to="danio",null=True,blank=True)
    descripciom_dan = models.TextField()

class Orden(models.Model):
    id_ord=models.AutoField(primary_key=True)
    fecha_ord = models.DateTimeField()
    fecha_fin_ord = models.DateTimeField()
    numero_ord = models.IntegerField()
    observaciones_ord = models.TextField()
    estado_ord = models.CharField(max_length=30)
    usuario_id = models.ForeignKey(Usuario,on_delete=models.PROTECT)
    vehiculo_id = models.ForeignKey(Vehiculo, on_delete=models.PROTECT)
    inspeccion_id = models.ForeignKey(Inspeccion, on_delete=models.PROTECT)
    danios_id = models.ForeignKey(Danio, on_delete=models.PROTECT)

class OrdenServicio(models.Model):
    id_ord_ser = models.AutoField(primary_key=True)
    orden_id = models.ForeignKey(Orden, on_delete=models.CASCADE)
    servicio_id = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)

    
class OrdenRepuesto(models.Model):
    id_rep = models.AutoField(primary_key=True)
    orden_id = models.ForeignKey(Orden, on_delete=models.CASCADE)
    nombre_rep = models.CharField(max_length=255)
    descripcion_rep = models.TextField()
    precio_rep = models.DecimalField(max_digits =10 ,decimal_places = 2)
    cantidad_rep = models.IntegerField()
    subtotal_rep = models.DecimalField(max_digits=10,decimal_places=2)


