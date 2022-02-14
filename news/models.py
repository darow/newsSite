import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class News(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    photo = models.ImageField(upload_to='news', null=True, blank=True)
    create_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, default=None, null=True)
    admitted = models.BooleanField(default=False, verbose_name='Допущено')

    def __str__(self):
        return self.title + ' ' + str(self.create_date)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def was_created_recently(self):
        now = timezone.now()
        return now >= self.create_date >= now - datetime.timedelta(days=1)


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    create_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    admitted = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

