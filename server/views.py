from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse

# Create your views here.


def login(request):
    data = request.POST
    res = {"key": "value"}
    return JsonResponse(res)
