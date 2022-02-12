from django.urls import path
from . import views

app_name = 'news'
urlpatterns = [
    path('', views.IndexView.as_view(), name='news_list'),
    path('create/', views.create, name='create'),
    path('<int:pk>/detail', views.DetailView.as_view(), name='detail'),
    path('new_comment/', views.new_comment_view, name='new_comment')
]
