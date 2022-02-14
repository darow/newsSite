from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.views.generic import CreateView


def toggle_group(request, group_name):
    group = Group.objects.get(name=str(group_name))
    if group in request.user.groups.all():
        request.user.groups.remove(group)
    else:
        request.user.groups.add(group)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
