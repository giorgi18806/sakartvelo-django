from django.urls import path

from sakartvelo import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("shop-grid/", views.shop_grid, name="shop-grid"),
    path("products/<int:pk>", views.ProductDetailView.as_view(), name="product-detail"),

]

app_name = "sakartvelo"
