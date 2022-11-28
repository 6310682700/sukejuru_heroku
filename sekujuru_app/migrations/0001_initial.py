# Generated by Django 4.1.1 on 2022-11-26 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnimePlatform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=99)),
                ('premium', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=99)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=99)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=99)),
            ],
        ),
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('anime_id', models.IntegerField(primary_key=True, serialize=False)),
                ('anime_name', models.CharField(max_length=99)),
                ('anime_image', models.CharField(default='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/640px-Image_not_available.png', max_length=999)),
                ('description', models.CharField(default='-', max_length=999)),
                ('time', models.TimeField()),
                ('rating', models.IntegerField(default=5)),
                ('day', models.ManyToManyField(to='sekujuru_app.day')),
                ('genre', models.ManyToManyField(to='sekujuru_app.genre')),
                ('platform', models.ManyToManyField(default=None, to='sekujuru_app.animeplatform')),
                ('season', models.ManyToManyField(to='sekujuru_app.season')),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episode', models.IntegerField(default=None)),
                ('link', models.CharField(max_length=999)),
                ('anime', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sekujuru_app.anime')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sekujuru_app.animeplatform')),
            ],
            options={
                'unique_together': {('anime', 'platform', 'episode')},
            },
        ),
    ]