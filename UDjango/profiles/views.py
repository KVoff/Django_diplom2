from django.shortcuts import render
from django.contrib.auth.decorators import login_required



def profile(request):

    buyer = request.user
    return render(request, 'profile/profile.html', {'buyer': buyer})
