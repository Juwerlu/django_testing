from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils.timezone import now
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Title',
        text='Text',

    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Text',
    )
    return comment


@pytest.fixture
def news_list():
    return News.objects.bulk_create(
        News(
            title=f'Заголовок {index}',
            text=f'Текст {index}',
            date=datetime.today().date() - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comments_list(author, news):
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text='Comment Text',
        )
        comment.created = now() + timedelta(days=index)
        comment.save()
    return comments_list


@pytest.fixture
def form_data():
    return {'text': 'New Comment Text'}


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def login_reverse():
    return reverse('users:login')


@pytest.fixture
def delete_url(news, comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def edit_url(news, comment):
    return reverse('news:edit', args=(comment.id,))
