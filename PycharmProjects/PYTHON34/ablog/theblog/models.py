from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, datetime, timedelta
from django.contrib import admin
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # перемещение пользователя после добавление нового поста
        return reverse('home')


class Post(models.Model):
    title = models.CharField(max_length=120)
    title_tag = models.CharField(max_length=120, default="It балаган")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    post_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=120, default='coding')
    likes = models.ManyToManyField(User, related_name='blog_post')

    def total_likes(self):
        return self.likes.count() # считаем лайки

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        # перемещение пользователя после добавление нового поста
        return reverse('home')

    def was_published_recently(self):
        return self.post_date >= timezone.now() - datetime.timedelta(days=1)

class Comment(models.Model):
    article = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_name = models.CharField('имя автора', max_length=40)
    comment_text = models.CharField(max_length=350)

    def __str__(self):
        return f'{str(self.article)}'
    