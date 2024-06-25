from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


def test_autorised_user_create_comments(author_client, author,
                                        form_data, detail_url, news):
    comments_count = Comment.objects.count()
    response = author_client.post(detail_url, data=form_data)
    assertRedirects(response, detail_url + '#comments')
    assert Comment.objects.count() == comments_count + 1
    new_comment = Comment.objects.all().last()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author
    assert new_comment.news == news


def test_not_autorised_user_create_comments(client, form_data,
                                            detail_url, login_reverse):
    actual_count = Comment.objects.count()
    response = client.post(detail_url, data=form_data)
    login_url = login_reverse
    expected_url = f'{login_url}?next={detail_url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == actual_count


def test_comment_bad_words_acsess(author_client, detail_url):
    comments_count = Comment.objects.count()
    bad_data = {
        'text': f'Коментарий содержащий слово - {BAD_WORDS[0]}!!!'}
    response = author_client.post(detail_url, data=bad_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == comments_count


def test_author_comment_edit(author_client, author, news,
                             form_data, comment, edit_url, detail_url):
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(response, detail_url + '#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']
    assert comment.author == author
    assert comment.news == news


def test_author_comment_delete(author_client, detail_url, delete_url, comment):
    response = author_client.delete(delete_url)
    assertRedirects(response, detail_url + '#comments')
    comment = Comment.objects.filter(id=comment.id)
    assert not comment.exists()


def test_not_author_comment_delete(not_author_client, delete_url, comment):
    response = not_author_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment = Comment.objects.filter(id=comment.id)
    assert comment.exists()


def test_not_author_comment_edit(not_author_client, author, news,
                                 form_data, comment, edit_url):
    actual_count = Comment.objects.count()
    response = not_author_client.post(edit_url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_text_old = comment.text
    comment.refresh_from_db()
    assert Comment.objects.count() == actual_count
    assert comment.text == comment_text_old
    assert comment.author == author
    assert comment.news == news
