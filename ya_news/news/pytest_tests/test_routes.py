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
    'client, url, status',
    (
        (pytest.lazy_fixture('anonym_client'), reverse('news:home'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('anonym_client'),
         pytest.lazy_fixture('detail_url'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('anonym_client'), reverse('users:login'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('anonym_client'), reverse('users:logout'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('anonym_client'), reverse('users:signup'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('not_author_client'),
         pytest.lazy_fixture('edit_url'),
         HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('not_author_client'),
         pytest.lazy_fixture('delete_url'),
         HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'),
         pytest.lazy_fixture('edit_url'),
         HTTPStatus.OK),
        (pytest.lazy_fixture('author_client'),
         pytest.lazy_fixture('delete_url'),
         HTTPStatus.OK),
    )
)
def test_home_availability_for_users(client, url, status):
    response = client.get(url)
    assert response.status_code == status
