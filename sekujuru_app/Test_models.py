from django.contrib import auth
from django.contrib.auth.models import User
from django.test import TestCase, client
from django.urls import reverse
from user.models import WebUser

from .models import Anime, AnimePlatform, Day, Genre, Season, Episode


class testModel(TestCase):

    def setUp(self):
        User.objects.create(username = "non", password = "ang")
        AnimePlatform.objects.create(name = "phone")
        AnimePlatform.objects.create(name = "netflix")
        Day.objects.create(name = "Monday")
        Day.objects.create(name = "Friday")
        Genre.objects.create(name ="Fantasy")
        Season.objects.create(name = "Winter")
        Anime.objects.create(anime_name ="A", anime_id = "1", time= "09:00", rating = 5)
        Anime.objects.first().day.add(Day.objects.get(id=1))
        Anime.objects.first().day.add(Day.objects.get(id=2))
        Anime.objects.first().genre.set(Genre.objects.all())
        Anime.objects.first().season.set(Season.objects.all())
        Anime.objects.first().platform.add(AnimePlatform.objects.get(id=1))
        Anime.objects.first().platform.add(AnimePlatform.objects.get(id=2))
        WebUser.objects.create(d_user = User.objects.first())
        WebUser.objects.first().fav_anime.set(Anime.objects.all())
    
    def test_anime_platform(self):                                                          # Test which platform anime in
        animes = Anime.objects.first()
        self.assertEqual(animes.platform.get(name = 'phone').name, "phone")

    def test_anime_day(self):                                                                # Test what day anime premiere
        day = Anime.objects.first()
        self.assertEqual(day.day.get(name = 'Monday').name, 'Monday')

    def test_anime_non_day(self):                                                            # Test that anime is not in this day (in this case teusday)
        nonday = Anime.objects.first()
        nonday = list(dict(nonday.day.all().values_list()).values())
        self.assertFalse('Tuesday' in nonday)

    def test_anime_seasons(self):                                                            # Test anime seasons
        seasons = Anime.objects.first()
        self.assertEqual(seasons.season.get(pk = 1).name, 'Winter')

    def test_anime_genre(self):                                                               # Test genre of a anime
        genre = Anime.objects.first()
        self.assertEqual(genre.genre.get(name = 'Fantasy').name, 'Fantasy')

    def test_anime_rating(self):                                                               # Test rating score
        rate = Anime.objects.first()
        self.assertEqual(rate.rating, 5)

    def test_anime_name(self):                                                                  # Test anime name
        animes = Anime.objects.first()
        self.assertEqual(animes.anime_name, "A")
    
    def test_user_have_fav(self):                                                              # Test user have a favorite anime                                                              
        user = WebUser.objects.first()
        self.assertEqual(user.fav_anime.first().anime_name, 'A')
