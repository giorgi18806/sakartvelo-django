from django.urls import path

from sakartvelo.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "sakartvelo"