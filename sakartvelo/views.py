from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView

from sakartvelo.forms import ContactMessageForm
from sakartvelo.models import Product, ContactMessage, Category


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "sakartvelo/index.html")


class ContactView(LoginRequiredMixin, CreateView):
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

@login_required
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


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 'self.object' is the current Product instance being viewed
        product = self.object

        context["breadcrumb_h2"] = product.title
        context["breadcrumb_second_option"] = "Shop"
        context["breadcrumb_span"] = product.title
        return context


class CategoryProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "sakartvelo/shop-grid.html"
    context_object_name = "products"

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            pk=self.kwargs["category_id"],
            is_active=True,
        )

        return Product.objects.filter(
            category=self.category,
            is_active=True,
        ).order_by("title")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["selected_category"] = self.category
        context["breadcrumb_h2"] = self.category.title
        context["breadcrumb_span"] = self.category.title

        return context


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "sakartvelo/register.html"
    success_url = reverse_lazy("sakartvelo:login")


