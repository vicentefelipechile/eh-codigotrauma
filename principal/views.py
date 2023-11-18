# ============================================================
# ==================== Librerias y Clases ====================
# ============================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.conf import settings
from pathlib import Path
from datetime import datetime


from django.http import HttpResponse, JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.template.backends.django import Template
from django.db.models.query import QuerySet
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from principal.models import Administrador, Doctor, Secretario, Paciente, Emergencia, Atencion


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
        # Añadir un contexto para el formulario
        RegistroContext: dict = FORMULARIO.copy()
        
        # Si el POST no contiene el usuario o la contraseña, mostrar un error
        if not request.POST["username"] or not request.POST["password"]:
            RegistroContext["error"] = True
            RegistroContext["error_mensaje"] = "No se ha especificado el usuario o la contraseña"
            
            return HttpResponse( HTML.render(RegistroContext, request) )
        
        # Buscar el usuario en la base de datos
        # Si no existe, mostrar un error
        usuario = None
        try:
            usuario = Administrador.objects.get(adm_cuentausuario=request.POST["username"])
        except:
            try:
                usuario = Doctor.objects.get(doc_cuentausuario=request.POST["username"])
            except:
                try:
                    usuario = Secretario.objects.get(sec_cuentausuario=request.POST["username"])
                except:
                    RegistroContext["error"] = True
                    RegistroContext["error_mensaje"] = "El usuario no existe"
                    
                    return HttpResponse( HTML.render(RegistroContext, request) )
        
        # Si la contraseña no coincide, mostrar un error
        if not usuario.ComprobarContrasena(request.POST["password"]):
            RegistroContext["error"] = True
            RegistroContext["error_mensaje"] = "La contraseña no coincide"
        
        
        # Si el usuario es un administrador, redirigir a la pagina de administrador
        if isinstance(usuario, Administrador):
            return redirect(reverse("PaginaAdministrador"))
        
        return HttpResponse( HTML.render(RegistroContext, request) )

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

    context = {'pacientes': pacientes, 'configuracionanterior': { "cantidad": MostrarCantidad, "pagina": Pagina, "busqueda": Busqueda }}
    return render(request, 'lista_pacientes.html', context)



def PaginaDoctores(request: WSGIRequest) -> HttpResponse:
    doctores = Doctor.objects.all()
    context = {'doctores': doctores}
    return render(request, 'empleados.html', context)



def detalles_paciente(request, pac_id):
    paciente = get_object_or_404(Paciente, pk=pac_id)
    num_emergencias = paciente.cantidad_emergencias()
    anio_actual = datetime.now().year
    paciente.edad = anio_actual - paciente.pac_nacimiento
    ultimas_emergencias = Emergencia.objects.filter(emerg_pac_id=paciente).order_by('-emerg_fecha')[:3]
    ultima_atencion = Atencion.objects.filter(atenc_pac_id=paciente).order_by('-atenc_fecha').first()

    context=  {'paciente': paciente,
                'num_emergencias': num_emergencias,
                'ultimas_emergencias': ultimas_emergencias,
                'ultima_atencion': ultima_atencion}


    return render(request,'detalles_paciente.html', context)