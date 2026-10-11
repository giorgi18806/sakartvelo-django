from django.urls import path

from sakartvelo import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),
    path("shop-grid/", views.shop_grid, name="shop-grid"),

]

app_name = "sakartvelo"
