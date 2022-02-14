from django.urls import path
from . import views

app_name = 'news'
urlpatterns = [
    path('', views.IndexView.as_view(), name='news_list'),
    path('my', views.MyNewsListView.as_view(), name='my_news_list'),
    path('moderate_list', views.ModerateNewsListView.as_view(), name='moderate_list'),
    path('admit/<int:pk>', views.admit_view, name='admit'),
    path('admit_comment/<int:pk>', views.admit_comment_view, name='admit_comment'),
    path('create/', views.CreateNews.as_view(), name='create'),
    path('<int:pk>/detail', views.DetailView.as_view(), name='detail'),
    path('new_comment/', views.new_comment_view, name='new_comment')
]
