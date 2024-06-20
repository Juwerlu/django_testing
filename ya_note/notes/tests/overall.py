
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.models import Note

AUTHOR = 'Автор'
READER = 'Читатель'
TITLE = 'Test Title'
TEXT = 'Test Text'
SLUG = 'note_slug'
NEW_SLUG = 'new_slug'

User = get_user_model()


class LogicFixture(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username=AUTHOR)
        cls.reader = User.objects.create(username=READER)

        cls.form_data = {'title': TITLE,
                         'text': TEXT, 'slug': NEW_SLUG}
        cls.url = reverse('notes:add')


class RoutesFixture(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username=AUTHOR)
        cls.reader = User.objects.create(username=READER)
        cls.note = Note.objects.create(
            title=TITLE,
            text=TEXT,
            author=cls.author,
            slug=SLUG
        )

    def login_user(self, login):
        if login is None:
            return None
        return self.client.force_login(login)


class UserInteractionLogicFixture(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.author = User.objects.create(username=AUTHOR)
        cls.reader = User.objects.create(username=READER)
        cls.author_note = Note.objects.create(
            title=TITLE,
            text=TEXT,
            author=cls.author,
            slug=SLUG
        )
        cls.reader_note = Note.objects.create(
            title=TITLE,
            text=TEXT,
            author=cls.reader,
            slug=NEW_SLUG
        )
        cls.form_data = {'title': 'New ' + TITLE,
                         'text': 'New ' + TEXT}
