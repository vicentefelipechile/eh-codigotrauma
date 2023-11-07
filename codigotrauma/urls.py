# =======================================================
# ================== Librerias y Clases =================
# =======================================================

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import principal.views as Principal
from django.urls import path
from principal.views import lista_pacientes


# =======================================================
# ================== Librerias y Clases =================
# =======================================================

urlpatterns = [
    ## === Paginas === ##

    path("", Principal.PaginaPrincipal, name="PaginaPrincipal"),
    path("registro/", Principal.PaginaRegistro, name="PaginaRegistro"),
    path("iniciarsesion/", Principal.PaginaIniciarSesion, name="PaginaIniciarSesion"),
    path("empleados/", Principal.PaginaEmpleados, name="PaginaEmpleados"),
    path("admin/", admin.site.urls),
    path("lista_pacientes/", Principal.PaginaPacientes, name="PaginaPacientes" ),

    ## === API === ##
    
    # Validadores
    path("api/v1/usuario/", Principal.API.BuscarUsuario),
    
    # Registrar
    path("api/v1/registrar/usuario", Principal.API.RegistrarUsuario),
    # path("api/v1/registrar/doctor", Principal.API.RegistrarDoctor),
    # path("api/v1/registrar/secretario", Principal.API.RegistrarSecretario),
    # path("api/v1/registrar/paciente", Principal.API.RegistrarPaciente),

    # Historial
    # path("api/v1/historial/", Principal.API.HistorialEmergencias),
       
] 
