from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, admin
from django.contrib.auth.models import User
from .models import WebUser
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def profile_redirect(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('admin:index'))
    return HttpResponseRedirect(reverse('user_profile'))

def profile_view(request):
    # anime_list = Anime.objects.all().order_by("-rating")
    fav_ani = None
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        fav_ani = WebUser.objects.get(d_user=user).fav_anime.all()

    return render(request, 'profile.html', {
        # 'anime_list': anime_list,
        'fav_list' : fav_ani
    })