from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from sakartvelo.models import Category


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "sakartvelo/index.html")

def contact(request:HttpRequest) -> HttpResponse:
    context = {
        "breadcrumb_h2": "Contact Us",
        "breadcrumb_span": "Contact Us"
    }
    return render(request, "sakartvelo/contact.html", context=context)

def shop_grid(request:HttpRequest) -> HttpResponse:
    context = {
        "breadcrumb_h2": "Sakartvelo Shop",
        "breadcrumb_span": "Shop"
    }
    return render(request, "sakartvelo/shop-grid.html", context=context)