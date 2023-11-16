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

from principal.models import Paciente
from principal.models import Emergencia
from principal.models import Administrador
from principal.models import Secretario
from principal.models import Doctor
from principal.models import Area
from principal.models import HoraDia, Horario, DiaSemana




# ============================================================
#   Generador de datos
# ============================================================
# Zona horaria UTC-3

random.seed(1337)
Faker.seed(1337)
fake = Faker("es_CL")

def generar_anio_nacimiento():
    return random.randint(1950, 2005)

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

DatosGenerador: GeneradorDatos = GeneradorDatos()


# ============================================================
#   Funciones varias
# ============================================================

GlobalPacientes: list = []
GlobalDoctores: list = []
GlobalHorarios: list = []
GlobalAreas: list = []
GlobalEmergencias: list = []

LenPacientes: int = 0
LenDoctores: int = 0
LenHorarios: int = 0
LenAreas: int = 0
LenEmergencias: int = 0


def GenerarDatosPacientes(Cantidad: int = 10) -> None:
    print(" > Generando datos de pacientes...                    ", end="")
    
    Fallo: bool = False
    FalloCantidad: int = 0
    FalloMensaje: str = ""

    Inicio: float = perf_counter()

    for id in range(Cantidad):
        try:
            Rut, Dv = DatosGenerador.Rut(Numeros=True)

            NewPaciente: Paciente = Paciente(
                rut     =   Rut,
                dv      =   Dv,
                primernombre    =   fake.first_name(),
                segundonombre   =   fake.first_name(),
                apellidopaterno =   fake.last_name(),
                apellidomaterno =   fake.last_name(),
                anio_nacimiento = generar_anio_nacimiento(),
                direccion = fake.street_address(),
                ciudad = fake.city(),
          
            )
            
            NewPaciente.save()
        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error

    global GlobalPacientes
    GlobalPacientes = list( Paciente.objects.all() )
    
    global LenPacientes
    LenPacientes = len(GlobalPacientes) - 1
    
    Termino: float = perf_counter()
    
    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")



def GenerarDoctores(Cantidad):
    print(" > Generando datos de doctores...                     ", end="")
    Fallo = False
    FalloCantidad = 0
    FalloMensaje = ""

    Inicio = perf_counter()
    for id in range(Cantidad):
        try:
            Rut, Dv = DatosGenerador.Rut(Numeros=True)
            pnombre = fake.first_name()
            snombre = fake.first_name()

            username = (pnombre[0:2] + "." + snombre + "." + str(Rut)[-4:]).lower()

            doctor = Doctor(
                rut     =   Rut,
                dv      =   Dv,
                primernombre    =   pnombre,
                segundonombre   =   snombre,
                apellidopaterno =   fake.last_name(),
                apellidomaterno =   fake.last_name(),
                anio_nacimiento = generar_anio_nacimiento(),
                direccion = fake.street_address(),
                ciudad = fake.city(),
                doc_cuentausuario   =   username,
                doc_cuentacontrasena=   DatosGenerador.Contrasena()
            )

            doctor.doc_area_id  =   GlobalAreas[ random.randint(0, LenAreas) ]
            doctor.doc_hor_id   =   GlobalHorarios[ random.randint(0, LenHorarios) ]
            doctor.save()

        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    
    global GlobalDoctores
    GlobalDoctores = list( Doctor.objects.all() )
    
    global LenDoctores
    LenDoctores = len(GlobalDoctores) - 1
    
    Termino = perf_counter()

    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")




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

def GenerarAdministradores(Cantidad: int = 10) -> None:
    print(" > Generando datos de administradores...              ", end="")
    
    Fallo: bool = False
    FalloCantidad: int = 0
    FalloMensaje: str = ""

    Inicio: float = perf_counter()
    
    try:
        administrador_principal = Administrador(
            rut     =   20000000,
            dv      =   0,
            primernombre    =   "Administrador",
            segundonombre   =   "Principal",
            apellidopaterno =   "Principal",
            apellidomaterno =   "Principal",
            adm_cuentausuario       =   "admin",
            adm_cuentacontrasena    =   make_password("admin")
        )
        administrador_principal.save()
    except Exception as Error:
        Fallo = True
        FalloCantidad += 1
        FalloMensaje = Error

    for id in range(Cantidad):
        
        try:
            Rut, Dv = DatosGenerador.Rut(Numeros=True)
            pnombre = fake.first_name()
            snombre = fake.first_name()
            
            username = (pnombre[0:2] + "." + snombre + "." + str(Rut)[-4:]).lower()
            
            # Crea una instancia de Administrador
            administrador = Administrador(
                rut     =   Rut,
                dv      =   Dv,
                primernombre    =   pnombre,
                segundonombre   =   snombre,
                apellidopaterno =   fake.last_name(),
                apellidomaterno =   fake.last_name(),
                anio_nacimiento = generar_anio_nacimiento(),
                direccion = fake.street_address(),
                ciudad = fake.city(),
                adm_cuentausuario       =   username,
                adm_cuentacontrasena    =   DatosGenerador.Contrasena()
            )
            
            # Encripta la contraseña ficticia antes de guardarla
            administrador.SetContrasena( DatosGenerador.Contrasena() )
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



