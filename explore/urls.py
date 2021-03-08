from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.all),
    path('search_events/', views.all),
    path('load_geo_all/', views.load_geo_all),
]
