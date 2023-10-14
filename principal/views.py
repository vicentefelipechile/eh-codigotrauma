# ============================================================
# ==================== Librerias y Clases ====================
# ============================================================
from django.shortcuts import render
from pathlib import Path

from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest

# ============================================================
# =================== Directorio Principal ===================
# ============================================================

MAIN_PATH: str = str(Path(__file__).parent.parent.absolute()) + "/templates"


# ============================================================
# ======================== Funciones =========================
# ============================================================

def PaginaPrincipal(request: WSGIRequest) -> HttpResponse:
    return render(request, 'index.html')

def PaginaContacto(request: WSGIRequest) -> HttpResponse:
    return render(request, 'contacto.html')