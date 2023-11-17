# ============================================================
#   Librerias
# ============================================================

import os, random, django
from time import perf_counter
from faker import Faker
from datetime import datetime, timedelta
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codigotrauma.settings")
django.setup()


from django.contrib.auth.hashers import make_password

# Modelos Varios
from principal.models import Area
from principal.models import HoraDia
from principal.models import DiaSemana
from principal.models import Horario

# Modelos Base
# from principal.models import Usuario
# from principal.models import Persona

# Modelos Personas
from principal.models import Paciente
from principal.models import Doctor
from principal.models import Secretario
from principal.models import Administrador

# Modelos Registros
from principal.models import Emergencia
from principal.models import Atencion




# ============================================================
#   Generador de datos
# ============================================================
# Zona horaria UTC-3

random.seed(1337)
Faker.seed(1337)
fake = Faker("es_CL")

colores_disponibles = ["Rojo", "Amarillo", "Verde", "Negro", "Blanco"]

AreasLista: list[str] = ["Cardiología", "Dermatología", "Ginecología", "Neurología", "Ortopedia"]
DiasSemana: list[str] = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

# ============================================================
#   Funciones varias
# ============================================================

class GeneradorDatos:
    def Rut(self, Numeros: bool = False) -> str | int:
        RUN: str = fake.person_rut()
        
        rut: str | int = int( RUN.split("-")[0].replace(".", "") ) if Numeros else RUN.split("-")[0]
        dv: str = RUN.split("-")[1]
        
        return rut, dv

    def Fecha(self, Inicio: str = "-1y") -> str:
        return fake.date_time_between(start_date=Inicio, end_date="now").strftime("%Y-%m-%d %H:%M:%S")
    
    def UniqueID(self, Digitos: int = 8) -> str:
        return str( fake.unique.random_number(digits=Digitos) )
    
    def Contrasena(self, UsarFaker: bool = False) -> str:
        return make_password( fake.password() if UsarFaker else "password" )
    
    def AnioNacimiento(self) -> int:
        return random.randint(1950, 2005)

DatosGenerador: GeneradorDatos = GeneradorDatos()

# ===========================================
# ============ Variables Globales ===========
# ===========================================

LenPacientes:       int = 0
LenDoctores:        int = 0
LenAreas:           int = 0
LenEmergencias:     int = 0
LenHorarios:        int = 0
LenDiaSemana:       int = 0
LenHoraDia:         int = 0



# ===========================================
# ============== Modelos Varios =============
# ===========================================

# Area
def GenerarArea() -> None:
    print(" > Generando datos de áreas...                        ", end="")
    
    Fallo:          bool    = False
    FalloCantidad:  int     = 0
    FalloMensaje:   str     = ""

    Inicio: float = perf_counter()

    for area in AreasLista:
        try:
            area                    = Area()
            area.area_nombre        = area
            area.save()

        except Exception as Error:
            Fallo                   = True
            FalloCantidad           += 1
            FalloMensaje            = Error

    global LenAreas
    LenAreas = Area.objects.all().count()
    
    Termino: float = perf_counter()
    
    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")


# HoraDia
def GenerarHoraDia(Cantidad: int = 10) -> None:
    print(" > Generando datos de horas del día...                ", end="")
    
    Fallo:          bool    = False
    FalloCantidad:  int     = 0
    FalloMensaje:   str     = ""

    Inicio: float = perf_counter()

    for id in range(Cantidad):

        try:
            hora_inicio_ficticia    = fake.time_object().replace(minute=0, second=0)
            hora_fin_ficticia       = datetime.combine(datetime.today(), hora_inicio_ficticia) + timedelta(hours=random.randint(8, 10))
            
            # Crea una instancia de HoraDia
            hora_dia = HoraDia()
            hora_dia.hordia_inicio  = hora_inicio_ficticia
            hora_dia.hordia_fin     = hora_fin_ficticia
            hora_dia.save()
            
        except Exception as Error:
            Fallo                   = True
            FalloCantidad           += 1
            FalloMensaje            = Error
    
    global LenHoraDia
    LenHoraDia = HoraDia.objects.all().count()
    
    Termino: float = perf_counter()
    
    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")


# DiaSemana
def GenerarDiaSemana() -> None:
    print(" > Generando datos de días de la semana...            ", end="")

    Inicio: float = perf_counter()
    
    for dia in DiasSemana:
        diasemana = DiaSemana()
        diasemana.diasem_nombre = dia
        diasemana.save()
    
    global LenDiaSemana
    LenDiaSemana = DiaSemana.objects.all().count()
    
    Termino: float = perf_counter()
    
    print(f"OK ({round(Termino - Inicio, 2)}s)")


