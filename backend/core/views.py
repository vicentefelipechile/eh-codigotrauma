from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import json

# Create your views here.
def home(request: WSGIRequest) -> JsonResponse:
    return JsonResponse({
        'message': f'Bienvenido a ',
        'method': request.method
    })
def index(request):
    return render(request, 'index.html')