from http import HTTPStatus

from django.urls import reverse
from notes.tests.overall import RoutesFixture


class TestRoutes(RoutesFixture):

    def test_users_availabilities(self):
        urls = (
            ('notes:list', self.reader, HTTPStatus.OK, None),
            ('notes:success', self.reader, HTTPStatus.OK, None),
            ('notes:add', self.reader, HTTPStatus.OK, None),
            ('notes:home', None, HTTPStatus.OK, None),
            ('users:login', None, HTTPStatus.OK, None),
            ('users:logout', None, HTTPStatus.OK, None),
            ('users:signup', None, HTTPStatus.OK, None),
            ('notes:detail', self.author,
             HTTPStatus.OK, (self.note.slug,)),
            ('notes:edit', self.author,
             HTTPStatus.OK, (self.note.slug,)),
            ('notes:delete', self.author,
             HTTPStatus.OK, (self.note.slug,)),
            ('notes:detail', self.reader,
             HTTPStatus.NOT_FOUND, (self.note.slug,)),
            ('notes:edit', self.reader,
             HTTPStatus.NOT_FOUND, (self.note.slug,)),
            ('notes:delete', self.reader,
             HTTPStatus.NOT_FOUND, (self.note.slug,)),
        )
        for name, user, status, args in urls:
            with self.subTest(name=name,
                              msg=f'Адрес {name} работает некоректно'):
                self.login_user(user)
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        urls = (
            ('notes:success', None),
            ('notes:list', None),
            ('notes:add', None),
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name,
                              msg=f'Адрес {name} работает некоректно'):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
