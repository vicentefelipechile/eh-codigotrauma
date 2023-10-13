from django.db import models

class HistorialEmergencias(models.Model):
    emergencia = models.ForeignKey('RegistroEmergencias', on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField()
    detalles = models.TextField()

    def __str__(self):
        return f"Historial de Emergencia: {self.emergencia}, Fecha de Registro: {self.fecha_registro}"

class RegistroEmergencias(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    descripcion = models.TextField(max_length=50)
    codigoColor = models.TextField(max_length=20)
    fecha = models.DateTimeField(max_length=30)
    nro_pacientes = models.IntegerField()
    doctores = models.ManyToManyField('doctorClave', through='HistorialDoctoresEmergencia')

    def __str__(self):
        return self.id
    
class Paciente(models.Model):
    rut = models.IntegerField(primary_key=True, max_length=8)
    dv = models.CharField(max_length=1)
    nombre = models.TextField(max_length=20)
    seg_nombre = models.TextField(max_length=20)
    apellido = models.TextField(max_length=20)
    seg_apellido = models.TextField(max_length=20)

    def __str__(self):
        return str(self.rut)

class HistorialDoctoresEmergencia(models.Model):
    emergencia = models.ForeignKey('RegistroEmergencias', on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey('DoctorClave', on_delete=models.SET_NULL, null=True)
    fecha_asignacion = models.DateTimeField()

    def __str__(self):
        return f"Historial - Emergencia: {self.emergencia}, Doctor: {self.doctor}, Fecha: {self.fecha_asignacion}"

class Secretario(models.Model):
    rut = models.IntegerField(primary_key=True, max_length=8)
    dv = models.CharField(max_length=1)
    nombre = models.TextField(max_length=20)
    seg_nombre = models.TextField(max_length=20)
    apellido = models.TextField(max_length=20)
    seg_apellido = models.TextField(max_length=20)

class Administrador(models.Model):
    rut = models.IntegerField(primary_key=True, max_length=8)
    dv = models.CharField(max_length=1)
    nombre = models.TextField(max_length=20)
    seg_nombre = models.TextField(max_length=20)
    apellido = models.TextField(max_length=20)
    seg_apellido = models.TextField(max_length=20)

# Creamos las clases pertinentes para formar un horario

class Horario(models.Model):
    dia = models.ForeignKey('DiaSemana', on_delete=models.SET_NULL, null=True)
    hora = models.ForeignKey('HoraDia',on_delete=models.SET_NULL, null=True)
    clase = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.dia.nombre} - {str(self.hora)}: {self.clase}"

class DiaSemana(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class HoraDia(models.Model):
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')}"

# Creamos la clase "doctorClave" y la asociamos a la clase horario.

class DoctorClave(models.Model):
    rut = models.IntegerField(primary_key=True, max_length=8)
    dv = models.CharField(max_length=1)
    nombre = models.TextField(max_length=20)
    seg_nombre = models.TextField(max_length=20)
    apellido = models.TextField(max_length=20)
    seg_apellido = models.TextField(max_length=20)
    area = models.TextField(max_length=30)
    horario = models.OneToOneField(Horario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.rut)
