from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("me-conheca/", views.presentation, name="presentation"),
    path("apresentacao/", RedirectView.as_view(pattern_name="presentation", permanent=True)),
]
