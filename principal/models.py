# ====================================================
# ================ Librerias y Clases ================
# ====================================================

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User

from django.utils import timezone
from django.db import models
from django.db.models import Model
from django.db.models import QuerySet
import json

from django.db.models import TextField, IntegerField, DateTimeField, CharField
from django.db.models import ForeignKey

# ===========================================
# ==== Funcion Json para todas las clases ===
# ===========================================

def GetJson(self: Model = None, Atributos: list = None) -> str:
    if not Atributos:
        Atributos = []

    JsonResponse: dict = {}

    for Atributo in Atributos:
        JsonResponse[Atributo] = self.__dict__[Atributo]

    return json.dumps(JsonResponse)



# ===========================================
# ==== Clases de Registros de Emergencia ====
# ===========================================


class Area(Model):
    area_id = models.AutoField(primary_key=True)
    area_nombre = models.TextField(max_length=30)



class Emergencia(Model):
    emerg_id = models.AutoField(primary_key=True)
    emerg_desc = models.TextField(max_length=50)
    emerg_color = models.TextField(max_length=20)
    emerg_fecha = models.DateTimeField(max_length=30, default=timezone.now)

    emerg_pac_id = models.ForeignKey('Paciente', on_delete=models.SET_NULL, to_field="pac_id", null=True, name="emerg_pac_id")
    emerg_doc_id = models.ForeignKey('Doctor', on_delete=models.SET_NULL, to_field="doc_id", null=True, name="emerg_doc_id")
    
    def JsonResponse(self) -> str:
        return GetJson(self, ["emerg_id", "emerg_desc", "emerg_color", "emerg_fecha", "emerg_pac_id", "emerg_doc_id"])

class AtencionPaciente(Model):
    atenc_id = models.AutoField(primary_key = True)
    atenc_descripcion = models.TextField(max_length=50)
    atenc_diagnostico = models.TextField(max_length=50)
    atenc_fecha = models.DateTimeField(max_length=30, default=timezone.now)


    atenc_pac_id = models.ForeignKey('Paciente', on_delete=models.SET_NULL, to_field="pac_id", null=True, name="atenc_pac_id")
    atenc_doc_id = models.ForeignKey('Doctor', on_delete=models.SET_NULL, to_field="doc_id", null=True, name="atenc_doc_id")
    
    def JsonResponse(self) -> str:
        return GetJson(self, ["atenc_id", "atenc_descripcion", "atenc_diagnostico", "atenc_fecha","atenc_pac_id", "atenc_doc_id"])



# ===========================================
# ============== Clases Persona =============
# ===========================================

class Persona(User):
    rut:                IntegerField = models.IntegerField(unique=True)
    dv:                 CharField = models.CharField(max_length=1)
    primernombre:       TextField = models.TextField(max_length=20)
    segundonombre:      TextField = models.TextField(max_length=20, null=True)
    apellidopaterno:    TextField = models.TextField(max_length=20)
    apellidomaterno:    TextField = models.TextField(max_length=20, null=True)
    anio_nacimiento:    IntegerField = models.IntegerField()
    direccion:          TextField = models.TextField()
    ciudad:             TextField = models.TextField()
    estado:             TextField = models.TextField()
    codigo_postal:      CharField = models.CharField(max_length=10)

    def GetAllAttributes(self, AtributosExtra: list = None) -> list:
        AllAttributes: list = [Atributo for Atributo in self.__dict__.keys() if not Atributo.startswith("_")]

        if not AtributosExtra:
            AtributosExtra = []
        
        for Atributo in AtributosExtra:
            AllAttributes.append(Atributo)

        return AllAttributes

    def JsonResponse(self) -> str:
        return GetJson(self, self.GetAllAttributes())

    class Meta:
        abstract = True



class Paciente(Model):
    pac_id = models.AutoField(primary_key=True)
    
    def GetEmergencias(self) -> QuerySet:
        return Emergencia.objects.filter(emerg_pac_id=self.pac_id)
    
    def cantidad_emergencias(self) -> int:
        return Emergencia.objects.filter(emerg_pac_id=self.pk).count()



class Secretario(Persona):
    sec_id = models.AutoField(primary_key=True)
    
    def JsonResponse(self) -> str:
        return GetJson(self, ["sec_id"])



class Administrador(Persona):
    adm_id = models.AutoField(primary_key=True)
    
    def JsonResponse(self) -> str:
        return GetJson(self, ["adm_id"])


class Doctor(Persona):
    doc_id = models.AutoField(primary_key=True)
    doc_area_id = models.ForeignKey('Area', on_delete=models.SET_NULL, null=True, to_field="area_id", name="doc_area_id")
    doc_hor_id = models.ForeignKey('Horario', on_delete=models.SET_NULL, null=True, to_field="hor_id", name="doc_hor_id")
    
    def JsonResponse(self) -> str:
        return GetJson(self, self.GetAllAttributes(["doc_area_id", "doc_hor_id"]))



# ===========================================
# ============== Clases Fechas ==============
# ===========================================

class Horario(Model):
    hor_id = models.AutoField(primary_key=True)
    hor_sem_id = models.ForeignKey('DiaSemana', on_delete=models.SET_NULL, null=True, to_field="sem_id", name="hor_sem_id")
    hor_horadia_id = models.ForeignKey('HoraDia', on_delete=models.SET_NULL, null=True, to_field="hordia_id", name="hor_horadia_id")

    def JsonResponse(self) -> str:
        return GetJson(self, ["DiaSemana", "DiaHora", "Clase"])



class DiaSemana(Model):
    sem_id = models.AutoField(primary_key=True)
    sem_nombre = models.CharField(max_length=20)
    
    def JsonResponse(self) -> str:
        return GetJson(self, ["sem_id", "sem_nombre"])



class HoraDia(Model):
    hordia_id = models.AutoField(primary_key=True)
    hordia_inicio = models.TimeField(default=timezone.now)
    hordia_fin = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"{self.hordia_inicio.strftime('%H:%M')} - {self.hordia_fin.strftime('%H:%M')}"
    
    def JsonResponse(self) -> str:
        return GetJson(self, ["hordia_inicio", "hordia_fin"])