def GenerarSecretarios(Cantidad):
    print(" > Generando datos de Secretarios...                  ", end="")
    Fallo: bool = False
    FalloCantidad: int = 0
    FalloMensaje: str = ""

    Inicio: float = perf_counter()
    for id in range(Cantidad):
        
        try: 
            Rut, Dv = DatosGenerador.Rut(Numeros=True)
            pnombre = fake.first_name()
            snombre = fake.first_name()
            
            username = (pnombre[0:2] + "." + snombre + "." + str(Rut)[-4:]).lower()
            
            secretario = Secretario(
                rut     =   Rut,
                dv      =   Dv,
                primernombre    =   pnombre,
                segundonombre   =   snombre,
                apellidopaterno =   fake.last_name(),
                apellidomaterno =   fake.last_name(),
                anio_nacimiento = generar_anio_nacimiento(),
                direccion = fake.street_address(),
                ciudad = fake.city(),
                sec_cuentausuario   =   username,
                sec_cuentacontrasena =  DatosGenerador.Contrasena()
            )
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



def GenerarHorasDias(Cantidad: int = 10) -> None:
    print(" > Generando datos de horas del día...                ", end="")
    
    Fallo: bool = False
    FalloCantidad: int = 0
    FalloMensaje: str = ""

    Inicio: float = perf_counter()

    for id in range(Cantidad):

        try:
            # Genera horas de inicio y fin ficticias que inicien exactamente en la hora, por ejemplo 08:00:00, 13:00:00, 17:00:00, etc.
            # hora_inicio_ficticia = fake.time_object(end_datetime=None)
            hora_inicio_ficticia = fake.time_object().replace(minute=0, second=0)
            
            # Añade entre 8 a 12 horas a la hora de inicio
            hora_fin_ficticia = datetime.combine(datetime.today(), hora_inicio_ficticia) + timedelta(hours=random.randint(8, 12))
            
            # Crea una instancia de HoraDia
            hora_dia = HoraDia(
                hordia_inicio   =   hora_inicio_ficticia,
                hordia_fin      =   hora_fin_ficticia
            )
            hora_dia.save()
            
        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    
    Termino: float = perf_counter()
    
    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")




def GenerarDiasSemana() -> None:
    print(" > Generando datos de días de la semana...            ", end="")
    
    Fallo: bool = False
    FalloCantidad: int = 0
    FalloMensaje: str = ""

    Inicio: float = perf_counter()
    
    for dia in DiasSemana:
        try:
            dia_semana = DiaSemana(sem_nombre = dia)
            dia_semana.save()
        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    
    Termino: float = perf_counter()
    
    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")




def GenerarHorarios(Cantidad: int = 10) -> None:
    print(" > Generando datos de horarios...                     ", end="")
    
    Fallo: bool = False
    FalloCantidad: int = 0
    FalloMensaje: str = ""

    Inicio: float = perf_counter()

    for id in range(Cantidad):

        try:
            dia_semana_ficticio = DiaSemana.objects.order_by("?").first()
            dia_hora_ficticio = HoraDia.objects.order_by("?").first()
            
            # Crea una instancia de Horario
            horario = Horario()
            horario.hor_sem_id = dia_semana_ficticio
            horario.hor_horadia_id = dia_hora_ficticio
            horario.save()
        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    
    global GlobalHorarios
    GlobalHorarios = list( Horario.objects.all() )
    
    global LenHorarios
    LenHorarios = len(GlobalHorarios) - 1
    
    Termino: float = perf_counter()
    
    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")




def GenerarAreas(Cantidad: int = 10) -> None:
    print(" > Generando datos de áreas...                        ", end="")
    
    Fallo: bool = False
    FalloCantidad: int = 0
    FalloMensaje: str = ""

    Inicio: float = perf_counter()

    for area in AreasLista:
        try:
            # Crea una instancia de Area
            area = Area(
                area_nombre = area,
            )
            area.save()
        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    
    global GlobalAreas
    GlobalAreas = list( Area.objects.all() )
    
    global LenAreas
    LenAreas = len(GlobalAreas) - 1
    
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

if True:
    # Valores fijos
    GenerarDiasSemana()
    GenerarAreas()

    # Valores ficticios
    GenerarHorasDias(100)
    GenerarHorarios(20)

    GenerarDatosPacientes(1000)
    GenerarDoctores(500)
    GenerarEmergencias(3000)

    # Extra
    GenerarAdministradores(10)
    GenerarSecretarios(20)
else:
    PacienteRandom: int = fake.random.randint(0, Paciente.objects.values("pac_id").count())
    
    print( Paciente.objects.values("pac_id")[PacienteRandom]["pac_id"] )

Termino: float = perf_counter()

print(f"Tarea completada en {round(Termino - Inicio, 2)}s")

print("=====================================")