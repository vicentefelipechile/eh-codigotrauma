# =======================================================
# ================== Librerias y Clases =================
# =======================================================

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import principal.views as Principal

from django.urls import path



# =======================================================
# ================== Librerias y Clases =================
# =======================================================

urlpatterns = [
    ## === Paginas === ##

    path("", Principal.PaginaPrincipal, name="PaginaPrincipal"),
    #path("registro/", Principal.PaginaRegistro, name="PaginaRegistro"),
    path("iniciarsesion/", Principal.PaginaIniciarSesion, name="PaginaIniciarSesion"),
    path("admin/", admin.site.urls, name="PaginaAdministrador"),
    path("emergencias/", Principal.PaginaEmergencias, name="emergencias"),
    path("atenciones/", Principal.PaginaAtenciones, name="atenciones"),
    path("nueva_emergencia/", Principal.nueva_emergencia, name="nueva_emergencia"),
    path("inicio_secretario/", Principal.PaginaInicioSecretario, name="inicio_secretario"),
   
    ## === Personas === ##
    path("paciente/", Principal.PaginaPaciente, name="PaginaPaciente"),
    path("paciente/detalles/", Principal.DetallePaciente, name="DetallePaciente"),
    path("paciente/detalles/<int:pac_id>/", Principal.DetallePacienteID, name="DetallePacienteID"),
    path("doctor/", Principal.PaginaDoctor, name="PaginaDoctor"),
    path("doctor/horario/<int:doc_id>/", Principal.HorarioDoctor, name="HorarioDoctor"),
    path("doctor/detalles/", Principal.DetalleDoctor, name="DetalleDoctor"),
    path("doctor/detalles/<int:doc_id>/", Principal.DetalleDoctorID, name="DetalleDoctorID"),
    
    ## === Interfaz === ##
] 
