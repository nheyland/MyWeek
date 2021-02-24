from django.urls import path
from . import views, render
urlpatterns = [
    path('', render.index),
    path('registering/', views.registering),
    path('register/', views.register),
    path('login/', views.login),
    path('kill/', views.kill),
]
