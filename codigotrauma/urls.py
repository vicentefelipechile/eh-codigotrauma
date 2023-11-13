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
    path("empleados/", Principal.PaginaEmpleados, name="PaginaEmpleados"),
    path("admin/", admin.site.urls),
    path("lista_pacientes/", Principal.PaginaPacientes, name="PaginaPacientes"),
    path("empleados/", Principal.PaginaDoctores, name="PaginaDoctores"),
       
] 
