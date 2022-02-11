from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.views import generic

from .models import News


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

    def get_queryset(self):
        return News.objects.filter(create_date__lte=timezone.now())


def create(request):
    return HttpResponse("Hello world. create news")
