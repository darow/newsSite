from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView


# Sign Up View
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('news:news_list'))
            else:
                return HttpResponse("НЕ вошли")
        else:
            return HttpResponse("Форма не валидная")

    else:
        context = {
            'form': AuthenticationForm,
        }
        return render(request, 'users/auth.html', context)


# class SignUpView(CreateView):
#     # model = User
#     form_class = SignupForm
#     template_name = 'users/signup.html'
#     success_url = reverse('news:news_list')


# @csrf_protect
# def reg_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(data=request.POST)
#         if form.is_valid():
#             user = form.save()
#             if user is not None:
#                 login(request, user)
#                 return HttpResponse("Вошли")
#             # username = form.cleaned_data['username']
#             # password = form.cleaned_data['password1']
#             # user = User.objects.create_user(username='username', password='password')
#             # user.save()
#             if user is not None:
#                 login(request, user)
#                 return HttpResponse("Вошли")
#             else:
#                 return HttpResponse("НЕ вошли")
#         else:
#             return HttpResponse("Форма не валидная")
#
#     else:
#         context = {
#             'form': UserCreationForm,
#         }
#         return render(request, 'users/signup.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse('news:news_list'))
