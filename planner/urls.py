from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('planner/<int:id>', views.planner),
    path('create_event/', views.create_event),
    path('details/<int:id>', views.details, name='eventDetail'),
    path('edit/<int:id>', views.edit_event),
    path('delete/<int:id>', views.delete_event, name='deleteEvent'),
    path('process_edit', views.process_edit),
    # path('load_geo_all/', views.load_geo_all),
]
