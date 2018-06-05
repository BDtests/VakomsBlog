from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from authentication.models import CustomUser
from unittest import mock
from post import views


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class TestPostView(TestCase):
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

    def test_PostView_get_positive(self):
        with mock.patch('post.views.Post') as mock_post:
            with mock.patch('post.views.Comment') as mock_comment:
                mock_post.get_by_id.return_value = True
                mock_comment.get_all.return_value = True
                url = reverse('post:index', kwargs={'post_id': 1})
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'post/index.html')

    def test_PostView_get_negative(self):
        with mock.patch('post.views.Post') as mock_post:
            with mock.patch('post.views.Comment') as mock_comment:
                mock_post.get_by_id.return_value = False
                mock_comment.get_all.return_value = False
                url = reverse('post:index', kwargs={'post_id': 1})
                response = self.client.get(url)

                self.assertEqual(response.status_code, 404)

    def test_CreatePostView_get(self):
        url = reverse('post:create_post', kwargs={'blog_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/post_form.html')

    def test_CreatePostView_post(self):
        with mock.patch('post.views.Blog') as mock_blog:
            with mock.patch('post.views.Post') as mock_post:

                mock_post.create.return_value = True

                author = {'id':1}
                blog = {}
                blog = dotdict(blog)
                blog.author = dotdict(author)

                mock_blog.get_by_id.return_value = blog

                data = {'key':'value'}
                url = reverse('post:create_post', kwargs={'blog_id': 1})

                request = self.factory.post(url, data)
                request.user = self.user
                create_post_view = views.CreatePostView()
                response = create_post_view.post(request, 1)

                self.assertEqual(response.status_code, 302)

    def test_delete_post(self):

        with mock.patch('post.views.Post') as mock_post:

            post = {}
            blog = {'id':1}
            post = dotdict(post)
            post.blog = dotdict(blog)

            mock_post.get_by_id.return_value = post

            url = reverse('post:delete_post', kwargs={'post_id': 1})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
