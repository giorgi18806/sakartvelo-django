from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import sakartvelo
from sakartvelo.models import Category


def index(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, "sakartvelo/index.html", context=context)
