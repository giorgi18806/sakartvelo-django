from django.urls import path

from sakartvelo import views
from sakartvelo.views import index

urlpatterns = [
    path("", index, name="index"),
    path("contact/", views.contact, name="contact"),
]

app_name = "sakartvelo"
