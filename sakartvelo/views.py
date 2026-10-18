from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView

from sakartvelo.forms import ContactMessageForm, CustomerRegistrationForm
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


def apply_sorting(queryset, request):
    sort_option = request.GET.get('sort', '').strip()

    allowed_sorts = {
        'title': 'title',
        '-title': '-title',
        'price': 'price',
        '-price': '-price',
        '-created_at': '-created_at',
        'created_at': 'created_at',
    }

    if sort_option in allowed_sorts:
        return queryset.order_by(allowed_sorts[sort_option])

    # Default fallback sorting
    return queryset.order_by('title')


@login_required
def shop_grid(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()

    products = Product.objects.filter(is_active=True)

    if query:
        query_lower = query.lower()
        products = products.annotate(
            title_lower=Lower('title'),
            desc_lower=Lower('description')
        ).filter(
            Q(title_lower__contains=query_lower) | Q(desc_lower__contains=query_lower)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    # Apply sorting using our helper function
    products = apply_sorting(products, request)

    paginator = Paginator(products, 9)  # Show 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,  # Pass the page object instead of the raw queryset
        "is_paginated": page_obj.has_other_pages(),
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "breadcrumb_h2": "Sakartvelo Shop",
        "breadcrumb_span": "Shop"
    }
    return render(request, "sakartvelo/shop-grid.html", context=context)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_queryset(self):
        # Restrict the queryset so only active products can be retrieved
        return super().get_queryset().filter(is_active=True)

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
    paginate_by = 9

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            pk=self.kwargs["category_id"],
            is_active=True,
        )

        queryset = Product.objects.filter(
            category=self.category,
            is_active=True,
        )

        # Apply sorting via helper function here as well
        return apply_sorting(queryset, self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_category"] = self.category
        context["categories"] = Category.objects.all()
        context["breadcrumb_h2"] = self.category.title
        context["breadcrumb_span"] = self.category.title
        return context


class RegisterView(CreateView):
    form_class = CustomerRegistrationForm
    template_name = "sakartvelo/register.html"
    success_url = reverse_lazy("sakartvelo:login")
