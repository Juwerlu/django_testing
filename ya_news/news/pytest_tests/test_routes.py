from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'name, comment_object',
    (
        ('news:edit', pytest.lazy_fixture('comment')),
        ('news:delete', pytest.lazy_fixture('comment')),
    )
)
def test_redirects(client, name, comment_object):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment_object.id,))
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


@pytest.mark.parametrize(
    'client, name, status, args',
    (
        (pytest.lazy_fixture('anonym_client'), 'news:home',
         HTTPStatus.OK, None),
        (pytest.lazy_fixture('anonym_client'), 'news:detail',
         HTTPStatus.OK, pytest.lazy_fixture('id_news_for_args')),
        (pytest.lazy_fixture('anonym_client'), 'users:login',
         HTTPStatus.OK, None),
        (pytest.lazy_fixture('anonym_client'), 'users:logout',
         HTTPStatus.OK, None),
        (pytest.lazy_fixture('anonym_client'), 'users:signup',
         HTTPStatus.OK, None),
        (pytest.lazy_fixture('not_author_client'), 'news:edit',
         HTTPStatus.NOT_FOUND, pytest.lazy_fixture('id_comment_for_args')),
        (pytest.lazy_fixture('not_author_client'), 'news:delete',
         HTTPStatus.NOT_FOUND, pytest.lazy_fixture('id_comment_for_args')),
        (pytest.lazy_fixture('author_client'), 'news:edit',
         HTTPStatus.OK, pytest.lazy_fixture('id_comment_for_args')),
        (pytest.lazy_fixture('author_client'), 'news:delete',
         HTTPStatus.OK, pytest.lazy_fixture('id_comment_for_args')),
    )
)
def test_home_availability_for_users(client, name, status, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == status
