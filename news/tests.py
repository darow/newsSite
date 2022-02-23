import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from news.models import News, Comment


def create_news(news_text, days, title="default_title", admitted=True):
    time = timezone.now() + datetime.timedelta(days=days)
    return News.objects.create(title=title, text=news_text, create_date=time, admitted=admitted)


def create_comment(comment_text, news):
    return Comment.objects.create(text=comment_text, news=news)


class NewsDetailViewTest(TestCase):
    def test_one_comment(self):
        news = create_news('test_news', -1)
        comment = create_comment('comment', news)
        response = self.client.get(reverse('news:detail', args=(news.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['comment_list'], [comment])
        print(0)
        print(response.context['comment_list'])

    def test_no_comments(self):
        news = create_news('test_news', -1)
        response = self.client.get(reverse('news:detail', args=(news.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['comment_list'], [])
        print(1)
        print(response.context['comment_list'])

    def test_future_news(self):
        future_news = create_news('future_news', 6)
        response = self.client.get(reverse('news:detail', args=(future_news.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_news(self):
        news = create_news('usualNews', -1)
        response = self.client.get(reverse('news:detail', args=(news.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, news.title)
        self.assertEqual(response.context['news'], news)


class NewsIndexViewTests(TestCase):

    def test_past_news(self):
        news = create_news('past_news', days=-30)
        response = self.client.get(reverse('news:news_list'))
        self.assertQuerysetEqual(
            response.context['news_list'],
            [news],
        )
        print("news", response.context['news_list'])


    def test_no_news(self):
        response = self.client.get(reverse('news:news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No news are available now')
        self.assertQuerysetEqual(response.context['news_list'], [])
        print("nonews", response.context['news_list'])


    def test_future_news(self):
        news = create_news('future_news', days=20)
        response = self.client.get(reverse('news:news_list'))
        self.assertQuerysetEqual(response.context['news_list'], [])

    def test_future_news_and_past_news(self):
        news1 = create_news('future_news', days=5)
        news2 = create_news('past_news', days=-20)
        response = self.client.get(reverse('news:news_list'))
        self.assertQuerysetEqual(response.context['news_list'], [news2])

    def test_two_past_news(self):
        news1 = create_news('past_news', days=-30)
        news2 = create_news('future_news', days=-20)
        response = self.client.get(reverse('news:news_list'))
        self.assertQuerysetEqual(response.context['news_list'], [news2, news1])


class NewsModelTests(TestCase):
    def test_was_published_recently_with_recent_news(self):
        recent_news = News(create_date=timezone.now() - datetime.timedelta(hours=5))
        self.assertIs(recent_news.was_created_recently(), True)

    def test_was_published_recently_with_old_news(self):
        old_news = News(create_date=timezone.now() - datetime.timedelta(days=2))
        self.assertIs(old_news.was_created_recently(), False)

    def test_was_published_recently_with_future_news(self):
        """
        was_published_recently returns True to news whose create_date is in the future
        """
        future_time = timezone.now() + datetime.timedelta(days=30)
        future_news = News(create_date=future_time)
        self.assertIs(future_news.was_created_recently(), False)
