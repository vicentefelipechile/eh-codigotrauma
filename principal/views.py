# ============================================================
# ==================== Librerias y Clases ====================
# ============================================================

from django.shortcuts import render
from django.template import loader
from django.conf import settings
from pathlib import Path

from django.http import HttpResponse, JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.template.backends.django import Template


from principal.models import Administrador, DoctorClave, Secretario, Paciente


# ============================================================
# =================== Directorio Principal ===================
# ============================================================

MAIN_PATH: str = str(Path(__file__).parent.parent.absolute()) + "/templates"

CONTEXTO: dict = {
    "PaginaNombre": settings.DOMAIN_NAME,
    "PaginaNombreCorto": settings.DOMAIN_SHORTNAME,
    "ContrasenaRegex": settings.PASSWORD_REGEX,
}



# ============================================================
# ======================== Funciones =========================
# ============================================================

def PaginaPrincipal(request: WSGIRequest) -> HttpResponse:
    IndexHtml: Template = loader.get_template("index.html")

    return HttpResponse( IndexHtml.render(CONTEXTO, request) )



def PaginaContacto(request: WSGIRequest) -> HttpResponse:
    HTML: Template = loader.get_template("contacto.html")

    return HttpResponse( HTML.render(CONTEXTO, request) )



def PaginaRegistro(request: WSGIRequest) -> HttpResponse:
    HTML: Template = loader.get_template("registro.html")

    return HttpResponse( HTML.render(CONTEXTO, request) )



# ============================================================
# ====================== Peticiones HTTP =====================
# ============================================================

def RespuestaCorta(EsError: bool = True, Mensaje: str = "Error", Codigo: int = 400) -> JsonResponse:
    return JsonResponse({ "error": EsError, "mensaje": Mensaje }, status=Codigo)



class API():

    def ValidarUsuario(request: WSGIRequest) -> JsonResponse:
        if request.method == "POST":

            # Utilizamos el Bearer Token para validar la sesion (Como en OpenAI)
            if "HTTP_AUTHORIZATION" not in request.META:
                return RespuestaCorta(True, "No se ha especificado el identificador de sesion", 401)


            # Verificamos si el usuario existe en la base de datos
            # Si no existe, se devuelve un error
            Usuario: str = request.headers.get(settings.API_CONFIG["Usuario"]["Header-Usuario"])
            Contrasena: str = request.headers.get(settings.API_CONFIG["Usuario"]["Header-Contrasena"])
            TipoUsuario: str = request.headers.get(settings.API_CONFIG["Usuario"]["Header-TipoUsuario"])


            if not Usuario:
                return RespuestaCorta(True, "No se ha especificado el usuario", 400)


            if not Contrasena:
                return RespuestaCorta(True, "No se ha especificado la contraseña", 400)


            if not TipoUsuario:
                return RespuestaCorta(True, "No se ha especificado el tipo de usuario", 400)


            if ( settings.API_CONFIG["Usuario"]["TipoUsuario"].get(TipoUsuario) ):
                try:
                    Usuario = Administrador.objects.get(CuentaUsuario=Usuario)
                except:
                    return RespuestaCorta(True, "Usuario no encontrado", 404)


            return RespuestaCorta(False, "Usuario valido", 200)

        # ============================================================
        # =================== Metodos no permitidos ==================
        # ============================================================
        else:
            return RespuestaCorta(True, "Metodo no permitido", 405)