# ============================================================
# ==================== Librerias y Clases ====================
# ============================================================

from django.shortcuts import render
from django.template import loader
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from principal.models import Paciente
from pathlib import Path

from django.http import HttpResponse, JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.template.backends.django import Template
from django.db.models.query import QuerySet


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

FORMULARIO: dict = CONTEXTO.copy()
FORMULARIO["form"] = UserCreationForm



# ============================================================
# ======================== Funciones =========================
# ============================================================

def PaginaPrincipal(request: WSGIRequest) -> HttpResponse:
    IndexHtml: Template = loader.get_template("index.html")

    return HttpResponse( IndexHtml.render(CONTEXTO, request) )



def PaginaRegistro(request: WSGIRequest) -> HttpResponse:
    HTML: Template = loader.get_template("registro.html")
    
    if request.method == "POST":
        RegistroContext: dict = FORMULARIO.copy()

        if not request.POST["username"]:
            RegistroContext["error"] = True
            RegistroContext["error_mensaje"] = "No se ha especificado el usuario"
            
            return HttpResponse( HTML.render(RegistroContext, request) )


        if not request.POST["password1"] == request.POST["password2"]:
            RegistroContext["error"] = True
            RegistroContext["error_mensaje"] = "Las contraseñas no coinciden"
            
            return HttpResponse( HTML.render(RegistroContext, request) )
        
        RegistroContext["registered"] = True
        
        return HttpResponse( HTML.render(RegistroContext, request) )

    return HttpResponse( HTML.render(FORMULARIO, request) )


def PaginaIniciarSesion(request: WSGIRequest) -> HttpResponse:
    HTML: Template = loader.get_template("iniciar-sesion.html")
    
    
    if request.method == "POST":

        RegistroContext: dict = FORMULARIO.copy()

        if not request.POST["username"]:
            RegistroContext["error"] = True
            RegistroContext["error_mensaje"] = "No se ha especificado el usuario"
            
            return HttpResponse( HTML.render(RegistroContext, request) )


        if not request.POST["password"]:
            RegistroContext["error"] = True
            RegistroContext["error_mensaje"] = "No se ha especificado la contraseña"
            
            return HttpResponse( HTML.render(RegistroContext, request) )
        
        # Buscar usuario y verificar contraseña
        # Si no existe, mostrar error

        try:
            User: Administrador = Administrador.objects.get(CuentaUsuario=request.POST["username"])
            
            if User.ComprobarContrasena(request.POST["password"]):
                
                RegistroContext["success"] = True
                RegistroContext["success_mensaje"] = "Usuario encontrado"
                
                return HttpResponse( HTML.render(RegistroContext, request) )
        except Exception as Error:
            print("Ai un error")
        
        return HttpResponse( HTML.render(RegistroContext, request) )

    return HttpResponse( HTML.render(CONTEXTO, request) )



def PaginaEmpleados(request: WSGIRequest) -> HttpResponse:
    HTML: Template = loader.get_template("empleados.html")

    return HttpResponse( HTML.render(CONTEXTO, request) )

def PaginaPacientes(request):
    pacientes = Paciente.objects.all()
    context = {'Pacientes': pacientes}
    return render(request, 'lista_pacientes.html', context)

# ============================================================
# ====================== Peticiones HTTP =====================
# ============================================================

def RespuestaCorta(EsError: bool = True, Mensaje: str = "Error", Codigo: int = 400) -> JsonResponse:
    return JsonResponse({ "error": EsError, "mensaje": Mensaje }, status=Codigo)



class API():

    def BuscarUsuario(request: WSGIRequest) -> JsonResponse | HttpResponse:
        ...


    def RegistrarUsuario(request: WSGIRequest) -> JsonResponse | HttpResponse:
        print(request.method)
        if not ( request.method == "POST"):
            return PaginaRegistro(request)


        UserContext: dict = FORMULARIO.copy()
        
        if not request.POST["username"]:
            UserContext["error"] = True
            UserContext["error_mensaje"] = "No se ha especificado el usuario"
            
            return RespuestaCorta(True, "No se ha especificado el usuario", 400)

        if not request.POST["password1"] == request.POST["password2"]:
            UserContext["error"] = True
            UserContext["error_mensaje"] = "Las contraseñas no coinciden"
            
            return RespuestaCorta(True, "Las contraseñas no coinciden", 400)
        
        UserContext["registered"] = True
        
        return RespuestaCorta(False, "Usuario registrado", 200)
    




    