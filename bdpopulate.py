
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codigotrauma.settings")
django.setup()


from principal.models import Paciente

from faker import Faker
fake = Faker()


def crear_pacientes_falsos(cantidad):
    for _ in range(cantidad):
        paciente = Paciente(
            Rut=fake.random_int(min=1000000, max=9999999),  # Ejemplo de generación de un número aleatorio
            Dv=fake.random_element(elements=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'K']),
            PrimerNombre=fake.first_name(),
            SegundoNombre=fake.first_name(),
            ApellidoPaterno=fake.last_name(),
            ApellidoMaterno=fake.last_name(),
        )
        paciente.save()

crear_pacientes_falsos(100)  


