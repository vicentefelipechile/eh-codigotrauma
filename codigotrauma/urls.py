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
    path("registro/", Principal.PaginaRegistro, name="PaginaRegistro"),
    path("iniciarsesion/", Principal.PaginaIniciarSesion, name="PaginaIniciarSesion"),
    path("admin/", admin.site.urls, name="PaginaAdministrador"),
    path("lista_pacientes/", Principal.PaginaPacientes, name="PaginaPacientes"),
    path("empleados/", Principal.PaginaDoctores, name="PaginaDoctores"),
    path('detalles_paciente/<int:pac_id>/', Principal.detalles_paciente, name='detalles_paciente'),
    path('detalles_doctores/<int:doc_id>/', Principal.detalles_doctores, name="detalles_doctores"),
    path('horario_doctor/<int:doc_id>/', Principal.horario_doctor, name='horario_doctor'),
    path('emergencias/', Principal.PaginaEmergencias, name="emergencias"),
    path('atenciones/', Principal.PaginaAtenciones, name="atenciones"),
    path('nueva_emergencia/', Principal.nueva_emergencia, name='nueva_emergencia'),
    path('inicio_secretario/', Principal.PaginaInicioSecretario, name='inicio_secretario'),
    path('inicio_doctor/', Principal.PaginaInicioDoctor, name='inicio_doctor'),
   

       
] 
