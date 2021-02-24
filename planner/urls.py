from django.urls import path
from . import views

urlpatterns = [
    path('planner/', views.planner),
    path('create_event/', views.create_event)
]
