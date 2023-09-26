from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, HttpResponse
from django.conf import settings

DOMAIN_NAME: str = settings.DOMAIN_NAME

# Create your views here.
def home(request: WSGIRequest) -> HttpResponse:

    return HttpResponse(f"""
                        <h1>hello world</h1>
                        <br>
                        <h2>La aplicacion se llamada {DOMAIN_NAME}</h2>
                        <h2>Y tu IP es {request.META['REMOTE_ADDR']}</h2>""")