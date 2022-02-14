from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.generic import CreateView, FormView

from .models import News, Comment
from .forms import NewCommentForm


def new_comment_view(request):
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            news_id = form.cleaned_data['news_id']
            text = form.cleaned_data['new_comment']
            author = None
            if not request.user.is_anonymous:
                author = request.user

            Comment.objects.create(text=text, news_id=news_id, author=author)
            return redirect(reverse('news:detail', args=(news_id,)))
        else:
            return HttpResponse("form is not valid")
    else:
        return HttpResponse("Сюда нельзя запросом не post")


class ModerateNewsListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5
    template_name = 'news/index.html'

    def get_queryset(self):
        return News.objects.filter(create_date__lte=timezone.now()).filter(admitted=False).order_by('-create_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Новости для модерации'
        context['moderate_page'] = True
        return context


class MyNewsListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 5
    template_name = 'news/index.html'

    def get_queryset(self):
        return News.objects.filter(create_date__lte=timezone.now()).filter(author=self.request.user).order_by(
            '-create_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Мои новости'
        return context


class IndexView(generic.ListView):
    paginate_by = 5
    template_name = 'news/index.html'

    def get_queryset(self):
        return News.objects.filter(create_date__lte=timezone.now()).filter(admitted=True).order_by('-create_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Опубликованные новости'
        return context


class DetailView(generic.DetailView):
    model = News
    template_name = 'news/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewCommentForm()
        context['comment_list'] = context['news'].comment_set.order_by('-create_date')
        return context

    def get_queryset(self):
        return News.objects.filter(create_date__lte=timezone.now())


class CreateNews(LoginRequiredMixin, CreateView):
    success_url = reverse_lazy('news:news_list')
    template_name = 'news/create.html'
    model = News
    fields = ['title', 'text', 'photo', 'author']

    def get_form(self, form_class=None):
        form = super().get_form()
        form.fields['author'].required = False
        return form

    def form_valid(self, form):
        news = form.save(commit=False)
        news.author = self.request.user
        print(news)
        return super().form_valid(form)


def admit_view(request, pk):
    news = News.objects.get(pk=pk)
    news.admitted = True
    news.save()
    return redirect(reverse('news:moderate_list'))


def admit_comment_view(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.admitted = True
    comment.save()
    return redirect(request.META.get('HTTP_REFERER'))
