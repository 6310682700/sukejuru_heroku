from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from sekujuru_app.models import Anime

# สร้าง WebUser object เมื่อมีการ create user
@receiver(post_save, sender=User)
def create_user_picks(sender, instance, created, **kwargs):
    if created:
        WebUser.objects.create(d_user=instance)

# Create your models here.
class WebUser(models.Model):
    fav_anime = models.ManyToManyField(Anime, blank=True, through='Favorite')
    d_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.d_user}: {self.fav_anime}'

# don't know why but if delete it, it will crash
class Favorite(models.Model):
    user = models.ForeignKey(WebUser, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}: {self.anime}'

    class Meta:
        unique_together = [['user', 'anime']]

class UserRating(models.Model):
    user_name = models.ForeignKey(WebUser, on_delete=models.CASCADE)
    anime_name = models.ForeignKey(Anime, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
