# ============================================================
# ==================== Librerias y Clases ====================
# ============================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest

from principal.models import Doctor, Emergencia
from principal.metodos.principal import RedireccionarUsuario, UsuarioYaInicioSesion

DiasSemana: list[str] = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]


# ============================================================
# ======================== Funciones =========================
# ============================================================

def PaginaDoctor(request: WSGIRequest) -> HttpResponse:
    if not UsuarioYaInicioSesion(request): return RedireccionarUsuario(request, True)
    
    doctor = Doctor.objects.all()
    ultimas_emergencias = Emergencia.objects.all().order_by("-emerg_fecha")[:5] 
    context: dict[str | dict] = {
        "secretario": doctor,
        "ultimas_emergencias": ultimas_emergencias
    }

    return render(request, "doctor.html", context)


def HorarioDoctor(request: WSGIRequest) -> HttpResponse:
    if not UsuarioYaInicioSesion(request): return RedireccionarUsuario(request, True)
    doc_id: int = request.COOKIES.get("SUI-DOC", None)
    
    doctor = Doctor.objects.get(pk=doc_id)
    context: dict[str | dict] = {
        "doctor": doctor,
        "dias_semana": DiasSemana
    }

    return render(request, "doctorhorario.html", context)


def DetalleDoctor(request: WSGIRequest) -> HttpResponse:
    if not UsuarioYaInicioSesion(request): return RedireccionarUsuario(request, True)

    doctores = Doctor.objects.all()
    print(doctores[0].doc_id)
    context: dict[str | dict] = {
        "doctores": doctores
    }

    return render(request, "doctordetalle.html", context)


def DetalleDoctorID(request, doc_id):
    if not UsuarioYaInicioSesion(request): return RedireccionarUsuario(request, True)

    doctor: Doctor = get_object_or_404(Doctor, pk=doc_id)
    num_emergencias = doctor.total_emergencias()
    ultimas_emergencias = Emergencia.objects.filter(emerg_doc_id=doctor).order_by("-emerg_fecha")[:3]

    context: dict[str | dict] = {
        "doctor": doctor,
        "num_emergencias": num_emergencias,
        "ultimas_emergencias" : ultimas_emergencias
    }

    return render(request,"doctordetalleid.html", context)