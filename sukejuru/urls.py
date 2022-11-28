"""sukejuru URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sekujuru_app import views as app_views
from user import views as user_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin/logout", app_views.logout_view, name='admin_logout'),
    path("", app_views.index, name="index"),
    path('register', app_views.register_view, name='register'),
    path('login', app_views.login_view, name='login'),
    path('logout', app_views.logout_view, name='logout'),
    path('home', app_views.home_view, name='home'),
    path('calender', app_views.calender_view, name='calender'),
    path('about', app_views.about_view, name='about'),
    path('search', app_views.search_view, name='search'),
    path('rate', app_views.rate_anime, name='rate'),
    path('favorite', app_views.do_favorite, name='favorite'),
    path('remove_favorite', app_views.remove_favorite, name='remove_favorite'),
    path('profile_redirect', user_views.profile_redirect, name='profile_redirect'),
    path('user_profile', user_views.profile_view, name='user_profile'),
    path('home/<int:id>', app_views.anime_page, name='anime_page'),
]
