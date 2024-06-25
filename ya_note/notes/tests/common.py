from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

AUTHOR = 'Автор'
READER = 'Читатель'
ANONYM = 'Аноним'
TITLE = 'Test Title'
TITLE_EDIT = 'Edit Title'
TEXT = 'Test Text'
TEXT_EDIT = 'Edit Text'
SLUG = 'note_slug'
NEW_SLUG = 'new_slug'

User = get_user_model()


class LogicFixture(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.reader = User.objects.create(username=READER)
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.reader)
        cls.form_data = {'title': TITLE,
                         'text': TEXT}
        cls.url = reverse('notes:add', args=None)


class RoutesFixture(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username=AUTHOR)
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username=READER)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.anonym_client = Client()
        cls.note = Note.objects.create(
            title=TITLE,
            text=TEXT,
            author=cls.author,
            slug=SLUG
        )


class UserInteractionLogicFixture(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.author = User.objects.create(username=AUTHOR)
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username=READER)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title=TITLE,
            text=TEXT,
            author=cls.author,
        )
        cls.note_url = reverse('notes:success', args=None)
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.form_data = {
            'text': TEXT_EDIT,
            'title': TITLE_EDIT
        }
