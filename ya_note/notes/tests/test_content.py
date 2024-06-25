from django.urls import reverse

from notes.forms import NoteForm
from notes.tests.common import RoutesFixture


class TestContent(RoutesFixture):

    LIST_URL = reverse('notes:list')

    def test_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for name, args in urls:
            self.client.force_login(self.author)
            response = self.client.get(reverse(name, args=args))
            self.assertIn('form', response.context)
            self.assertIsInstance(response.context['form'], NoteForm)

    def test_note_objects(self):
        user_status = (
            ((self.author), self.assertIn),
            ((self.reader), self.assertNotIn),
        )
        for user, func in user_status:
            self.client.force_login(user)
            response = self.client.get(self.LIST_URL)
            object_list = response.context['object_list']
            func(self.note, object_list)
