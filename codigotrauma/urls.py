# =======================================================
# ================== Librerias y Clases =================
# =======================================================

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import principal.views as Principal



# =======================================================
# ================== Librerias y Clases =================
# =======================================================

urlpatterns = [
    # Paginas
    path('', Principal.PaginaPrincipal, name='PaginaPrincipal'),
    path('contacto/', Principal.PaginaContacto, name='PaginaContacto'),
    path('registro/', Principal.PaginaRegistro, name='PaginaRegistro'),
    path('admin/', admin.site.urls),

    # API
    path('v1/usuario/', Principal.API.ValidarUsuario)
] 
