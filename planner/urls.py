from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('planner/<int:id>', views.planner),
    path('create_event/', views.create_event),
    # ADDED NAME TO DETAILS PATH TO SIMPLIFY MAKING LINKS TO EVENTS. /ew
    path('details/<int:id>', views.details, name = 'eventDetail'),
]
