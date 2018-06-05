from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from authentication.models import CustomUser
from blog.models import Blog
from unittest import mock
from blog.views import CreateBlogView


class TestBlogView(TestCase):
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

    def test_BlogView_get_positive(self):
        with mock.patch('blog.views.Blog') as mock_blog:
            with mock.patch('blog.views.Post') as mock_post:
                mock_blog.get_by_id.return_value = True
                mock_post.get_all_posts.return_value = True

                url = reverse('blog:index', kwargs={'blog_id':1})
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'blog/index.html')

    def test_BlogView_get_negative(self):
        with mock.patch('blog.views.Blog') as mock_blog:
            with mock.patch('blog.views.Post') as mock_post:
                mock_blog.get_by_id.return_value = False
                mock_post.get_all_posts.return_value = False

                url = reverse('blog:index', kwargs={'blog_id':22})
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)

    def test_CreateBlogView_get(self):
        url = reverse('blog:create_blog')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_form.html')

    def test_CreateBlogView_post_positive(self):
        url = reverse('blog:create_blog')
        data = {"name": "some blog",
                "description": "testing some blog"
                }
        request = self.factory.post(url, data)
        request.user = self.user
        create_blog_view = CreateBlogView()
        response = create_blog_view.post(request)

        self.assertEqual(response.status_code, 302)

    def test_delete_blog(self):
        with mock.patch('blog.views.Blog') as mock_blog:
            mock_blog.delete_blog_by_id.return_value = True
            url = reverse('blog:delete_blog', kwargs={'blog_id': 22})
            response = self.client.get(url)

            self.assertEqual(response.status_code, 302)
