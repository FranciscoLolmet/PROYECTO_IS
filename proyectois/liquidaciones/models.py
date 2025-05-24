from django.db import models

class Liquidacion(models.Model):
    empleado_id = models.IntegerField(verbose_name="ID Empleado")
    fecha_baja = models.DateField(verbose_name="Fecha de Baja")
    anos_historico = models.IntegerField(
        db_column='años_historico',
        verbose_name="Años considerados"
    )
    monto_salarios_pendientes = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Salarios Pendientes"
    )
    monto_vacaciones = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Vacaciones"
    )
    monto_aguinaldo_prop = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Aguinaldo Proporcional"
    )
    monto_bono14_prop = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Bono 14 Proporcional"
    )
    monto_dias_trabajados = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Días Trabajados"
    )
    total_liquidacion = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name="Total Liquidación"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )

    class Meta:
        managed = False
        db_table = 'liquidaciones'
        verbose_name = "Liquidación"
        verbose_name_plural = "Liquidaciones"
        ordering = ['-fecha_baja']

    def __str__(self):
        return f"Liquidación {self.id} - Empleado {self.empleado_id}"