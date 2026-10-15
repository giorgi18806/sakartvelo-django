from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView

from sakartvelo.forms import ContactMessageForm
from sakartvelo.models import Product, ContactMessage


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "sakartvelo/index.html")

# def contact(request:HttpRequest) -> HttpResponse:
#     context = {
#         "breadcrumb_h2": "Contact Us",
#         "breadcrumb_span": "Contact Us"
#     }
#     return render(request, "sakartvelo/contact.html", context=context)
class ContactView(CreateView):
    model = ContactMessage
    form_class = ContactMessageForm
    template_name = "sakartvelo/contact.html"
    success_url = reverse_lazy("sakartvelo:contact")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumb_h2"] = "Contact Us"
        context["breadcrumb_span"] = "Contact Us"

        return context

    def form_valid(self, form):
        messages.success(
            self.request,
            "Thank you! Your message has been sent successfully."
        )
        return super().form_valid(form)

def shop_grid(request:HttpRequest) -> HttpResponse:
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()

    # Start with active products
    products = Product.objects.filter(is_active=True)

    # Filter by text search (title or description)
    if query:
        query_lower = query.lower()

        products = products.annotate(
            title_lower=Lower('title'),
            desc_lower=Lower('description')
        ).filter(
            Q(title_lower__contains=query_lower) | Q(desc_lower__contains=query_lower)
        )

    context = {
        "products": products,
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