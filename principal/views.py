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
from django.urls import reverse

from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from principal.models import Administrador, Doctor, Secretario, Paciente, Emergencia, Atencion
from principal.models import Usuario


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
    HTML: Template = loader.get_template("iniciar-sesion.html")
    
    
    if request.method == "POST":
        print("=====================================")
        # Añadir un contexto para el formulario
        FormularioContext: dict = FORMULARIO.copy()

        if not request.POST["username"]:                               return RespuestaCortaHTTP("iniciar-sesion.html", ERROR_NOUSER)
        if not request.POST["password"]:                               return RespuestaCortaHTTP("iniciar-sesion.html", ERROR_NOPASS)
        
        # Buscar el usuario en la base de datos
        UsuarioEncontrado: QuerySet = Usuario.objects.filter(user_name=request.POST["username"]).first()
        if not UsuarioEncontrado:                                      return RespuestaCortaHTTP("iniciar-sesion.html", ERROR_USERDOESNTEXIST)

        # Verificar la contraseña
        if not check_password(request.POST["password"], UsuarioEncontrado.user_password): return RespuestaCortaHTTP("iniciar-sesion.html", ERROR_WRONGPASS)
        
        # Si el usuario es un administrador (1), redirigir a la pagina de administrador
        # Si el usuario es un secretario (2), redirigir a la pagina de secretario
        # Si el usuario es un doctor (3), redirigir a la pagina de doctor
        if UsuarioEncontrado.user_type == 1:
            return redirect("/empleados/")
        elif UsuarioEncontrado.user_type == 2:
            return redirect("/empleados/")
        elif UsuarioEncontrado.user_type == 3:
            return redirect("/emergencias/")

    return HttpResponse( HTML.render(CONTEXTO, request) )



def PaginaPacientes(request: WSGIRequest) -> HttpResponse:
    MostrarCantidad: int = 20
    Pagina: int = 1
    Busqueda: str = ""

    try:
        MostrarCantidad = int(request.GET["cantidad"])
    except:
        pass

    try:
        Pagina = int(request.GET["pagina"])
    except:
        pass
    

    try:
        # Buscar pacientes
        # Extraer todos los numeros de la busqueda
        # Si existen numeros en la busqueda, buscar por rut con este formato ("SELECT * FROM paciente WHERE rut LIKE '{numero}%'")
        # En el caso contrario, buscar por apellido paterno con este formato ("SELECT * FROM paciente WHERE apellidopaterno LIKE '{apellido}%'") ignorando los acentos
        try:
            Busqueda = request.GET["buscarpaciente"]
        except:
            pacientes = Paciente.objects.all()
        
        if Busqueda:
            if Busqueda.isnumeric():
                pacientes = Paciente.objects.filter(rut__startswith=Busqueda)
            else:
                pacientes = Paciente.objects.filter(apellidopaterno__startswith=Busqueda)
    except:
        pacientes = Paciente.objects.all()


    # Mostrar la cantidad de pacientes especificada y la pagina especificada
    # Si la pagina dice numero 2, se saltaran los primero 20 pacientes y se mostraran los siguientes 20
    pacientes = pacientes[(Pagina - 1) * MostrarCantidad : (Pagina * MostrarCantidad)]

    context: dict = {
        "pacientes":        pacientes,
        "configuracionanterior": {
            "cantidad":     MostrarCantidad,
            "pagina":       Pagina,
            "busqueda":     Busqueda
            }
        }

    return render(request, "lista_pacientes.html", context)



def PaginaDoctores(request: WSGIRequest) -> HttpResponse:
    doctores = Doctor.objects.all()
    context = {'doctores': doctores}
    return render(request, 'empleados.html', context)

def PaginaEmergencias(request: WSGIRequest) -> HttpResponse:
    emergencia = Emergencia.objects.all()
    context = {'emergencias': emergencia}
    return render(request, 'emergencias.html', context)

def PaginaAtenciones(request: WSGIRequest) -> HttpResponse:
    atencion = Atencion.objects.all()
    context = {'atenciones': atencion}
    return render(request, 'atenciones.html', context)

def detalles_doctores(request, doc_id):
    doctor= get_object_or_404(Doctor, pk=doc_id)
    num_emergencias = doctor.total_emergencias()
    ultimas_emergencias = Emergencia.objects.filter(emerg_doc_id=doctor).order_by('-emerg_fecha')[:3]


    context=  {'doctor': doctor,
               'num_emergencias': num_emergencias,
               'ultimas_emergencias' : ultimas_emergencias}

    return render(request,'detalles_doctores.html', context)

def detalles_paciente(request, pac_id):
    paciente = get_object_or_404(Paciente, pk=pac_id)
    num_emergencias = paciente.total_emergencias()
    num_atenciones = paciente.total_atenciones()
    print(f"DEBUG: Número total de emergencias para el paciente {paciente.pac_primernombre}: {num_emergencias}")
    anio_actual = datetime.now().year
    paciente.edad = anio_actual - paciente.pac_nacimiento
    ultimas_emergencias = Emergencia.objects.filter(emerg_pac_id=paciente).order_by('-emerg_fecha')[:3]
    ultima_atencion = Atencion.objects.filter(atenc_pac_id=paciente).order_by('-atenc_fecha').last()

    context=  {'paciente': paciente,
                'num_emergencias': num_emergencias,
                'num_atenciones' : num_atenciones,
                'ultimas_emergencias': ultimas_emergencias,
                'ultima_atencion': ultima_atencion}


    return render(request,'detalles_paciente.html', context)

def horario_doctor(request, doc_id):
    doctor = Doctor.objects.get(pk=doc_id)
    context = {'doctor': doctor, 'dias_semana': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']}
    return render(request, 'horario_doctor.html', context)


