from http import HTTPStatus

from django.urls import reverse

from notes.tests.common import RoutesFixture


class TestRoutes(RoutesFixture):

    def test_users_availabilities(self):
        urls = (
            ('notes:list', self.reader_client, HTTPStatus.OK, None),
            ('notes:success', self.reader_client, HTTPStatus.OK, None),
            ('notes:add', self.reader_client, HTTPStatus.OK, None),
            ('notes:home', self.anonym_client, HTTPStatus.OK, None),
            ('users:login', self.anonym_client, HTTPStatus.OK, None),
            ('users:logout', self.anonym_client, HTTPStatus.OK, None),
            ('users:signup', self.anonym_client, HTTPStatus.OK, None),
            ('notes:detail', self.author_client,
             HTTPStatus.OK, (self.note.slug,)),
            ('notes:edit', self.author_client,
             HTTPStatus.OK, (self.note.slug,)),
            ('notes:delete', self.author_client,
             HTTPStatus.OK, (self.note.slug,)),
            ('notes:detail', self.reader_client,
             HTTPStatus.NOT_FOUND, (self.note.slug,)),
            ('notes:edit', self.reader_client,
             HTTPStatus.NOT_FOUND, (self.note.slug,)),
            ('notes:delete', self.reader_client,
             HTTPStatus.NOT_FOUND, (self.note.slug,)),
        )
        for name, client, status, args in urls:
            with self.subTest(name=name,
                              msg=f'Адрес {name} работает некоректно'):
                url = reverse(name, args=args)
                response = client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        urls = (
            reverse('notes:success'),
            reverse('notes:list'),
            reverse('notes:add'),
            reverse('notes:detail', args=(self.note.slug,)),
            reverse('notes:edit', args=(self.note.slug,)),
            reverse('notes:delete', args=(self.note.slug,)),
        )
        for url in urls:
            with self.subTest(url=url,
                              msg=f'Адрес {url} работает некоректно'):
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
