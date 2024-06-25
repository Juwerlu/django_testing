from http import HTTPStatus

from django.template.defaultfilters import slugify

from notes.models import Note
from notes.tests.common import (
    TEXT,
    TITLE,
    TEXT_EDIT,
    TITLE_EDIT,
    LogicFixture,
)


class TestLogic(LogicFixture):

    def test_anonymus_cant_create_notes(self):
        current_notes_count = Note.objects.count()
        self.anonym_client.post(self.add_url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, current_notes_count)

    def test_login_user_can_create_note(self):
        current_notes_count = Note.objects.count()
        self.reader_client.post(self.add_url, data=self.form_data_edit)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, current_notes_count + 1)
        note = Note.objects.all().last()
        self.assertEqual(note.text, TEXT_EDIT)
        self.assertEqual(note.title, TITLE_EDIT)
        self.assertEqual(note.author, self.reader)

    def test_same_slug(self):
        current_notes_count = Note.objects.count()
        self.reader_client.post(self.add_url, data=self.form_data_edit)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, current_notes_count + 1)
        self.reader_client.post(self.add_url, data=self.form_data_edit)
        notes_count_2 = Note.objects.count()
        self.assertEqual(notes_count_2, current_notes_count + 1)

    def test_slug_autho_create(self):
        current_notes_count = Note.objects.count()
        self.reader_client.post(self.add_url, data=self.form_data_edit)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, current_notes_count + 1)
        new_note = Note.objects.all().last()
        expected_slug = slugify(self.form_data_edit['title'])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_edit(self):
        response = self.author_client.post(self.edit_url,
                                           data=self.form_data_edit)
        self.assertRedirects(response, self.note_url)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title,
                         self.form_data_edit['title'])
        self.assertEqual(self.note.text,
                         self.form_data_edit['text'])
        self.assertEqual(self.note.author, self.author)

    def test_not_author_edit(self):
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, TEXT)
        self.assertEqual(self.note.title, TITLE)
        self.assertEqual(self.note.author, self.author)

    def test_author_delete(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.note_url)
        note = Note.objects.filter(id=self.note.id)
        self.assertFalse(note.exists())

    def test_not_author_delete(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.filter(id=self.note.id)
        self.assertTrue(note.exists())
