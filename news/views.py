from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import News, Comment
from .forms import NewCommentForm


def new_comment_view(request):
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            news_id = form.cleaned_data['news_id']
            text = form.cleaned_data['new_comment']
            Comment.objects.create(text=text, news_id=news_id)
            return redirect(reverse('news:detail', args=(news_id,)))
            # return render(request, 'news/thanks.html', {'text': text})
        else:
            return HttpResponse("form is not valid")

    else:
        return HttpResponse("Get?")
    return HttpResponse("fail")


# def index(request):
#     latest_news_list = News.objects.order_by('-create_date')[:5]
#     template = loader.get_template('news/index.html')
#     context = {
#         'latest_news_list': latest_news_list,
#     }
#     # output = ', '.join([q.title for q in latest_news_list])
#     return HttpResponse(template.render(context, request))


class IndexView(generic.ListView):
    paginate_by = 5
    template_name = 'news/index.html'
    # context_object_name = 'news_list'

    def get_queryset(self):
        return News.objects.filter(create_date__lte=timezone.now()).order_by('-create_date')


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


def create(request):
    return HttpResponse("Hello world. create news")
