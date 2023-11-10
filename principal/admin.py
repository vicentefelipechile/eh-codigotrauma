from django.contrib import admin
from .models import Administrador, DiaSemana, Doctor, HistorialDoctorEmergencia, HistorialEmergencia, HoraDia, Horario, Paciente, Emergencia, Secretario

# Register your models here.
admin.site.register(Administrador)
admin.site.register(DiaSemana)
admin.site.register(Doctor)
admin.site.register(HistorialDoctorEmergencia)
admin.site.register(HistorialEmergencia)
admin.site.register(HoraDia)
admin.site.register(Horario)
admin.site.register(Paciente)
admin.site.register(Emergencia)
admin.site.register(Secretario)