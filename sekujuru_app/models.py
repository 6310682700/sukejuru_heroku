from django.db import models

# ที่ทำ class platform, genre และ season เพราะจะได้เรียงตามพวกนี้ละก็ใส่ได้หลายอันได้
class AnimePlatform(models.Model):
    name = models.CharField(max_length=99)
    premium = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

class Genre(models.Model):
    name = models.CharField(max_length=99)

    def __str__(self):
        return f'{self.name}'

class Season(models.Model):
    name = models.CharField(max_length=99)

    def __str__(self):
        return f'{self.name}'

class Day(models.Model):
    name = models.CharField(max_length=99)
    
    def __str__(self):
        return f'{self.name}'
    

class Anime(models.Model):
    anime_id = models.IntegerField(primary_key=True)
    anime_name = models.CharField(max_length=99)
    anime_image = models.CharField(max_length=999, default="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/640px-Image_not_available.png")
    description = models.CharField(max_length=999, default="-")
    platform = models.ManyToManyField(AnimePlatform, default=None)
    day = models.ManyToManyField(Day)
    time = models.TimeField()
    genre = models.ManyToManyField(Genre)
    season = models.ManyToManyField(Season)
    rating = models.FloatField(default=5)

    def __str__(self):
        return f'{self.anime_id}: {self.anime_name} {self.time} {self.rating}'

class Episode(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, default=None)
    episode = models.IntegerField(default=None)
    platform = models.ForeignKey(AnimePlatform, on_delete=models.CASCADE)
    link = models.CharField(max_length=999)

    class Meta:
        unique_together = [['anime', 'platform', 'episode']]

    def __str__(self):
        return  f'{self.anime}| Episode {self.episode} {self.platform}'