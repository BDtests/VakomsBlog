from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from authentication.models import CustomUser
from unittest import mock


class TestAuthenticationView(TestCase):

    def setUp(self):
        CustomUser(id=1,
                   first_name='Bohdan',
                   last_name='Dubas',
                   phone='123456789',
                   email='dubas.bogdan@gmail.com',
                   is_active=True).save()

        self.user = CustomUser.objects.get(id=1)
        self.user.set_password('password')
        self.client = Client()

    def test_register_positive(self):
        with mock.patch('authentication.views.send_email') as mock_send_email:
            mock_send_email.return_value = True

            data = {"first_name": "Helen",
                    "last_name": "Demkiv",
                    "email": "dubas.bogdan+1@gmail.com",
                    "phone": "12345",
                    "password": "helendemkiv"}

            url = reverse('authentication:registration')
            response = self.client.post(url, data)

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'authentication/index.html')

    def test_register_negative(self):
        url = reverse('authentication:registration')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/register.html')

    def test_login_user_post_positive(self):
        with mock.patch('authentication.views.authenticate') as mock_auth:
            mock_auth.return_value = self.user

            url = reverse('authentication:login')

            data = {'email': 'dubas.bogdan@gmail.com',
                    'password': 'password'}

            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 302)

    def test_login_user_post_negative(self):
        url = reverse('authentication:login')
        data = {'email': 'wrongemail@gmail.com',
                'password': 'password'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_login_user_get_positive(self):
        url = reverse('authentication:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')

    def test_login_user_negative(self):
        url = reverse('authentication:login')
        response = self.client.put(url)
        self.assertEqual(response.status_code, 400)

    def test_logout_user_positive(self):
        url = reverse('authentication:logout')
        self.client.login(email='dubas.bogdan@gmail.com', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_logout_user_negative(self):
        url = reverse('authentication:logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)

    def test_activate_positive(self):
        CustomUser(id=22,
                   first_name='Helen',
                   last_name='Demkiv',
                   phone='123456789',
                   email='dubas.bogdan+1@gmail.com',
                   is_active=False).save()

        url = reverse('authentication:activate',  kwargs={'token': 'dubas.bogdan+1@gmail.com'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_activate_negative(self):
        url = reverse('authentication:activate', kwargs={'token': 'dubas.bogdan+1@gmail.com'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
