from django.db import models

class Nacionalidad(models.Model):
    codigo_naci = models.CharField(max_length=18, primary_key=True)
    descripcion = models.CharField(max_length=50, null=True, blank=True)

class Pasajero(models.Model):
    id_pasajero = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=22, null=True, blank=True)
    apellido_paterno = models.CharField(max_length=25, null=True, blank=True)
    apellido_materno = models.CharField(max_length=25, null=True, blank=True)
    correo = models.EmailField(max_length=50, null=True, blank=True)
    codigo_naci = models.ForeignKey(Nacionalidad, on_delete=models.SET_NULL, null=True, blank=True)
    rut = models.CharField(max_length=18, null=True, blank=True)

class TipoUsuario(models.Model):
    id_tipo_usuario = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=60, null=True, blank=True)

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.SET_NULL, null=True, blank=True)
    password = models.CharField(max_length=30, null=True, blank=True)
    nombre_usuario = models.CharField(max_length=25, null=True, blank=True)

class TipoHabitacion(models.Model):
    id_tipo_habitacion = models.CharField(max_length=22, primary_key=True)
    nombre_tipo_hab = models.CharField(max_length=60, null=True, blank=True)

class Habitacion(models.Model):
    n_habitacion = models.AutoField(primary_key=True)
    tipo_habitacion = models.ForeignKey(TipoHabitacion, on_delete=models.SET_NULL, null=True, blank=True)
    estado_habitacion = models.CharField(max_length=30, null=True, blank=True)

class Reserva(models.Model):
    nro_reserva = models.AutoField(primary_key=True)
    pasajero = models.ForeignKey(Pasajero, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_reserva = models.DateField(null=True, blank=True)
    estado_reserva = models.CharField(max_length=22, null=True, blank=True)
    flag_particular = models.BooleanField(default=False)
    cantidad_persona = models.IntegerField(null=True, blank=True)
    nombre_empresa = models.CharField(max_length=40, null=True, blank=True)
    cantidad_dias = models.IntegerField(null=True, blank=True)

class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, db_column='id_pasajero')  # Asegúrate de que esto esté correcto
    fecha = models.DateField(null=True)
    pago_total = models.IntegerField(null=True)
    metodo_pago = models.CharField(max_length=18, null=True)

    
class Servicios(models.Model):
    id_servicios = models.AutoField(primary_key=True)  # AutoField genera un campo entero autoincremental
    descripcion = models.CharField(max_length=50, null=True, blank=True)  # Campo de texto con longitud máxima de 50

    def __str__(self):
        return self.Descripcion  # Devuelve la descripción como representación del objeto

class DetallePago(models.Model):
    id_pago = models.OneToOneField(Pago, on_delete=models.CASCADE, primary_key=True)
    id_servicios = models.ForeignKey(Servicios, on_delete=models.SET_NULL, null=True, blank=True)
    numero_linea = models.IntegerField()
    monto = models.IntegerField(null=True, blank=True)
