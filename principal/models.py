from django.db import models

# Create your models here.
class RegistroEmergencias(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    descripcion = models.TextField( max_length=50)
