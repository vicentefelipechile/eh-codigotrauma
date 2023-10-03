from django.shortcuts import render

# Fuerte tipado librerias
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest


def index(request: WSGIRequest) -> HttpResponse:

    return HttpResponse("<h1>Hello World</h1>")