# Horario
def GenerarHorario(Cantidad: int = 10) -> None:
    print(" > Generando datos de horarios...                     ", end="")
    
    Fallo:          bool    = False
    FalloCantidad:  int     = 0
    FalloMensaje:   str     = ""

    Inicio: float = perf_counter()

    for id in range(Cantidad):
        try:
            
            # Crea una instancia de Horario
            horario = Horario()
            horario.horario_dia     = DiaSemana.objects.get( diasem_id=random.randint(1, LenDiaSemana) )
            horario.horario_hora    = HoraDia.objects.get( hordia_id=random.randint(1, LenHoraDia) )
            horario.save()

        except Exception as Error:
            Fallo                   = True
            FalloCantidad           += 1
            FalloMensaje            = Error

    global LenHorarios
    LenHorarios = Horario.objects.all().count()
    
    Termino: float = perf_counter()
    
    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")



# ===========================================
# ============= Modelos Personas ============
# ===========================================

# Paciente
def GenerarPacientes(Cantidad: int = 10) -> None:
    print(" > Generando datos de pacientes...                    ", end="")
    
    Fallo:              bool    = False
    FalloCantidad:      int     = 0
    FalloMensaje:       str     = ""

    Inicio: float = perf_counter()

    for id in range(Cantidad):
        try:
            Rut, Dv = DatosGenerador.Rut(Numeros=True)

            paciente: Paciente = Paciente()
            paciente.pac_rut                    = Rut
            paciente.pac_dv                     = Dv
            paciente.pac_primernombre           = fake.first_name()
            paciente.pac_segundonombre          = fake.first_name()
            paciente.pac_apellidopaterno        = fake.last_name()
            paciente.pac_apellidomaterno        = fake.last_name()
            paciente.pac_nacimiento             = DatosGenerador.AnioNacimiento()
            paciente.pac_direccion              = fake.street_address()
            paciente.pac_ciudad                 = fake.city()
            paciente.pac_estado                 = fake.city()
            paciente.pac_codigopostal           = fake.postcode()
            
            paciente.save()
        except Exception as Error:
            Fallo                               = True
            FalloCantidad                       += 1
            FalloMensaje                        = Error
    
    global LenPacientes
    LenPacientes = Paciente.objects.all().count()
    
    Termino: float = perf_counter()
    
    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")


# Doctor
def GenerarDoctores(Cantidad: int = 10) -> None:
    print(" > Generando datos de doctores...                     ", end="")
    
    Fallo:              bool    = False
    FalloCantidad:      int     = 0
    FalloMensaje:       str     = ""

    Inicio = perf_counter()
    for id in range(Cantidad):
        try:
            Rut, Dv = DatosGenerador.Rut(Numeros=True)
            pnombre = fake.first_name()
            snombre = fake.first_name()

            username = (pnombre[0:2] + "." + snombre + "." + str(Rut)[-4:]).lower()

            doctor = Doctor()
            doctor.pers_rut                 = Rut
            doctor.pers_dv                  = Dv
            doctor.pers_primernombre        = pnombre
            doctor.pers_segundonombre       = snombre
            doctor.pers_apellidopaterno     = fake.last_name()
            doctor.pers_apellidomaterno     = fake.last_name()
            doctor.pers_nacimiento          = DatosGenerador.AnioNacimiento()
            doctor.pers_direccion           = fake.street_address()
            doctor.pers_ciudad              = fake.city()

            doctor.user_name                = username
            doctor.user_password            = DatosGenerador.Contrasena()
            doctor.doc_area                 = Area.objects.get(area_id=random.randint(1, LenAreas))
            doctor.doc_horario              = Horario.objects.get(horario_id=random.randint(1, LenHorarios))
            doctor.save()

        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    
    global LenDoctores
    LenDoctores = Doctor.objects.all().count()
    
    Termino = perf_counter()

    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")


# Secretario
def GenerarSecretarios(Cantidad: int = 10) -> None:
    print(" > Generando datos de secretarios...                  ", end="")
    
    Fallo:              bool    = False
    FalloCantidad:      int     = 0
    FalloMensaje:       str     = ""

    Inicio: float = perf_counter()
    for id in range(Cantidad):
        try:
            Rut, Dv = DatosGenerador.Rut(Numeros=True)
            pnombre = fake.first_name()
            snombre = fake.first_name()

            username = (pnombre[0:2] + "." + snombre + "." + str(Rut)[-4:]).lower()

            secretario = Secretario()
            secretario.pers_rut                 = Rut
            secretario.pers_dv                  = Dv
            secretario.pers_primernombre        = pnombre
            secretario.pers_segundonombre       = snombre
            secretario.pers_apellidopaterno     = fake.last_name()
            secretario.pers_apellidomaterno     = fake.last_name()
            secretario.pers_nacimiento          = DatosGenerador.AnioNacimiento()
            secretario.pers_direccion           = fake.street_address()
            secretario.pers_ciudad              = fake.city()

            secretario.user_name                = username
            secretario.user_password            = DatosGenerador.Contrasena()
            secretario.save()

        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    
    Termino: float = perf_counter()

    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")


