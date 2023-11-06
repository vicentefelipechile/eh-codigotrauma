


# ===========================================
# ========= Guardado de Contraseñas =========
# ===========================================
# ====================================================
# ================ Librerias y Clases ================
# ====================================================

from django.contrib.auth.hashers import make_password, check_password

from django.utils import timezone
from django.db import models
from django.db.models import Model
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

class HistorialEmergencias(Model):
    Emergencia = models.ForeignKey('RegistroEmergencias', on_delete=models.CASCADE)
    FechaRegistro = models.DateTimeField(default=timezone.now)
    Detalles = models.TextField()

    def __str__(self) -> str:
        return f"Historial de Emergencia: {self.Emergencia}, Fecha de Registro: {self.FechaRegistro}"
    
    def JsonResponse(self) -> str:
        return GetJson(self, ["Emergencia", "FechaRegistro", "Detalles"])



class RegistroEmergencias(Model):
    ID = models.CharField(primary_key=True, max_length=8)
    Descripcion = models.TextField(max_length=50)
    CodigoColor = models.TextField(max_length=20)
    Fecha = models.DateTimeField(max_length=30, default=timezone.now)
    NumeroPacientes = models.IntegerField()
    Doctores = models.ManyToManyField('DoctorClave', through='HistorialDoctoresEmergencia')

    def __str__(self):
        return self.id
    
    def JsonResponse(self) -> str:
        return GetJson(self, ["ID", "Descripcion", "CodigoColor", "Fecha", "NumeroPacientes"])



class HistorialDoctoresEmergencia(Model):
    Emergencia = models.ForeignKey('RegistroEmergencias', on_delete=models.SET_NULL, null=True)
    Doctor = models.ForeignKey('DoctorClave', on_delete=models.SET_NULL, null=True)
    FechaAsignacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Historial - Emergencia: {self.Emergencia}, Doctor: {self.Doctor}, Fecha: {self.FechaAsignacion}"
    
    def JsonResponse(self) -> str:
        return GetJson(self, ["Emergencia", "Doctor", "FechaAsignacion"])



# ===========================================
# ============== Clases Persona =============
# ===========================================

class Persona(Model):
    Rut: IntegerField = models.IntegerField(unique=True)
    Dv: CharField = models.CharField(max_length=1)
    PrimerNombre: TextField = models.TextField(max_length=20)
    SegundoNombre: TextField = models.TextField(max_length=20, null=True)
    ApellidoPaterno: TextField = models.TextField(max_length=20)
    ApellidoMaterno: TextField = models.TextField(max_length=20, null=True)

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
        return f"Primer Nombre: {self.PrimerNombre}, Apellido Paterno: {self.ApellidoPaterno}, Rut: {self.Rut}-{self.Dv}"

    class Meta:
        abstract = True



class Paciente(Persona):
    ID = models.IntegerField(primary_key=True)



class Secretario(Persona):
    ID = models.IntegerField(primary_key=True)
    CuentaUsuario = models.TextField(max_length=20)
    CuentaContrasena = models.TextField(max_length=64)

    # La contraseña se guarda encriptada en la base de datos.
    def SetContrasena(self, Contrasena: str) -> None:
        self.CuentaContrasena = make_password(Contrasena)

    # Se comprueba que la contraseña ingresada sea la misma que la guardada en la base de datos.
    def ComprobarContrasena(self, Contrasena: str) -> bool:
        return check_password(Contrasena, self.CuentaContrasena)



class Administrador(Persona):
    ID = models.IntegerField(primary_key=True)
    CuentaUsuario = models.TextField(max_length=20)
    CuentaContrasena = models.TextField(max_length=64)

    def SetContrasena(self, Contrasena: str) -> None:
        self.CuentaContrasena = make_password(Contrasena)

    def ComprobarContrasena(self, Contrasena: str) -> bool:
        return check_password(Contrasena, self.CuentaContrasena)



# ===========================================
# ============== Clases Fechas ==============
# ===========================================

class Horario(Model):
    DiaSemana = models.ForeignKey('DiaSemana', on_delete=models.SET_NULL, null=True)
    DiaHora = models.ForeignKey('HoraDia', on_delete=models.SET_NULL, null=True)
    Clase = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.DiaSemana.Nombre} - {str(self.DiaHora)}: {self.Clase}"

    def JsonResponse(self) -> str:
        return GetJson(self, ["DiaSemana", "DiaHora", "Clase"])


class DiaSemana(Model):
    Nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.Nombre
    
    def JsonResponse(self) -> str:
        return GetJson(self, ["Nombre"])



class HoraDia(Model):
    HoraInicio = models.TimeField(default=timezone.now)
    HoraFin = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"{self.HoraInicio.strftime('%H:%M')} - {self.HoraFin.strftime('%H:%M')}"
    
    def JsonResponse(self) -> str:
        return GetJson(self, ["HoraInicio", "HoraFin"])



# Creamos la clase "doctorClave" y la asociamos a la clase horario.

class DoctorClave(Persona):
    Area = models.TextField(max_length=30)
    Horario = models.OneToOneField(Horario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.rut)
    
    def JsonResponse(self) -> str:
        return GetJson(self, self.GetAllAttributes(["Area", "Horario"]))

class Area(Model):
    ID = models.IntegerField(primary_key=True)
    Nombre = models.TextField(max_length=30)
    def __str__(self):
        return self.Nombre