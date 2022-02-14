from django import forms
from django.forms import Textarea

from news.models import News


class NewCommentForm(forms.Form):
    news_id = forms.IntegerField(required=False)
    new_comment = forms.CharField(label='Новый комментарий', max_length=100)
