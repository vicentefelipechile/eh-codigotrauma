# ====================================================
# ================ Librerias y Clases ================
# ====================================================

from typing import Any
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Permission

from django.utils import timezone
from django.db import models
from django.db.models import Model

from django.forms import ChoiceField
from django.db.models import TextField, IntegerField, CharField, AutoField, TimeField
from django.db.models import ForeignKey, ManyToManyField

from .sms import send_sms
from hashlib import sha256
from random import randint


# ===========================================
# ============== Modelos Varios =============
# ===========================================

# Utilizado por "Usuarios" para definir los permisos de cada usuario
class Permisos(Model):
    class Tipos():
        ROOT:       int = 0
        ADMIN:      int = 1
        SECRETARIO: int = 5
        DOCTOR:     int = 10
        PACIENTE:   int = 100

    permiso_id:     AutoField = AutoField(primary_key=True)
    permiso_nombre: TextField = TextField(max_length=30)


# Utilizado por "Doctor" para definir a que area pertenece
class Area(Model):
    area_id:        AutoField = AutoField(primary_key=True)
    area_nombre:    TextField = TextField(max_length=30)


# Utilizado por "Horario" para los turnos
class HoraDia(Model):
    hordia_id:      AutoField = AutoField(primary_key=True)
    hordia_inicio:  TimeField = TimeField(default=timezone.now)
    hordia_fin:     TimeField = TimeField(default=timezone.now)


# Utilizado por "Horario" para los dias de la semana
class DiaSemana(Model):
    diasem_id:      AutoField = AutoField(primary_key=True)
    diasem_nombre:  TextField = TextField(max_length=30)


# Utilizado por "Doctor" para definir su horario
class Horario(Model):
    horario_id:     AutoField = AutoField(primary_key=True)
    horario_hora:   ForeignKey = ForeignKey(HoraDia, on_delete=models.SET_NULL, to_field="hordia_id", null=True, name="horario_hora")
    horario_dia:    ForeignKey = ForeignKey(DiaSemana, on_delete=models.SET_NULL, to_field="diasem_id", null=True, name="horario_dia")



# ===========================================
# ============== Modelos Base ===============
# ===========================================


# Utilizado como Base para la administracion de usuarios y contraseñas en el sistema,
# con esto se puede mantener un listado de usuarios y el rol que tienen.
# (Paciente, Doctor, Secretario, Administrador)
class Usuario(Model):
    
    # Enumeracion de tipos de usuario
    ROOT:       int = 0
    ADMIN:      int = 1
    SECRETARIO: int = 2
    DOCTOR:     int = 3
    PACIENTE:   int = 4
    
    USER_TYPE_CHOICES: list[ tuple[int | str] ] = [
        (ROOT,          "Root"),
        (ADMIN,         "Administrador"),
        (SECRETARIO,    "Secretario"),
        (DOCTOR,        "Doctor"),
        (PACIENTE,      "Paciente"),
    ]

    # Establecer tipo de usuario por defecto a "Usuario" utilizando el metodo "UsuarioTipo"
    user_type:              IntegerField = IntegerField(choices=USER_TYPE_CHOICES, default=PACIENTE)

    user_name:              CharField = CharField(max_length=30, unique=True)
    user_password:          CharField = CharField(max_length=128)
    
    # ===== CRUD =====
    
    def crear_usuario(self, username: str = None, password: str = None, datos: dict = None) -> object | None:
        if not username:
            raise Exception("No se ha especificado un nombre de usuario")
        
        if not password:
            raise Exception("No se ha especificado una contraseña")
        
        if not datos:
            datos = {}
        
        # Crear usuario
        user = self.create(user_name=username, user_password=make_password(password))
        
        # Crear datos
        for key, value in datos.items():
            setattr(user, key, value)
        
        return user
    
    def borrar_usuario(self) -> None:
        self.delete()
    
    def modificar_usuario(self, datos: dict = None) -> None:
        if not datos:
            return

        # Eliminar datos que no se pueden modificar
        datos["pers_rut"] = None
        datos["pers_dv"] = None
        
        password = datos.pop("password", None)
        
        # Modificar datos
        for key, value in datos.items():
            setattr(self, key, value)
        
        # Modificar contraseña
        if password:
            self.password = make_password(password)
            
        self.save()
        
    def obtenertipo_usuario(self, tostring: bool = False) -> int | str:
        if tostring:
            return self.USER_TYPE_CHOICES[self.user_type][1]
        
        return self.user_type

    def obtenerdatos_usuario(self, target: list = None) -> dict:
        datos: dict = {}
        
        # Si no esta especificado el target, retornar todos los datos
        if not target:
            for key, value in self.__dict__.items():
                if not key.startswith("_"):
                    datos[key] = value
        else:
            for key in target:
                if key in self.__dict__:
                    datos[key] = self.__dict__[key]
                
        return datos


