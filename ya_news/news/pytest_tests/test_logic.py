from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


def test_autorised_user_create_comments(author_client, author,
                                        detail_url, news):
    comments_before = set(Comment.objects.all())
    form_data = {'text': 'New Comment Text'}
    response = author_client.post(detail_url,
                                  data=form_data)
    comments_after = set(Comment.objects.all())
    assert len(comments_after - comments_before) == 1
    new_comment = (comments_after - comments_before).pop()
    assertRedirects(response, detail_url + '#comments')
    assert new_comment.text == form_data['text']
    assert new_comment.author == author
    assert new_comment.news == news


def test_not_autorised_user_create_comments(client,
                                            detail_url, login_reverse):
    actual_count = Comment.objects.count()
    form_data = {'text': 'New Comment Text'}
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
                             comment, edit_url, detail_url):
    form_data = {'text': 'New Comment Text'}
    response = author_client.post(edit_url, data=form_data)
    assertRedirects(response, detail_url + '#comments')
    edit_comment = Comment.objects.get(id=comment.id)
    assert edit_comment.text == form_data['text']
    assert edit_comment.author == author
    assert edit_comment.news == news


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


def test_not_author_comment_edit(not_author_client,
                                 comment, edit_url):
    actual_count = Comment.objects.count()
    form_data = {'text': 'New Comment Text'}
    response = not_author_client.post(edit_url,
                                      data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == actual_count
    not_edit_comment = Comment.objects.get(id=comment.id)
    assert not_edit_comment.text == comment.text
    assert not_edit_comment.author == comment.author
    assert not_edit_comment.news == comment.news
