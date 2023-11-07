# ============================================================
#   Librerias
# ============================================================

import os
import random
import django
from time import perf_counter
from django.contrib.auth.hashers import make_password
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codigotrauma.settings")
django.setup()


from principal.models import Paciente
from principal.models import RegistroEmergencias
from principal.models import HistorialEmergencias
from principal.models import Administrador
from principal.models import Secretario
from principal.models import DoctorClave
from principal.models import HistorialDoctoresEmergencia
from principal.models import Area
from principal.models import HoraDia, Horario, DiaSemana



# ============================================================
#   Generador de datos
# ============================================================
# Zona horaria UTC-3

Faker.seed(1337)
fake = Faker("es_CL")


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


# ============================================================
#   Funciones varias
# ============================================================


def GenerarDatosPacientes(Cantidad: int = 10) -> None:
    print(" > Generando datos de pacientes...                    ", end="")
    
    Fallo: bool = False
    FalloCantidad: int = 0
    FalloMensaje: str = ""

    Inicio: float = perf_counter()

    for id in range(Cantidad):
        try:
            Rut, Dv = GeneradorDatos().Rut(Numeros=True)

            NewPaciente: Paciente = Paciente(
                Rut     =   Rut,
                Dv      =   Dv,
                PrimerNombre    =   fake.first_name(),
                SegundoNombre   =   fake.first_name(),
                ApellidoPaterno =   fake.last_name(),
                ApellidoMaterno =   fake.last_name(),
            )
            
            NewPaciente.save()
        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    
    Termino: float = perf_counter()
    
    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")




def GenerarRegistrosEmergencias(Cantidad: int = 10) -> None:
    print(" > Generando datos de registros de emergencias...     ", end="")
    
    Fallo: bool = False
    FalloCantidad: int = 0
    FalloMensaje: str = ""

    Inicio: float = perf_counter()

    for id in range(Cantidad):
        colores_disponibles = ["Rojo", "Amarillo", "Verde", "Negro", "Blanco"]
            
        try:
            # Crea una instancia de RegistroEmergencias
            Registro = RegistroEmergencias(
                ID          =       GeneradorDatos().UniqueID(),
                Descripcion =       fake.text(max_nb_chars=50),
                CodigoColor =       random.choice(colores_disponibles),
                Fecha       =       GeneradorDatos().Fecha(),
                NumeroPacientes =   fake.random_int(min=1, max=100),
            )
            Registro.save()
        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    
    Termino: float = perf_counter()
    
    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")



def GenerarHistorialEmergencias(Cantidad: int = 10) -> None:
    print(" > Generando datos de historial de emergencias...     ", end="")
    
    Fallo: bool = False
    FalloCantidad: int = 0
    FalloMensaje: str = ""

    Inicio: float = perf_counter()

    for id in range(Cantidad):

        try:
            # Crea una instancia de HistorialEmergencias
            historial_emergencias = HistorialEmergencias(
                Emergencia      =   RegistroEmergencias.objects.order_by("?").first(),
                FechaRegistro   =   GeneradorDatos().Fecha(),
                Detalles        =   fake.text(max_nb_chars=200)
            )

            historial_emergencias.save()
        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    
    Termino: float = perf_counter()
    
    if Fallo:
        print(f"ERROR ({FalloCantidad} fallos) - {FalloMensaje}")
    else:
        print(f"OK ({round(Termino - Inicio, 2)}s)")

