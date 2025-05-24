from django.db import models

class Empleado(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_ingreso = models.DateField()
    cargo = models.CharField(max_length=50)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default='activo')

class Nomina(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    periodo = models.CharField(max_length=20)  # semanal, quincenal, mensual
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField()

class Prestacion(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_otorgada = models.DateField()

class Indicador(models.Model):
    indicador = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_registro = models.DateField()

class Reporte(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_generacion = models.DateTimeField(auto_now_add=True)

class Administrativo(models.Model):
    nombre_modulo = models.CharField(max_length=100)
    configuracion = models.TextField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)
