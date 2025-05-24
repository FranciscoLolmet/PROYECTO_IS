from django.db import models

class Vacacion(models.Model):
    empleado = models.ForeignKey('dashboard.Empleado', on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    dias_disfrutados = models.IntegerField()
    periodo = models.CharField(max_length=20)