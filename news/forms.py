from django import forms


class NewCommentForm(forms.Form):
    news_id = forms.IntegerField(required=False)
    new_comment = forms.CharField(label='Новый комментарий', max_length=100)