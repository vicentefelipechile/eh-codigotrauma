# ====================================================
# ================ Librerias y Clases ================
# ====================================================

from django.contrib.auth.hashers import make_password, check_password

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

class Emergencia(Model):
    emerg_id = models.AutoField(primary_key=True)
    emerg_desc = models.TextField(max_length=50)
    emerg_color = models.TextField(max_length=20)
    emerg_fecha = models.DateTimeField(max_length=30, default=timezone.now)

    emerg_pac_id = models.ForeignKey('Paciente', on_delete=models.SET_NULL, to_field="pac_id", null=True, name="emerg_pac_id")
    emerg_doc_id = models.ForeignKey('Doctor', on_delete=models.SET_NULL, to_field="doc_id", null=True, name="emerg_doc_id")

    def __str__(self):
        return self.emerg_id
    
    def JsonResponse(self) -> str:
        return GetJson(self, ["emerg_id", "emerg_desc", "emerg_color", "emerg_fecha", "emerg_pac_id", "emerg_doc_id"])



class HistorialEmergencia(Model):
    hist_id = models.AutoField(primary_key=True)
    hist_emerg_id = models.ForeignKey('Emergencia', on_delete=models.CASCADE, null=True,to_field="emerg_id")
    hist_fecha = models.DateTimeField(default=timezone.now)
    hist_detalle = models.TextField()

    def __str__(self) -> str:
        return f"Historial de Emergencia: {self.Emergencia}, Fecha de Registro: {self.FechaRegistro}"
    
    def JsonResponse(self) -> str:
        return GetJson(self, ["hist_emerg_id", "hist_fecha", "hist_detalle"])



class HistorialDoctorEmergencia(Model):
    histdoct_id = models.AutoField(primary_key=True)
    histdoct_emerg_id = models.ForeignKey('Emergencia', on_delete=models.SET_NULL, null=True, to_field="emerg_id", name="histdoct_emerg_id")
    histdoct_doc_id = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, to_field="doc_id", name="histdoct_doc_id")
    histdoct_fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Historial - Emergencia: {self.histdoct_emerg_id}, Doctor: {self.histdoct_doc_id}, Fecha: {self.histdoct_fecha}"
    
    def JsonResponse(self) -> str:
        return GetJson(self, ["histdoct_emerg_id", "histdoct_doc_id", "histdoct_fecha"])



# ===========================================
# ============== Clases Persona =============
# ===========================================

class Persona(Model):
    rut: IntegerField = models.IntegerField(unique=True)
    dv: CharField = models.CharField(max_length=1)
    primernombre: TextField = models.TextField(max_length=20)
    segundonombre: TextField = models.TextField(max_length=20, null=True)
    apellidopaterno: TextField = models.TextField(max_length=20)
    apellidomaterno: TextField = models.TextField(max_length=20, null=True)

    def GetAllAttributes(self, AtributosExtra: list = None) -> list:
        AllAttributes: list = [Atributo for Atributo in self.__dict__.keys() if not Atributo.startswith("_")]

        if not AtributosExtra:
            AtributosExtra = []
        
        for Atributo in AtributosExtra:
            AllAttributes.append(Atributo)

        return AllAttributes

    def JsonResponse(self) -> str:
        return GetJson(self, self.GetAllAttributes())

    def __str__(self):
        return f"Primer Nombre: {self.primernombre}, Apellido Paterno: {self.apellidopaterno}, Rut: {self.rut}-{self.dv}"

    class Meta:
        abstract = True



class Paciente(Persona):
    pac_id = models.AutoField(primary_key=True)
    
    # Obtener los registros de emergencias asociados al paciente
    def GetEmergencias(self) -> QuerySet:
        return Emergencia.objects.filter(emerg_pac_id=self.pac_id)



class Secretario(Persona):
    sec_id = models.AutoField(primary_key=True)
    sec_cuentausuario = models.TextField(max_length=20)
    sec_cuentacontrasena = models.TextField(max_length=64)
    
    def __str__(self):
        return str(self.rut)
    
    def JsonResponse(self) -> str:
        return GetJson(self, ["sec_id"])

    # La contraseña se guarda encriptada en la base de datos.
    def SetContrasena(self, Contrasena: str) -> None:
        self.sec_cuentacontrasena = make_password(Contrasena)

    # Se comprueba que la contraseña ingresada sea la misma que la guardada en la base de datos.
    def ComprobarContrasena(self, Contrasena: str) -> bool:
        return check_password(Contrasena, self.sec_cuentacontrasena)



class Administrador(Persona):
    adm_id = models.AutoField(primary_key=True)
    adm_cuentausuario = models.TextField(max_length=20)
    adm_cuentacontrasena = models.TextField(max_length=64)
    
    def __str__(self):
        return str(self.rut)
    
    def JsonResponse(self) -> str:
        return GetJson(self, ["adm_id", "adm_cuentausuario", "adm_cuentacontrasena"])

    def SetContrasena(self, Contrasena: str) -> None:
        self.adm_cuentacontrasena = make_password(Contrasena)

    def ComprobarContrasena(self, Contrasena: str) -> bool:
        return check_password(Contrasena, self.adm_cuentacontrasena)


class Doctor(Persona):
    doc_id = models.AutoField(primary_key=True)
    doc_area_id = models.ForeignKey('Area', on_delete=models.SET_NULL, null=True, to_field="area_id", name="doc_area_id")
    doc_hor_id = models.ForeignKey('Horario', on_delete=models.SET_NULL, null=True, to_field="hor_id", name="doc_hor_id")
    doc_cuentausuario = models.TextField(max_length=20)
    doc_cuentacontrasena = models.TextField(max_length=64)

    def __str__(self):
        return str(self.rut)
    
    def JsonResponse(self) -> str:
        return GetJson(self, self.GetAllAttributes(["doct_area", "doct_horario"]))

    def SetContrasena(self, Contrasena: str) -> None:
        self.doct_cuentacontrasena = make_password(Contrasena)

    def ComprobarContrasena(self, Contrasena: str) -> bool:
        return check_password(Contrasena, self.doct_cuentacontrasena)


class Area(Model):
    area_id = models.AutoField(primary_key=True)
    area_nombre = models.TextField(max_length=30)

    def __str__(self):
        return self.area_nombre



# ===========================================
# ============== Clases Fechas ==============
# ===========================================

class Horario(Model):
    hor_id = models.AutoField(primary_key=True)
    hor_sem_id = models.ForeignKey('DiaSemana', on_delete=models.SET_NULL, null=True, to_field="sem_id", name="hor_sem_id")
    hor_horadia_id = models.ForeignKey('HoraDia', on_delete=models.SET_NULL, null=True, to_field="hordia_id", name="hor_horadia_id")


    def __str__(self):
        return f"{self.DiaSemana.Nombre} - {str(self.DiaHora)}: {self.Clase}"

    def JsonResponse(self) -> str:
        return GetJson(self, ["DiaSemana", "DiaHora", "Clase"])



class DiaSemana(Model):
    sem_id = models.AutoField(primary_key=True)
    sem_nombre = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.sem_id} - {self.sem_nombre}"
    
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