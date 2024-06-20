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
    'user, name, status, args',
    (
        (None, 'news:home', HTTPStatus.OK, None),
        (None, 'news:detail',
         HTTPStatus.OK, pytest.lazy_fixture('news')),
        (None, 'users:login', HTTPStatus.OK, None),
        (None, 'users:logout', HTTPStatus.OK, None),
        (None, 'users:signup', HTTPStatus.OK, None),
        (pytest.lazy_fixture('not_author_client'),
         'news:edit', HTTPStatus.NOT_FOUND, pytest.lazy_fixture('comment')),
        (pytest.lazy_fixture('not_author_client'),
         'news:delete', HTTPStatus.NOT_FOUND, pytest.lazy_fixture('comment')),
        (pytest.lazy_fixture('author_client'),
         'news:edit', HTTPStatus.OK, pytest.lazy_fixture('comment')),
        (pytest.lazy_fixture('author_client'),
         'news:delete', HTTPStatus.OK, pytest.lazy_fixture('comment')),
    )
)
def test_home_availability_for_users(client, user, name, status, args):
    if args is not None:
        url = reverse(name, args=(args.id,))
    else:
        url = reverse(name)
    if user is not None:
        response = user.get(url)
    else:
        response = client.get(url)
    assert response.status_code == status
