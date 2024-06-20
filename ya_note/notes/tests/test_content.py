from django.urls import reverse
from notes.tests.overall import RoutesFixture


class TestContent(RoutesFixture):

    LIST_URL = reverse('notes:list')

    def test_form(self):
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for name, args in urls:
            self.login_user(self.author)
            response = self.client.get(reverse(name, args=args))
            self.assertIn('form', response.context)

    def test_note_objects(self):
        objects = (
            ((self.author), 1),
            ((self.reader), 0),
        )
        for user, count in objects:
            self.login_user(user)
            response = self.client.get(self.LIST_URL)
            object_list = response.context['object_list']
            notes_count = object_list.count()
            self.assertEqual(notes_count, count)