# Administrador
def GenerarAdministradores(Cantidad: int = 10) -> None:
    print(" > Generando datos de administradores...              ", end="")
    
    Fallo:              bool    = False
    FalloCantidad:      int     = 0
    FalloMensaje:       str     = ""

    Inicio: float = perf_counter()
    for id in range(Cantidad):
        try:
            Rut, Dv = DatosGenerador.Rut(Numeros=True)
            pnombre = fake.first_name()
            snombre = fake.first_name()

            username = (pnombre[0:2] + "." + snombre + "." + str(Rut)[-4:]).lower()

            administrador = Administrador()
            administrador.pers_rut                 = Rut
            administrador.pers_dv                  = Dv
            administrador.pers_primernombre        = pnombre
            administrador.pers_segundonombre       = snombre
            administrador.pers_apellidopaterno     = fake.last_name()
            administrador.pers_apellidomaterno     = fake.last_name()
            administrador.pers_nacimiento          = DatosGenerador.AnioNacimiento()
            administrador.pers_direccion           = fake.street_address()
            administrador.pers_ciudad              = fake.city()

            administrador.user_name                = username
            administrador.user_password            = DatosGenerador.Contrasena()
            administrador.save()

        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    
    Termino: float = perf_counter()

    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")


# ============================================================
#   Funciones varias
# ============================================================








def GenerarEmergencias(Cantidad: int = 10) -> None:
    print(" > Generando datos de registros de emergencias...     ", end="")
    
    Fallo: bool = False
    FalloCantidad: int = 0
    FalloMensaje: str = ""

    Inicio: float = perf_counter()

    for id in range(Cantidad):
            
        try:            
            # Crea una instancia de Emergencia
            Registro = Emergencia(
                emerg_desc      =       fake.text(max_nb_chars=50),
                emerg_color     =       random.choice(colores_disponibles),
                emerg_fecha     =       DatosGenerador.Fecha()
            )
            
            Registro.emerg_pac_id = GlobalPacientes[ random.randint(0, LenPacientes) ]
            Registro.emerg_doc_id = GlobalDoctores[ random.randint(0, LenDoctores) ]
            
            Registro.save()
        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    
    global GlobalEmergencias
    GlobalEmergencias = list( Emergencia.objects.all() )
    
    global LenEmergencias
    LenEmergencias = len(GlobalEmergencias) - 1
    
    Termino: float = perf_counter()
    
    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")








def GenerarAtencionesPacientes(Cantidad: int = 10) -> None:
    print(" > Generando datos de atenciones a pacientes...      ", end="")
    
    Fallo: bool = False
    FalloCantidad: int = 0
    FalloMensaje: str = ""

    Inicio: float = perf_counter()

    for _ in range(Cantidad):
        try:            
            # Crea una instancia de Atencion
            atencion = Atencion(
                atenc_descripcion = fake.text(max_nb_chars=50),
                atenc_diagnostico = fake.sentence(nb_words=20)
            )
            
            # Asigna un paciente y un doctor aleatorio
            atencion.atenc_pac_id = GlobalPacientes[random.randint(0, LenPacientes)]
            atencion.atenc_doc_id = GlobalDoctores[random.randint(0, LenDoctores)]
            
            atencion.save()
        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    
    global GlobalAtenciones
    GlobalAtenciones = list(Atencion.objects.all())
    
    global LenAtenciones
    LenAtenciones = len(GlobalAtenciones) - 1
    
    Termino: float = perf_counter()
    
    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")

    
    
# ============================================================
#   Ejecución
# ============================================================

print("=====================================")
print("     Generacion de datos falsos")
print("=====================================")

Inicio: float = perf_counter()

# Modelos Varios
GenerarArea()
GenerarHoraDia(100)
GenerarDiaSemana()
GenerarHorario(50)

# Modelos Personas
GenerarPacientes(100)
GenerarDoctores(40)
GenerarSecretarios(10)
GenerarAdministradores(5)

Termino: float = perf_counter()

print(f"Tarea completada en {round(Termino - Inicio, 2)}s")

print("=====================================")