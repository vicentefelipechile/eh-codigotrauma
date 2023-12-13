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

from principal.metodos.principal import RedireccionarUsuario, UsuarioYaInicioSesion


# ============================================================
# ======================== Funciones =========================
# ============================================================


def PaginaInicioSecretario(request: WSGIRequest) -> HttpResponse:
    if not UsuarioYaInicioSesion(request): return RedireccionarUsuario(request, True)

    secretario = Secretario.objects.all()
    ultimas_emergencias = Emergencia.objects.all().order_by("-emerg_fecha")[:5] 
    context = {
        "secretario": secretario,
        "ultimas_emergencias": ultimas_emergencias
    }
    return render(request, "inicio_secretario.html", context)