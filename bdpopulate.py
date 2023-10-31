# ============================================================
#   Librerias
# ============================================================

import os
import django
from django.contrib.auth.hashers import make_password
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codigotrauma.settings")
django.setup()


from principal.models import Paciente, RegistroEmergencias, HistorialEmergencias, Administrador, Secretario, DoctorClave, HistorialDoctoresEmergencia


from principal.models import Paciente

# ============================================================
#   Generador de datos
# ============================================================

Faker.seed(1337)
fake = Faker("es_CL")


def crear_pacientes_falsos(cantidad):
    for _ in range(cantidad):
        RUN: str = fake.person_rut()
        
        rut: str = int( RUN.split("-")[0].replace(".", "") )
        dv: str = RUN.split("-")[1]
        
        paciente = Paciente(
            Rut     =   rut,
            Dv      =   dv,
            PrimerNombre    =   fake.first_name(),
            SegundoNombre   =   fake.first_name(),
            ApellidoPaterno =   fake.last_name(),
            ApellidoMaterno =   fake.last_name(),
        )
        paciente.save()

crear_pacientes_falsos(100)  


def crear_registros_emergencias_falsos(cantidad):
    for _ in range(cantidad):
        # Genera un ID ficticio (puedes ajustarlo según tus necesidades)
        id_ficticio = fake.unique.random_number(digits=8)
        
        # Genera una descripción ficticia
        descripcion_ficticia = fake.text(max_nb_chars=50)
        
        # Genera un código de color ficticio
        codigo_color_ficticio = fake.color_name()
        
        # Genera una fecha ficticia
        fecha_ficticia = fake.date_time_between(start_date="-1y", end_date="now")
        
        # Genera un número de pacientes ficticio
        numero_pacientes_ficticio = fake.random_int(min=1, max=100)
        
        # Crea una instancia de RegistroEmergencias
        registro_emergencias = RegistroEmergencias(
            ID=str(id_ficticio),
            Descripcion=descripcion_ficticia,
            CodigoColor=codigo_color_ficticio,
            Fecha=fecha_ficticia,
            NumeroPacientes=numero_pacientes_ficticio,
        )
        registro_emergencias.save()

crear_registros_emergencias_falsos(100)  

def crear_historiales_emergencias_falsos(cantidad):
    for _ in range(cantidad):
        # Genera una fecha de registro ficticia
        fecha_registro_ficticia = fake.date_time_between(start_date="-1y", end_date="now")
        
        # Genera detalles ficticios
        detalles_ficticios = fake.text(max_nb_chars=200)
        
        # Selecciona una emergencia aleatoria
        emergencia_aleatoria = RegistroEmergencias.objects.order_by("?").first()

        # Crea una instancia de HistorialEmergencias
        historial_emergencias = HistorialEmergencias(
            Emergencia=emergencia_aleatoria,
            FechaRegistro=fecha_registro_ficticia,
            Detalles=detalles_ficticios,
        )
        historial_emergencias.save()

crear_historiales_emergencias_falsos(100)

def crear_administradores_falsos(cantidad):
    for _ in range(cantidad):
        # Genera un nombre de usuario ficticio
        nombre_usuario_ficticio = fake.user_name()
        
        # Genera una contraseña ficticia
        contrasena_ficticia = fake.password()
        
        # Crea una instancia de Administrador
        administrador = Administrador(
            CuentaUsuario=nombre_usuario_ficticio,
        )
        
        # Encripta la contraseña ficticia antes de guardarla
        administrador.SetContrasena(contrasena_ficticia)
        
        administrador.save()

crear_administradores_falsos(100)

def crear_doctoresclave_falsos(cantidad):
    