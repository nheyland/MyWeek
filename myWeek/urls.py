from django.urls import path, include

urlpatterns = [
    path('', include('planner.urls')),
    path('', include('login.urls')),
    path('u/', include('social.urls')),
    path('explore/',include('explore.urls'))
]
