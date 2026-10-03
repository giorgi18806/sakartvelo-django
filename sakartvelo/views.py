from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import sakartvelo


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "sakartvelo/index.html")
