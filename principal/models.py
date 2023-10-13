from django.db import models

class RegistroEmergencias(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    descripcion = models.TextField(max_length=50)
    codigoColor = models.TextField(max_length=20)
    fecha = models.DateTimeField(max_length=30)
    nro_pacientes = models.IntegerField(max_length=5)

    def __str__(self):
        return self.id


