from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.app_homepage,name = "app_homepage"),
]
