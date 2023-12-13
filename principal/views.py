# ============================================================
# ==================== Librerias y Clases ====================
# ============================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.conf import settings
from pathlib import Path
from datetime import datetime


from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest
from django.template.backends.django import Template
from django.db.models.query import QuerySet

from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse

from principal.forms import NuevaEmergenciaForm
from principal.models import Administrador, Doctor, Secretario, Paciente, Emergencia, Atencion
from principal.models import Usuario
from principal.models import Session
from principal.forms import NuevaEmergenciaForm, PacienteForm


from .metodos.principal import *

from .metodos.secretario import *
from .metodos.paciente import *
from .metodos.doctor import *

# ============================================================
# =================== Directorio Principal ===================
# ============================================================

MAIN_PATH: str = str(Path(__file__).parent.parent.absolute()) + "/templates"

CONTEXTO: dict = {
    "PaginaNombre": settings.DOMAIN_NAME,
    "PaginaNombreCorto": settings.DOMAIN_SHORTNAME
}

FORMULARIO: dict = CONTEXTO.copy()
FORMULARIO["form"] = UserCreationForm


# ============================================================
# ======================= Enumeraciones ======================
# ============================================================

ERROR_UNKNOWN = "Error desconocido"
ERROR_NOPASS = "No se ha especificado la contraseña"
ERROR_NOUSER = "No se ha especificado el usuario"
ERROR_NOMATCHPASS = "Las contraseñas no coinciden"
ERROR_USERDOESNTEXIST = "El usuario no existe"
ERROR_WRONGPASS = "La contraseña es incorrecta"

def RespuestaCortaHTTP(Direccion: str = "iniciar-sesion.html", ErrorTipo: str = None, EsError: bool = True) -> HttpResponse:
    FormularioContext: dict = FORMULARIO.copy()
    
    if not ErrorTipo:
        FormularioContext["error"] = True
        FormularioContext["error_mensaje"] = ERROR_UNKNOWN
        
        return HttpResponse( loader.get_template(Direccion).render(FormularioContext) )
    
    FormularioContext["error"] = EsError
    FormularioContext["error_mensaje"] = ErrorTipo
    
    return HttpResponse( loader.get_template(Direccion).render(FormularioContext) )



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

        if not request.POST["username"]:                                return RespuestaCortaHTTP("registro.html", ERROR_NOUSER)
        if not request.POST["password1"] == request.POST["password2"]:  return RespuestaCortaHTTP("registro.html", ERROR_NOMATCHPASS)
        
        RegistroContext["registered"] = True
        
        return HttpResponse( HTML.render(RegistroContext, request) )

    return HttpResponse( HTML.render(FORMULARIO, request) )



def PaginaIniciarSesion(request: WSGIRequest) -> HttpResponse | HttpResponseRedirect:
    # Verificar si el usuario ya ha iniciado sesión
    if UsuarioYaInicioSesion(request):  return RedireccionarUsuario(request)

    if request.method == "POST":
        if not request.POST["username"]:    return RespuestaCortaHTTP("iniciar-sesion.html", ERROR_NOUSER)
        if not request.POST["password"]:    return RespuestaCortaHTTP("iniciar-sesion.html", ERROR_NOPASS)
        
        # Buscar el usuario en la base de datos
        UsuarioEncontrado: QuerySet = Usuario.objects.filter(user_name=request.POST["username"]).first()
        if not UsuarioEncontrado:           return RespuestaCortaHTTP("iniciar-sesion.html", ERROR_USERDOESNTEXIST)

        # Verificar la contraseña
        if not check_password(request.POST["password"], UsuarioEncontrado.user_password): return RespuestaCortaHTTP("iniciar-sesion.html", ERROR_WRONGPASS)
        
        # Crear un identificador de sesión
        IdentificadorSesion: Session = Session()
        SessionID: str = IdentificadorSesion.SetSessionUser(UsuarioEncontrado, request.META["REMOTE_ADDR"])
        IdentificadorSesion.save()
        
        return GenerarYRedireccionar(request, SessionID, UsuarioEncontrado)


    HTML: Template = loader.get_template("iniciar-sesion.html")
    return HttpResponse( HTML.render(CONTEXTO, request) )


def PaginaEmergencias(request: WSGIRequest) -> HttpResponse:
    emergencias = Emergencia.objects.all()

    # Crear una lista para almacenar el número de pacientes para cada emergencia
    num_pacientes_por_emergencia = []

    for emergencia in emergencias:
        num_pacientes = emergencia.total_pacientes()
        num_pacientes_por_emergencia.append(num_pacientes)

    context = {"emergencias": emergencias, "num_pacientes_por_emergencia": num_pacientes_por_emergencia}
    return render(request, "emergencias.html", context)


def PaginaAtenciones(request: WSGIRequest) -> HttpResponse:
    atencion = Atencion.objects.all()
    context = {"atenciones": atencion}
    return render(request, "atenciones.html", context)


def nueva_emergencia(request):
    if request.method == "POST":
        form = NuevaEmergenciaForm(request.POST)
        if form.is_valid():
            emergencia = form.save(commit=False)
            num_pacientes = emergencia.num_pacientes
            emergencia.save()

            for _ in range(num_pacientes):
                paciente_form = PacienteForm(request.POST)
                if paciente_form.is_valid():
                    paciente = paciente_form.save()
                    emergencia.pacientes.add(paciente)

            return redirect("emergencias")
    else:
        form = NuevaEmergenciaForm()

    context = {"form": form}
    return render(request, "nueva_emergencia.html", context)