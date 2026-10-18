from django.contrib.auth import views as auth_views
from django.urls import path

from sakartvelo import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("shop-grid/", views.shop_grid, name="shop-grid"),
    path(
        "products/<int:pk>/",
        views.ProductDetailView.as_view(),
        name="product-detail"
    ),
    path(
        "category/<int:category_id>/",
        views.CategoryProductListView.as_view(),
        name="category_products",
    ),

    # Authentication
    path(
        "register/",
        views.RegisterView.as_view(),
        name="register",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="sakartvelo/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

]

app_name = "sakartvelo"
