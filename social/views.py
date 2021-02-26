from django.shortcuts import render, redirect
from login.models import User

# VIEW USER PROFILE
def viewProfile(request, userID):
    currentUser = User.objects.get(id = request.session['user_id'])
    viewUser = User.objects.get(id = userID)
    context = {
        'viewUser': viewUser,
        'currentUser': currentUser
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
    # userProfile = UserProfile.objects.get(user = currentUser)
    friend2Add = User.objects.get(id = request.POST['friendID'])
    # friendsProfile = UserProfile.objects.get(user = friend2Add)
    currentUser.friends.add(friend2Add)
    # It should be reciprocal
    friend2Add.friends.add(currentUser)
    return redirect('allUsers')