# Utilizado como Base para todos los modelos que usen a una persona, ademas de añadir un inicio de sesion
class Persona(Usuario):
    pers_rut:               IntegerField = models.IntegerField(unique=True)
    pers_dv:                CharField = CharField(max_length=1)
    pers_primernombre:      TextField = TextField(max_length=24)
    pers_segundonombre:     TextField = TextField(max_length=24, null=True)
    pers_apellidopaterno:   TextField = TextField(max_length=24)
    pers_apellidomaterno:   TextField = TextField(max_length=24, null=True)
    pers_nacimiento:        IntegerField = IntegerField()
    pers_direccion:         TextField = TextField(null=True)
    pers_ciudad:            TextField = TextField(null=True)
    pers_estado:            TextField = TextField(null=True)
    pers_codigopostal:      IntegerField = IntegerField(null=True)
    
    class Meta:
        abstract = True


# Modelo utilizado para almacenar las sessiones de los usuarios, se utiliza para mantener la sesion activa
class Session(Model):
    session_id:     AutoField = AutoField(primary_key=True)
    session_key:    CharField = CharField(max_length=40, unique=True)
    session_data:   TextField = TextField(null=True)
    session_expire: IntegerField = IntegerField(default=0, null=True)
    
    def SetSessionUser(self, user: Usuario, ip: str = None) -> str:
        value: str = make_password(user.user_name, salt=ip)
        value = sha256(value.encode("utf-8")).hexdigest()
        
        self.session_key = user.user_name
        self.session_data = value
        self.session_expire = timezone.now().timestamp() + (60 * 60 * 24 * 7)  # La session expira en 1 semana
        
        return value
    
    def GetSessionUser(self) -> str:
        return self.session_key
    
    def IsSessionValid(self) -> bool:
        return self.session_expire > timezone.now().timestamp()
    
    def CheckSesion(self, user: Usuario, hashsession: str = None, ip: str = None) -> bool: 
        if not hashsession: return False
        if not ip:          return False
        
        # Obtener la sesion del usuario utilizando el usuario como llave
        session = Session.objects.get(session_key=user.user_name)
        if not session:     return False
        if session == "":   return False
        
        # Verificar que la sesion no haya expirado
        if not session.IsSessionValid(): return False
        
        # Verificar que la sesion sea valida
        value: str = make_password(user.user_name, salt=ip)
        value = sha256(value.encode("utf-8")).hexdigest()
        
        if value != hashsession: return False
        
        return True


# ===========================================
# ============= Modelos Persona =============
# ===========================================

