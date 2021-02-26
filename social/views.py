from django.shortcuts import render, redirect
from login.models import User, UserProfile

# VIEW USER PROFILE
def viewProfile(request, userID):
    viewUser = User.objects.get(id = userID)
    context = {
        'viewUser': viewUser
    }
    return render(request, 'social/profile.html', context)

# ALL USER LIST - NOT FOR PRODUCTION, JUST FOR DEVELOPMENT USE.
def allUsers(request):
    context = {
        'allUsers': User.objects.all()
    }
    return render(request, 'social/allusers.html', context)

# ADD TO FRIENDS LIST
def addFriend(request):
    # Making Assumptions till the User Profile is built.
    currentUser = User.objects.get(id = request.session['user_id'])
    friend2Add = User.objects.get(id = request.post['friendID'])
    currentUser.friends_list.add(friend2Add)
    # It should be reciprocal
    friend2Add.friends_list.add(currentUser)
    return redirect('/')
