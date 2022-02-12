import datetime

from django.db import models
from django.utils import timezone


class News(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title + ' ' + str(self.create_date)

    class Meta:
        verbose_name_plural = 'news'

    def was_created_recently(self):
        now = timezone.now()
        return now >= self.create_date >= now - datetime.timedelta(days=1)


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
