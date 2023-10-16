from django.contrib import admin
from .models import Administrador, DiaSemana, DoctorClave, HistorialDoctoresEmergencia, HistorialEmergencias, HoraDia, Horario, Paciente, RegistroEmergencias, Secretario

# Register your models here.
admin.site.register(Administrador)
admin.site.register(DiaSemana)
admin.site.register(DoctorClave)
admin.site.register(HistorialDoctoresEmergencia)
admin.site.register(HistorialEmergencias)
admin.site.register(HoraDia)
admin.site.register(Horario)
admin.site.register(Paciente)
admin.site.register(RegistroEmergencias)
admin.site.register(Secretario)