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
from django.contrib.auth import login

from principal.forms import NuevaEmergenciaForm
from principal.models import Administrador, Doctor, Secretario, Paciente, Emergencia, Atencion
from principal.models import Usuario
from principal.models import Session
from principal.forms import NuevaEmergenciaForm, PacienteForm


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
# ====================== Peticiones HTTP =====================
# ============================================================

def RespuestaCorta(EsError: bool = True, Mensaje: str = "Error", Codigo: int = 400) -> JsonResponse:
    return JsonResponse({ "error": EsError, "mensaje": Mensaje }, status=Codigo)


def GenerarYRedireccionar(request: WSGIRequest, session_id: str = None, user_type: int = 0):
    # Generar la cookie con la ID de sesión SUI (Session User ID)
    response = HttpResponseRedirect("/")
    response.set_cookie("SUI-Key", session_id)

    # Redireccionar al usuario a la página correspondiente según su tipo de usuario
    if user_type == 1:
        response["Location"] = "/empleados/"
    elif user_type == 2:
        response["Location"] = "/empleados/"
    elif user_type == 3:
        response["Location"] = "/emergencias/"

    return response



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

    if request.method == "POST":
        # Añadir un contexto para el formulario
        FormularioContext: dict = FORMULARIO.copy()

        if not request.POST["username"]:    return RespuestaCortaHTTP("iniciar-sesion.html", ERROR_NOUSER)
        if not request.POST["password"]:    return RespuestaCortaHTTP("iniciar-sesion.html", ERROR_NOPASS)
        
        # Buscar el usuario en la base de datos
        UsuarioEncontrado: QuerySet = Usuario.objects.filter(user_name=request.POST["username"]).first()
        if not UsuarioEncontrado:           return RespuestaCortaHTTP("iniciar-sesion.html", ERROR_USERDOESNTEXIST)

        # Verificar la contraseña
        if not check_password(request.POST["password"], UsuarioEncontrado.user_password): return RespuestaCortaHTTP("iniciar-sesion.html", ERROR_WRONGPASS)
        
        # Crear un identificador de sesión
        IdentificadorSesion: Session = Session()
        SessionID: str = IdentificadorSesion.SetSessionUser(UsuarioEncontrado)
        IdentificadorSesion.save()
        
        Redirecion: HttpResponseRedirect = GenerarYRedireccionar(request, SessionID, UsuarioEncontrado.user_type)
        return Redirecion


    HTML: Template = loader.get_template("iniciar-sesion.html")
    return HttpResponse( HTML.render(CONTEXTO, request) )


def PaginaInicioSecretario(request: WSGIRequest) -> HttpResponse:
    secretario = Secretario.objects.all()
    ultimas_emergencias = Emergencia.objects.all().order_by("-emerg_fecha")[:5] 
    context = {"secretario": secretario,"ultimas_emergencias": ultimas_emergencias}
    return render(request, "inicio_secretario.html", context)


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