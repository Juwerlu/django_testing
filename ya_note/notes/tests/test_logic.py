from http import HTTPStatus

from django.template.defaultfilters import slugify
from django.urls import reverse
from notes.forms import WARNING
from notes.models import Note
from notes.tests.overall import LogicFixture, UserInteractionLogicFixture


class TestLogic(LogicFixture):

    def data_create(self, note_list=None):
        if note_list is None:
            self.client.force_login(self.author)
            response = self.client.post(self.url, data=self.form_data)
            self.assertRedirects(response, reverse('notes:success'))
        else:
            for item in note_list:
                self.form_data.pop(item)
            self.client.force_login(self.author)
            response = self.client.post(self.url, data=self.form_data)
            self.assertRedirects(response, reverse('notes:success'))

    def test_anonymus_notes_create(self):
        current_notes_count = Note.objects.count()
        self.client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, current_notes_count)

    def test_login_user_notes_create(self):
        self.data_create()
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_same_slug(self):
        self.data_create()
        response = self.client.post(self.url, data=self.form_data)
        slug = self.form_data['slug']
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=f'{slug}{WARNING}',

        )

    def test_slug_autho_create(self):
        self.data_create(pop_list=['slug'])
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)


class TestUserInteractionLogic(UserInteractionLogicFixture):

    def test_author_edit(self):
        self.client.force_login(self.author)
        url = reverse('notes:edit', args=(self.author_note.slug,))
        response = self.client.post(url, data=self.form_data)
        self.assertRedirects(
            response, reverse('notes:success'))
        self.author_note.refresh_from_db()
        self.assertEqual(self.author_note.title,
                         self.form_data['title'])
        self.assertEqual(self.author_note.text,
                         self.form_data['text'])

    def test_not_author_edit(self):
        self.client.force_login(self.author)
        url = reverse('notes:edit', args=(self.reader_note.slug,))
        response = self.client.post(url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.reader_note.refresh_from_db()
        self.assertNotEqual(self.reader_note.title,
                            self.form_data['title'])
        self.assertNotEqual(self.reader_note.text,
                            self.form_data['text'])

    def test_author_delete(self):
        self.client.force_login(self.author)
        url = reverse('notes:delete', args=(self.author_note.slug,))
        response = self.client.post(url)
        self.assertRedirects(
            response, reverse('notes:success'))
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)

    def test_not_author_delete(self):
        self.client.force_login(self.author)
        url = reverse('notes:delete', args=(self.reader_note.slug,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 2)
