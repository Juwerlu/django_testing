import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_per_page(client, news_list, home_url):
    response = client.get(home_url)
    object_list = list(response.context['object_list'])
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE
    assert object_list == sorted(
        object_list, key=lambda x: x.date, reverse=True)


def test_comments_sorted(client, comments_list, detail_url):
    response = client.get(detail_url)
    news_content = response.context['news']
    all_comments = news_content.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert sorted_timestamps == all_timestamps


def test_detail_page_contains_form(author_client, detail_url):
    response = author_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_detail_page_contains_form_for_user(anonym_client, detail_url):
    response = anonym_client.get(detail_url)
    assert 'form' not in response.context
