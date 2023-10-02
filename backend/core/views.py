from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import json

DOMAIN_NAME: str = settings.DOMAIN_NAME

# Create your views here.
def home(request: WSGIRequest) -> JsonResponse:
    return JsonResponse({
        'message': f'Bienvenido a {DOMAIN_NAME}',
        'method': request.method
    })