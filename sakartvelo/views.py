from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from sakartvelo.models import Category


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "sakartvelo/index.html", {"categories": Category.objects.all()})

def contact(request:HttpRequest) -> HttpResponse:
    return render(request, "sakartvelo/contact.html",
                  {"categories": Category.objects.all(),
                    "breadcrumb_h2": "Contact Us",
                    "breadcrumb_span": "Contact Us"
                   })