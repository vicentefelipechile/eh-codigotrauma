# ============================================================
# ==================== Librerias y Clases ====================
# ============================================================


from django.http import JsonResponse, HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest

from django.urls import reverse

from principal.models import Doctor
from principal.models import Usuario
from principal.models import Session

# ============================================================
# ====================== Peticiones HTTP =====================
# ============================================================

def RespuestaCorta(EsError: bool = True, Mensaje: str = "Error", Codigo: int = 400) -> JsonResponse:
    return JsonResponse({ "error": EsError, "mensaje": Mensaje }, status=Codigo)


def GenerarYRedireccionar(request: WSGIRequest, session_id: str, user: Usuario):
    # Generar la cookie con la ID de sesión SUI (Session User ID)
    response = HttpResponseRedirect("/")
    response.set_cookie("SUI-Key", session_id)
    response.set_cookie("SUI-US", user.user_name)

    # Redireccionar al usuario a la página correspondiente según su tipo de usuario
    match user.user_type:
        case 0: # Root
            response["Location"] = reverse("PaginaPrincipal")
            
        case 1: # Administrador
            response["Location"] = reverse("PaginaPrincipal")
            
        case 2: # Secretario
            response["Location"] = reverse("inicio_secretario")
            
        case 3: # Doctor
            response["Location"] = reverse("PaginaDoctor")
            doctor: Doctor = Doctor.objects.filter(user_name=user.user_name).first()
            doctorid: int = doctor.doc_id
            
            response.set_cookie("SUI-DOC", str(doctorid))
            
        case 4: # Paciente
            response["Location"] = reverse("PaginaPaciente")

    return response


def UsuarioYaInicioSesion(r: WSGIRequest) -> bool: return True if ( r.COOKIES.get("SUI-Key", None) and r.COOKIES.get("SUI-US", None) ) else False

def RedireccionarUsuario(request: WSGIRequest, deletecookies: bool = False) -> HttpResponseRedirect:
    # Verificar si el hash de la cookie es válido
    SessionID:              str = request.COOKIES.get("SUI-Key", None)
    SessionUser:            str = request.COOKIES.get("SUI-US", None)
    IdentificadorSesion:    Session = Session.objects.filter(session_key=SessionUser).first()
    UsuarioClase:           Usuario = Usuario.objects.filter(user_name=SessionUser).first()
    
    if deletecookies:
        response = HttpResponseRedirect(reverse("PaginaIniciarSesion"))
        response.delete_cookie("SUI-Key")
        response.delete_cookie("SUI-US")
        response.delete_cookie("SUI-DOC")
        return response
    
    if not SessionID or not SessionUser:
        return HttpResponseRedirect(reverse("PaginaIniciarSesion"))
    
    if not IdentificadorSesion:
        return HttpResponseRedirect(reverse("PaginaIniciarSesion"))
    
    # Verificar si el usuario contiene la sesión correcta dando como argumento el usuario, la hash y la ip del usuario
    if not IdentificadorSesion.CheckSesion(UsuarioClase, SessionID, request.META["REMOTE_ADDR"]):
        return HttpResponseRedirect(reverse("PaginaIniciarSesion"))
    
    # Redireccionar al usuario a la página correspondiente según su tipo de usuario
    match UsuarioClase.user_type:
        case 0: # Root
            return HttpResponseRedirect(reverse("PaginaPrincipal"))
            
        case 1: # Administrador
            return HttpResponseRedirect(reverse("PaginaPrincipal"))
            
        case 2: # Secretario
            return HttpResponseRedirect(reverse("inicio_secretario"))
            
        case 3: # Doctor
            return HttpResponseRedirect(reverse("PaginaDoctor"))
            
        case 4: # Paciente
            return HttpResponseRedirect(reverse("PaginaPaciente"))
    
    return HttpResponseRedirect(reverse("PaginaIniciarSesion"))


def PaginaCerrarSesion(request: WSGIRequest) -> HttpResponseRedirect:
    response = HttpResponseRedirect(reverse("PaginaIniciarSesion"))
    response.delete_cookie("SUI-Key")
    response.delete_cookie("SUI-US")
    response.delete_cookie("SUI-DOC")
    return response