def GenerarHistorialDoctoresClave(Cantidad: int = 10) -> None:
    print(" > Generando datos de historial de doctores clave...  ", end="")
    
    Fallo: bool = False
    FalloCantidad: int = 0
    FalloMensaje: str = ""

    Inicio: float = perf_counter()

    for id in range(Cantidad):

        try:
            # Crea una instancia de HistorialEmergencias
            historial_doctores = HistorialDoctoresEmergencia(
                Emergencia      =   RegistroEmergencias.objects.order_by("?").first(),
                Doctor          =   DoctorClave.objects.order_by("?").first(),
                FechaAsignacion =   GeneradorDatos().Fecha(),
            )

            historial_doctores.save()
        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    
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

    for id in range(Cantidad):
        
        try:
            Rut, Dv = GeneradorDatos().Rut(Numeros=True)
            
            # Crea una instancia de Administrador
            administrador = Administrador(
                Rut     =   Rut,
                Dv      =   Dv,
                PrimerNombre    =   fake.first_name(),
                SegundoNombre   =   fake.first_name(),
                ApellidoPaterno =   fake.last_name(),
                ApellidoMaterno =   fake.last_name(),
                CuentaUsuario = fake.user_name()
            )
            
            # Encripta la contraseña ficticia antes de guardarla
            administrador.SetContrasena(fake.password())
            administrador.save()
        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    
    try:
        administrador_principal = Administrador(
            Rut     =   20000000,
            Dv      =   0,
            PrimerNombre    =   "Administrador",
            SegundoNombre   =   "Principal",
            ApellidoPaterno =   "Principal",
            ApellidoMaterno =   "Principal",
            CuentaUsuario   =   "admin"
        )
        
        administrador_principal.SetContrasena("password")
        administrador_principal.save()
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
            Rut, Dv = GeneradorDatos().Rut(Numeros=True)
            secretario = Secretario(
                Rut     =   Rut,
                Dv      =   Dv,
                PrimerNombre    =   fake.first_name(),
                SegundoNombre   =   fake.first_name(),
                ApellidoPaterno =   fake.last_name(),
                ApellidoMaterno =   fake.last_name(),
                CuentaUsuario = fake.user_name()
            )
            secretario.SetContrasena(fake.password())
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
        
        
def GenerarDoctoresClave(Cantidad):
    print(" > Generando datos DoctoresClave...                   ", end="")
    Fallo = False
    FalloCantidad = 0
    FalloMensaje = ""

    Inicio = perf_counter()
    for id in range(Cantidad):
        nombre_area_ficticio = fake.word(ext_word_list=["Cardiología", "Dermatología", "Ginecología", "Neurología", "Ortopedia"])
        try:
            Rut, Dv = GeneradorDatos().Rut(Numeros=True)
            doctorclave = DoctorClave(
                Rut=Rut,
                Dv=Dv,
                PrimerNombre=fake.first_name(),
                SegundoNombre=fake.first_name(),
                ApellidoPaterno=fake.last_name(),
                ApellidoMaterno=fake.last_name(),
                Area=nombre_area_ficticio,
                CuentaUsuario=fake.user_name()
            )
            doctorclave.SetContrasena(fake.password())
            horario_aleatorio = Horario.objects.order_by("?").first()
            doctorclave.Horario = horario_aleatorio
            doctorclave.save()
        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    Termino = perf_counter()

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
            # Genera horas de inicio y fin ficticias
            hora_inicio_ficticia = fake.time_object(end_datetime=None)
            
            # Asegura que la hora de fin sea posterior a la hora de inicio
            hora_fin_ficticia = fake.time_object(end_datetime=None)
            while hora_fin_ficticia <= hora_inicio_ficticia:
                hora_fin_ficticia = fake.time_object(end_datetime=None)
            
            # Crea una instancia de HoraDia
            hora_dia = HoraDia(
                HoraInicio=hora_inicio_ficticia,
                HoraFin=hora_fin_ficticia,
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
    
    Semanas: list[str] = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    
    for dia in Semanas:
        try:
            dia_semana = DiaSemana(Nombre=dia)
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
            # Genera una referencia ficticia a un día de la semana
            dia_semana_ficticio = DiaSemana.objects.order_by("?").first()
            
            # Genera una referencia ficticia a una hora del día
            dia_hora_ficticio = HoraDia.objects.order_by("?").first()
            
            # Genera una descripción de clase ficticia
            
            # Crea una instancia de Horario
            horario = Horario(
                DiaSemana=dia_semana_ficticio,
                DiaHora=dia_hora_ficticio,
                
            )
            horario.save()
        except Exception as Error:
            Fallo = True
            FalloCantidad += 1
            FalloMensaje = Error
    
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

    for id in range(Cantidad):
        try:
            # Genera un nombre de área ficticio
            nombre_area_ficticio = fake.word(ext_word_list=["Cardiología", "Dermatología", "Ginecología", "Neurología", "Ortopedia"])
            
            # Crea una instancia de Area
            area = Area(
                Nombre=nombre_area_ficticio,
            )
            area.save()
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
#   Ejecución
# ============================================================

print("=====================================")
print("     Generacion de datos falsos")
print("=====================================")

Inicio: float = perf_counter()

GenerarDatosPacientes(100)
GenerarAdministradores(100)
GenerarDoctoresClave(100)
GenerarSecretarios(100)
GenerarRegistrosEmergencias(100)
GenerarHistorialEmergencias(100)
GenerarHorasDias(100)
GenerarDiasSemana()
GenerarHorarios(100)
GenerarAreas(100)
GenerarHistorialDoctoresClave(100)

Termino: float = perf_counter()

print(f"Tarea completada en {round(Termino - Inicio, 2)}s")

print("=====================================")