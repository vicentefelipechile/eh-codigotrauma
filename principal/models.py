# ====================================================
# ================ Librerias y Clases ================
# ====================================================

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Permission

from django.utils import timezone
from django.db import models
from django.db.models import Model

from django.db.models import TextField, IntegerField, CharField, AutoField, TimeField, BooleanField
from django.db.models import ForeignKey

from .sms import send_sms



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

# Utilizado como Base para la administracion de usuarios y contraseñas en el sistema, con esto se puede mantener un listado de usuarios y el rol que tienen (Paciente, Doctor, Secretario, Administrador)
class Usuario(Model):
    user_name:              CharField = CharField(max_length=30, unique=True)
    user_password:          CharField = CharField(max_length=128)
    
    # ===== CRUD =====
    def crear_usuario(self) -> None:
        self.save()
    
    def borrado_usuario(self) -> None:
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
    pers_direccion:         TextField = TextField()
    pers_ciudad:            TextField = TextField()
    pers_estado:            TextField = TextField()
    pers_codigopostal:      IntegerField = IntegerField(null=True)
    
    class Meta:
        abstract = True



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


# El modelo "Doctor" utiliza como base a "Persona" debido a que es un usuario recurrente en el sistema
class Doctor(Persona):
    doc_id:                 AutoField = AutoField(primary_key=True)
    doc_especialidad:       TextField = TextField(max_length=30)
    doc_area:               ForeignKey = ForeignKey(Area, on_delete=models.SET_NULL, to_field="area_id", null=True, name="doc_area")
    doc_horario:            ForeignKey = ForeignKey(Horario, on_delete=models.SET_NULL, to_field="horario_id", null=True, name="doc_horario")



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
    emerg_pac_id:           ForeignKey = ForeignKey(Paciente, on_delete=models.SET_NULL, to_field="pac_id", null=True, name="emerg_pac_id")
    emerg_doc_id:           ForeignKey = ForeignKey(Doctor, on_delete=models.SET_NULL, to_field="doc_id", null=True, name="emerg_doc_id")


# El modelo "Atencion" utilizara como modelo base a "Model" y estara asociado a un "Doctor" y a un "Paciente" ya que el doctor le dara un diagnóstico al paciente
class Atencion(Model):
    atenc_id:               AutoField = AutoField(primary_key=True)
    atenc_descripcion:      TextField = TextField(max_length=50)
    atenc_diagnostico:      TextField = TextField(max_length=50)
    atenc_fecha:            TextField = TextField(max_length=30, default=timezone.now)
    atenc_pac_id:           ForeignKey = ForeignKey(Paciente, on_delete=models.SET_NULL, to_field="pac_id", null=True, name="atenc_pac_id")
    atenc_doc_id:           ForeignKey = ForeignKey(Doctor, on_delete=models.SET_NULL, to_field="doc_id", null=True, name="atenc_doc_id")