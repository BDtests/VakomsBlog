from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from authentication.models import CustomUser
from unittest import mock
from home import views


class TestHomeView(TestCase):
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
        self.factory = RequestFactory()

    def test_index_positive(self):
        url = reverse('home:index')
        request = self.factory.get(url)
        request.user = self.user
        response = views.index(request)

        self.assertEqual(response.status_code, 200)

    def test_index_negative(self):
        url = reverse('home:index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/index.html')

    def test_my_blogs(self):

        with mock.patch('home.views.Blog') as mock_blog:
            mock_blog.get_by_author.return_value = True
            url = reverse('home:my_blogs')
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'home/my_blogs.html')

    def test_user_blogs_positive(self):
        with mock.patch ('home.views.CustomUser') as mock_user:
            with mock.patch('home.views.Blog') as mock_blog:
                mock_user.get_by_email.return_value = True
                mock_blog.get_by_author.return_value = True

                data = {'email':'dubas.bogdan@gmail.com'}
                url = reverse('home:user_blogs')
                response = self.client.get(url, data)

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'home/my_blogs.html')

    def test_user_blogs_negative(self):
        with mock.patch('home.views.CustomUser') as mock_user:
            mock_user.get_by_email.return_value = False

            data = {'email': 'dubas.bogdan@gmail.com'}
            url = reverse('home:user_blogs')
            response = self.client.get(url, data)

            self.assertEqual(response.status_code, 302)

    def test_find_blog_positive(self):
        with mock.patch('home.views.Blog') as mock_blog:
            mock_blog.get_by_name.return_value = True
            url = reverse('home:find_blog')
            data = {'blog_name': 'anything'}

            response = self.client.get(url, data)

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'home/my_blogs.html')

    def test_find_blog_negative(self):
        with mock.patch('home.views.Blog') as mock_blog:
            mock_blog.get_by_name.return_value = False
            url = reverse('home:find_blog')
            data = {'blog_name': 'anything'}

            response = self.client.get(url, data)

            self.assertEqual(response.status_code, 302)
