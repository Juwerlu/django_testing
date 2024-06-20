from http import HTTPStatus

import pytest
from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from pytest_django.asserts import assertFormError, assertRedirects

pytestmark = pytest.mark.django_db


def test_autorised_user_create_comments(not_author_client,
                                        form_data, detail_url):
    url = detail_url
    actual_count = Comment.objects.count()
    response = not_author_client.post(url, data=form_data)
    assertRedirects(response, detail_url + '#comments')
    assert Comment.objects.count() == actual_count + 1


def test_not_autorised_user_create_comments(client, form_data,
                                            detail_url, login_reverse):
    url = detail_url
    actual_count = Comment.objects.count()
    response = client.post(url, data=form_data)
    login_url = login_reverse
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == actual_count


def test_comment_bad_words_acsess(author_client, detail_url):
    url = detail_url
    bad_data = {
        'text': f'Коментарий содержащий слово - {BAD_WORDS[0]}!!!'}
    response = author_client.post(url, data=bad_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING

    )


def test_author_comment_edit(author_client,
                             form_data, comment, edit_url, detail_url):
    url = edit_url
    actual_count = Comment.objects.count()
    response = author_client.post(url, data=form_data)
    assertRedirects(response, detail_url + '#comments')
    comment.refresh_from_db()
    assert Comment.objects.count() == actual_count
    assert comment.text == form_data['text']


def test_author_comment_delete(author_client, detail_url, delete_url):
    url = delete_url
    actual_count = Comment.objects.count()
    response = author_client.delete(url)
    assertRedirects(response, detail_url + '#comments')
    comments_count = Comment.objects.count()
    assert comments_count == actual_count - 1


def test_not_author_comment_delete(not_author_client, delete_url):
    url = delete_url
    actual_count = Comment.objects.count()
    response = not_author_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == actual_count


def test_not_author_comment_edit(not_author_client,
                                 form_data, comment, edit_url):
    url = edit_url
    actual_count = Comment.objects.count()
    response = not_author_client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert Comment.objects.count() == actual_count
    assert comment.text != form_data['text']
