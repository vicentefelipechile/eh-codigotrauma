# ============================================================
#   Librerias
# ============================================================

import os
import django
from faker import Faker
from faker import providers

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codigotrauma.settings")
django.setup()

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


