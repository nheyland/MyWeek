from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('planner/', views.planner),
    path('create_event/', views.create_event),
    path('details/<int:id>', views.details),
]
