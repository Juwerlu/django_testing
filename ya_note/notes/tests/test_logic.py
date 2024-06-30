from http import HTTPStatus

from django.template.defaultfilters import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.common import LogicFixture


class TestLogic(LogicFixture):

    def test_anonymus_cant_create_notes(self):
        current_notes_count = Note.objects.count()
        self.anonym_client.post(self.add_url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, current_notes_count)

    def test_login_user_can_create_note(self):
        notes_before = set(Note.objects.all())
        self.reader_client.post(self.add_url, data=self.form_data_edit)
        notes_after = set(Note.objects.all())
        self.assertEqual(len(notes_after - notes_before), 1)
        new_note = (notes_after - notes_before).pop()
        self.assertEqual(new_note.text, self.form_data_edit['text'])
        self.assertEqual(new_note.title, self.form_data_edit['title'])
        self.assertEqual(new_note.author, self.reader)

    def test_same_slug(self):
        current_notes_count = Note.objects.count()
        response = self.reader_client.post(self.add_url,
                                           data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, current_notes_count)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=f'{self.note.slug}{WARNING}',
        )

    def test_slug_autho_create(self):
        notes_before = set(Note.objects.all())
        self.reader_client.post(self.add_url, data=self.form_data_edit)
        notes_after = set(Note.objects.all())
        self.assertEqual(len(notes_after - notes_before), 1)
        new_note = (notes_after - notes_before).pop()
        max_slug_length = new_note._meta.get_field('slug').max_length
        expected_slug = slugify(self.form_data_edit['title'][:max_slug_length])
        self.assertEqual(new_note.slug, expected_slug)

    def test_author_edit(self):
        response = self.author_client.post(self.edit_url,
                                           data=self.form_data_edit)
        self.assertRedirects(response, self.note_url)
        edit_note = Note.objects.get(id=self.note.id)
        self.assertEqual(edit_note.title,
                         self.form_data_edit['title'])
        self.assertEqual(edit_note.text,
                         self.form_data_edit['text'])
        self.assertEqual(edit_note.author, self.author)

    def test_not_author_edit(self):
        response = self.reader_client.post(self.edit_url,
                                           data=self.form_data_edit)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        not_edit_note = Note.objects.get(id=self.note.id)
        self.assertEqual(not_edit_note.text, self.form_data['text'])
        self.assertEqual(not_edit_note.title, self.form_data['title'])
        self.assertEqual(not_edit_note.author, self.author)

    def test_author_delete(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.note_url)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_not_author_delete(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(id=self.note.id).exists())
