# Librerias importantes
from django.shortcuts import render
from pathlib import Path

# Fuerte tipado librerias
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest

MAIN_PATH: str = str(Path(__file__).parent.parent.absolute()) + "/templates"

def PlantillaExiste(direccion: str = None) -> bool:
    if direccion == None:
        return False

    try:
        with open(MAIN_PATH + direccion, 'r') as Plantilla:
            return True
    except FileNotFoundError:
        return False


def PaginaPrincipal(request: WSGIRequest) -> HttpResponse:
    return render(request, 'index.html')