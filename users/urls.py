from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reg/', views.SignUpView.as_view(), name='signup'),
    path('toggle_group/<str:group_name>', views.toggle_group, name='toggle_group'),
]
