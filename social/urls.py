from django.urls import path
import social.views as SocialViews

urlpatterns = [
    path('<int:userID>', SocialViews.viewProfile, name = 'viewProfile'),
    path('addFriend/', SocialViews.addFriend, name = 'addFriend'),
    path('allusers/', SocialViews.allUsers, name = 'allUsers'),
]