# El modelo "Paciente" utiliza como base a "Model" debido a que no es un usuario recurrente en el sistema, solo existe para el registro de emergencias
class Paciente(Model):
    pac_id:                 AutoField = AutoField(primary_key=True)
    pac_rut:                IntegerField = IntegerField(unique=True)
    pac_dv:                 CharField = CharField(max_length=1)
    pac_primernombre:       TextField = TextField(max_length=24, null=True)
    pac_segundonombre:      TextField = TextField(max_length=24, null=True)
    pac_apellidopaterno:    TextField = TextField(max_length=24, null=True)
    pac_apellidomaterno:    TextField = TextField(max_length=24, null=True)
    pac_nacimiento:         IntegerField = IntegerField()
    pac_direccion:          TextField = TextField()
    pac_ciudad:             TextField = TextField()
    pac_estado:             TextField = TextField()
    pac_codigopostal:       IntegerField = IntegerField()

    # Mostrar el total de emergencias que ha tenido el paciente
    def total_emergencias(self) -> int:
        num_emergencias = Emergencia.objects.filter(emerg_pac_id=self).count()
        return num_emergencias

    def total_atenciones(self) -> int:
        num_atenciones = Atencion.objects.filter(atenc_pac_id = self).count()
        return num_atenciones


# El modelo "Doctor" utiliza como base a "Persona" debido a que es un usuario recurrente en el sistema
class Doctor(Persona):
    doc_id:                 AutoField = AutoField(primary_key=True)
    doc_especialidad:       TextField = TextField(max_length=30)
    doc_area:               ForeignKey = ForeignKey(Area, on_delete=models.SET_NULL, to_field="area_id", null=True, name="doc_area")
    doc_horario:            ForeignKey = ForeignKey(Horario, on_delete=models.SET_NULL, to_field="horario_id", null=True, name="doc_horario")
    
    def total_emergencias(self) -> int:
        num_emergencias = Emergencia.objects.filter(emerg_doc_id=self).count()
        print(f"DEBUG: Número de emergencias para {self.pers_primernombre}: {num_emergencias}")
        return num_emergencias



# El modelo "Secretario" utiliza como base a "Persona" ya que es quien se encarga de administrar las emergencias
class Secretario(Persona):
    sec_id:                 AutoField = AutoField(primary_key=True)


# El modelo "Administrador" utiliza como base a "Persona" ya que es quien se encarga de administrar todos los usuarios
class Administrador(Persona):
    adm_id:                 AutoField = AutoField(primary_key=True)



# ===========================================
# ============= Modelos Registro ============
# ===========================================

# El modelo "Emergencia" utilizara como modelo base a "Model" y tendra asociado a un "Doctor" y a un "Paciente"
class Emergencia(Model):
    emerg_id:               AutoField = AutoField(primary_key=True)
    emerg_desc:             TextField = TextField(max_length=50)
    emerg_color:            TextField = TextField(max_length=20)
    emerg_fecha:            TextField = TextField(max_length=30, default=timezone.now)
    
    # Una emergencia puede tener muchos pacientes, hacer una relacion muchos a muchos a los Pacientes (pac_id)
    emerg_pac_id:           ManyToManyField = models.ManyToManyField(Paciente, related_name="emerg_pac_id", )
    emerg_doc_id:           ForeignKey = ForeignKey(Doctor, on_delete=models.SET_NULL, to_field="doc_id", null=True, name="emerg_doc_id")
    
    def __str__(self):
        return self.emerg_desc
    
    def total_pacientes(self) -> int:
        num_pacientes = Paciente.objects.filter(emerg_pac_id=self).count()
        return num_pacientes
    


# El modelo "Atencion" utilizara como modelo base a "Model" y estara asociado a un "Doctor" y a un "Paciente" ya que el doctor le dara un diagnóstico al paciente
class Atencion(Model):
    atenc_id:               AutoField = AutoField(primary_key=True)
    atenc_descripcion:      TextField = TextField(max_length=50)
    atenc_diagnostico:      TextField = TextField(max_length=50)
    atenc_fecha:            TextField = TextField(max_length=30, default=timezone.now)
    atenc_pac_id:           ForeignKey = ForeignKey(Paciente, on_delete=models.SET_NULL, to_field="pac_id", null=True, name="atenc_pac_id")
    atenc_doc_id:           ForeignKey = ForeignKey(Doctor, on_delete=models.SET_NULL, to_field="doc_id", null=True, name="atenc_doc_id")