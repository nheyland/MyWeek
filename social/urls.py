from django.urls import path
import social.views as SocialViews

urlpatterns = [
    path('profile/<int:userID>/', SocialViews.viewProfile, name = 'viewProfile'),
    path('addFriend/', SocialViews.addFriend, name = 'addFriend'),
    path('confirmDelete/', SocialViews.confirmDeletionAndNotify, name = 'confirmDelete'),
    path('editProfile/<int:userID>/', SocialViews.editProfile, name = 'editProfile'),
    path('inviteFriend/', SocialViews.inviteFriend, name = 'inviteFriend'),
    path('inviteToEvent/', SocialViews.addFriendToEvent, name = 'inviteToEvent'),
]