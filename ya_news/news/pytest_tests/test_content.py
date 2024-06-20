import pytest
from django.conf import settings
from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_per_page(client, news_list, home_url):
    url = home_url
    response = client.get(url)
    object_list = list(response.context['object_list'])
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE
    assert object_list == sorted(
        object_list, key=lambda x: x.date, reverse=True)


def test_comments_sorted(client, comments_list, detail_url):
    url = detail_url
    response = client.get(url)
    news_content = response.context['news']
    all_comments = news_content.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert sorted_timestamps == all_timestamps


@pytest.mark.parametrize(
    'user, answer',
    (
        (pytest.lazy_fixture('not_author_client'), True),
        (pytest.lazy_fixture('client'), False),
    )
)
def test_comment_form_acsess(user, answer, detail_url):
    url = detail_url
    response = user.get(url)
    assert ('form' in response.context) == answer
    if answer is True:
        assert isinstance(response.context['form'], CommentForm)
