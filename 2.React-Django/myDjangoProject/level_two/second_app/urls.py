from django.contrib import admin
from django.urls import path,re_path,include
from . import views

urlpatterns = [
    #path("admin/", admin.site.urls),
    path("index/", views.index),
    re_path(r"^$", views.index),
    path("users/", views.users),
    path("forms/", views.form_name),
]