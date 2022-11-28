from django.http import HttpResponse
from django.shortcuts import render
from audioop import reverse
import datetime
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import *
from .form import NewUserForm
from user.models import WebUser, UserRating
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def index(request):
    return HttpResponseRedirect(reverse('home'))

def register_view(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = NewUserForm()
    return render(request=request, template_name='User/register.html', context={'register_form':form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponseRedirect(reverse('admin:index'))
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('home'))
            # return render(request, 'Home/home.html', {
            #     'message': 'invalid username or password.'
            #     })
    return HttpResponseRedirect(reverse('home'))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def home_view(request):
    anime_list = Anime.objects.all().order_by("-rating")
    fav_ani = None
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        try:
            fav_ani = WebUser.objects.get(d_user=user).fav_anime.all()
        except:
            fav_ani = None

    return render(request, 'Home/home.html', {
        'anime_list': anime_list,
        'fav_list' : fav_ani,
    })


def do_favorite(request):
    if request.method == "POST":
        data = request.POST['data']
        anime = Anime.objects.get(anime_name=data)
        user = WebUser.objects.get(d_user=User.objects.get(username=request.user.username))
        user.fav_anime.add(anime)
        
    return HttpResponseRedirect(reverse('home'))

def remove_favorite(request):
    if request.method == "POST":
        data = request.POST['data']
        anime = Anime.objects.get(anime_name=data)
        user = WebUser.objects.get(d_user=User.objects.get(username=request.user.username))
        user.fav_anime.remove(anime)
        
    return HttpResponseRedirect(reverse('home'))

def rate_anime(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            el_id = request.POST.get('el_id')
            val = request.POST.get('val')
            user = WebUser.objects.get(d_user=request.user)
            anime = Anime.objects.get(anime_name=el_id)
            if len(UserRating.objects.filter(user_name=user, anime_name=anime)) == 0:
                UserRating.objects.create(user_name=user, anime_name=anime)
            obj = UserRating.objects.get(user_name=user, anime_name=anime)
            obj.rating = val
            obj.save()
            rating_list = UserRating.objects.filter(anime_name=anime)
            rating = 0
            for anime_rating in rating_list:
                rating += anime_rating.rating
            anime.rating = rating / len(rating_list)
            anime.save()
            return JsonResponse({'success':'true', 'score': val}, safe=False)
        return JsonResponse({'success':'false'})
    return HttpResponseRedirect(reverse('anime_page'))

def calender_view(request):
    select_day = datetime.datetime.now().strftime("%A")
    anime = Anime.objects.filter(day__name=select_day)
    fav_ani = None
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        try:
            fav_ani = WebUser.objects.get(d_user=user).fav_anime.all()
        except:
            fav_ani = None

    if request.method == "GET":
        request_day = request.GET.get("day")

        if request_day=="All" or request_day==None:
            select_day = datetime.datetime.now().strftime("%A")
            anime = Anime.objects.filter(day__name=select_day)
        else:
            select_day = request_day
            anime = Anime.objects.filter(day__name=request_day)
        
        day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        x = datetime.datetime.today().weekday()
        # anime_today = Anime.objects.filter(time__gte=datetime.datetime.now().strftime("%H:%M:%S")).order_by('time').first()
        anime_today = Anime.objects.filter(day__name=day_of_week[x], time__gte=datetime.datetime.now().strftime("%H:%M:%S")).order_by('time').first()
        
        count = 0
        while anime_today is None:
            if x == 6:
                x = 0
                anime_today = Anime.objects.filter(day__name=day_of_week[x]).order_by('time').first()
            else:
                x += 1
                anime_today = Anime.objects.filter(day__name=day_of_week[x]).order_by('time').first()
            count += 1            

    context = {
        "Anime": anime.order_by('time'),
        "now": datetime.datetime.now(),
        "anime_today": anime_today,
        "day": count,
        "anime_today_time": anime_today.time.strftime("%H,%M,%S"),
        "select_day": select_day,
        'fav_list' : fav_ani,
    }

    return render(request, 'Home/calender.html', context)
        
def about_view(request):
    return render(request, 'Home/about.html', {
    })

def search_view(request):
    fav_ani = None
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        try:
            fav_ani = WebUser.objects.get(d_user=user).fav_anime.all()
        except:
            fav_ani = None

    context = {
        "platform": AnimePlatform.objects.all(),
        "genre": Genre.objects.all(),
        "season": Season.objects.all(),
        'fav_list' : fav_ani,
    }

    if request.method == "GET":
        query = request.GET.get("q")
        platform = request.GET.get("platform")
        genre = request.GET.get("genre")
        season = request.GET.get("season")
        rating = request.GET.get("rating")
        day = request.GET.get("day")

        if query==None:            
            search_result = Anime.objects.all().order_by("-rating")
            context.update({"result": search_result})
        else:
            search_result = Anime.objects.filter(
                Q(anime_name__icontains=query) | Q(description__icontains=query), 
            )

        if platform != "All" and platform != None:
            search_result = search_result.filter(platform__name=platform)

        if genre != "All" and genre != None:
            search_result = search_result.filter(genre__name=genre)

        if season != "All" and season != None:
            search_result = search_result.filter(season__name=season)

        if rating != "All" and rating != None:
            search_result = search_result.filter(rating=int(rating))

        if day != "All" and day != None:
            search_result = search_result.filter(day__name=day)

        context.update({"result": search_result})

    return render(request, 'Home/search.html', context)

def anime_page(request, id):    
    anime = Anime.objects.get(anime_id=id)
    userRating = None
    
    if request.user.is_authenticated:
        if len(UserRating.objects.filter(user_name=WebUser.objects.get(d_user=request.user), anime_name=anime)) == 0:
            userRating = UserRating.objects.create(user_name=WebUser.objects.get(d_user=request.user), anime_name=anime)
        else:
            userRating = UserRating.objects.get(user_name=WebUser.objects.get(d_user=request.user), anime_name=anime)

    # มีกรณีมีตอนในเมะแต่ดันไม่ได้ใส่ platform ไว้ for loop นี้มีไว้เพื่อใส่ platform เข้าไป anime เรื่องนั้น
    for i in AnimePlatform.objects.all():
        ep = Episode.objects.filter(anime_id=id, platform_id=i.id)
        ani_got = AnimePlatform.objects.filter(anime=id, name=i.name)   # ดึงข้อมูลของ platform ทีละอัน
        if ep.exists() and not ani_got.exists():
            temp = AnimePlatform.objects.get(name=i.name)
            anime.platform.add(temp)

    c_platform = None
    episode = None
    if request.method == "GET":
        platform = request.GET.get("platform")        
        try:            
            c_platform = AnimePlatform.objects.get(name=platform)
            episode = Episode.objects.filter(anime_id=id, platform_id=c_platform.id)
        except:
            c_platform = AnimePlatform.objects.all().first()
            episode = Episode.objects.filter(anime_id=id, platform_id=c_platform.id)

    # print(episode.exists())
    # if not episode.exists():
    #     episode = None
    
    anime_platform = AnimePlatform.objects.filter(anime=id)

    context = {
        "anime": anime,
        "platform": anime_platform,
        "current_platform": c_platform,
        "genre": Genre.objects.filter(anime=id),
        "season": Season.objects.filter(anime=id),
        "episode": episode,
        "user_rating": userRating,
    }
    return render(request, 'Home/anime_page.html', context)