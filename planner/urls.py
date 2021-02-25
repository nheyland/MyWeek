from django.urls import path
from . import views

urlpatterns = [
    path('planner/', views.planner),
    path('create_event/', views.create_event),
    path('update_event/<int:event_to_update>', views.planner),
    path('process_update/<int:event_id>', views.update_event)

]
