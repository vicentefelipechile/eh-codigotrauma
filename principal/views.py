# ============================================================
# ==================== Librerias y Clases ====================
# ============================================================

from django.shortcuts import render
from django.template import loader
from django.conf import settings
from pathlib import Path

from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.template.backends.django import Template



# ============================================================
# =================== Directorio Principal ===================
# ============================================================

MAIN_PATH: str = str(Path(__file__).parent.parent.absolute()) + "/templates"

CONTEXTO: dict = {
    'PaginaNombre': settings.DOMAIN_NAME,
    'PaginaNombreCorto': settings.DOMAIN_SHORTNAME,
    'ContrasenaRegex': settings.PASSWORD_REGEX,
}

# ============================================================
# ======================== Funciones =========================
# ============================================================

def PaginaPrincipal(request: WSGIRequest) -> HttpResponse:
    IndexHtml: Template = loader.get_template('index.html')

    return HttpResponse( IndexHtml.render(CONTEXTO, request) )



def PaginaContacto(request: WSGIRequest) -> HttpResponse:
    HTML: Template = loader.get_template('contacto.html')

    return HttpResponse( HTML.render(CONTEXTO, request) )



def PaginaRegistro(request: WSGIRequest) -> HttpResponse:
    HTML: Template = loader.get_template('registro.html')

    return HttpResponse( HTML.render(CONTEXTO, request) )