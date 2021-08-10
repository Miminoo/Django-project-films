from django.db import models
import datetime
from django.db.models.aggregates import Count
from django.db.models.fields import CharField
from django.http import request
from django.urls.conf import include
from django.contrib.auth.models import User


#--------------* Janr Model *--------------#
class Janr(models.Model):
    name = models.CharField(max_length=100, verbose_name='Жанр')

    def __str__(self):
      return self.name

    class Meta:
      ordering = ['name']
      verbose_name = 'Жанр'
      verbose_name_plural = 'Жанры'

#--------------* FILMS Model *--------------#
class Film(models.Model):
    id_janr = models.ForeignKey(Janr,on_delete=models.CASCADE, verbose_name="Жанр")# ---> Model Janr
    id_user = models.ManyToManyField(User, through='film_to_user')
    name = models.CharField(max_length=100, verbose_name='Название фильма')
    years = models.CharField(max_length=4, verbose_name='Год')
    country = models.CharField(max_length=100, verbose_name='Страна')
    photo = models.ImageField(upload_to ='photos/%Y/%m/%d/', verbose_name='Фото',blank=True)
    created_at = models.DateTimeField(auto_now_add = True, verbose_name='Опубликовано', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Да/Нет?')
    slug = models.CharField(max_length=100, blank=True, verbose_name='slug')
    discription = models.CharField(max_length=300, blank=True, verbose_name='Описание')
    video = models.FileField(upload_to='movie/%Y/%m/%d/',blank=True,verbose_name='Видео',null=True)
    video_poster = models.ImageField(upload_to ='poster/%Y/%m/%d/', verbose_name='Постер',blank=True, null=True)

    @property
    def photoURL(self):
        try:
            url = self.photo.url
        except:
            url = ""
        return url
    
    @property
    def posterURL(self):
        try:
            url = self.video_poster.url
        except:
            url = ""
        return url

    @property
    def videoURL(self):
        try:
            url = self.video.url
        except:
            url = ""
        return url

    def __str__(self):
      return self.name

    class Meta:
      ordering = ['-years','-created_at']
      verbose_name = 'Фильм'
      verbose_name_plural = 'Фильмы'    

class Film_to_user(models.Model):
  id_film = models.ForeignKey(Film,on_delete=models.CASCADE)
  id_user = models.ForeignKey(User,on_delete=models.CASCADE)

  def __str__(self):
          return ('{}'.format(self.id_film))

  class Meta:
      ordering = ['id_film']
      verbose_name = 'Фильм пользователя'
      verbose_name_plural = 'Фильмы пользователя'

#--------------* Rejicer Model *--------------#
class Rejicer(models.Model):
    fullName = models.CharField(max_length=300, verbose_name='Имя')
    birthday_date = models.DateField(blank=True, verbose_name='Дата рождения')
    growth = models.CharField(max_length=100, verbose_name="Рост",null=True)
    birthday_place = models.CharField(max_length=100, verbose_name="Место рождения",null=True)
    picture = models.ImageField(upload_to ='rejicer/%Y/%m/%d/', verbose_name='Режисёр',blank=True)
    fr = models.ManyToManyField(Film,through='film_to_rejicer')

    def __str__(self):
      return self.fullName

    class Meta:
      ordering = ['fullName']
      verbose_name = 'Режисер'
      verbose_name_plural = 'Режисеры'

class Film_to_rejicer(models.Model):
    id_film = models.ForeignKey(Film, on_delete=models.CASCADE)
    id_rejicer = models.ForeignKey(Rejicer, on_delete=models.CASCADE)

    def __str__(self):
          return (
            'Фильм: {}, режиссёр {}.'.format(self.id_film,self.id_rejicer)
          )
    class Meta:
      ordering = ['id_film']
      verbose_name = 'Режиссёр фильма'
      verbose_name_plural = 'Режисcёры фильма'

#--------------* Actor Model *--------------#
class Actor(models.Model):
    fullName = models.CharField(max_length=300, verbose_name='Имя')
    birthday_date = models.DateField(blank=True, verbose_name='Дата рождения')
    growth = models.CharField(max_length=100, verbose_name="Рост",null=True)
    birthday_place = models.CharField(max_length=100, verbose_name="Место рождения",null=True)
    picture = models.ImageField(upload_to ='actor/%Y/%m/%d/', verbose_name='Актёр',blank=True)
    id_filma = models.ManyToManyField(Film, through='film_to_actor')

    def __str__(self):
      return self.fullName

    class Meta:
      ordering = ['fullName']
      verbose_name = 'Актер'
      verbose_name_plural = 'Актеры'

class Film_to_actor(models.Model):
    id_film = models.ForeignKey(Film, on_delete=models.CASCADE)
    id_actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    def __str__(self):
          return (
            '{}'.format(self.id_film)
          )

    class Meta:
      ordering = ['id_film']
      verbose_name = 'Актёр фильма'
      verbose_name_plural = 'Актёры фильма'

    

