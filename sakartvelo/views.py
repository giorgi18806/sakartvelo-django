from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView

from sakartvelo.models import Product


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


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 'self.object' is the current Product instance being viewed
        product = self.object

        context["breadcrumb_h2"] = product.title
        context["breadcrumb_second_option"] = "Shop"
        context["breadcrumb_span"] = product.title
        return context