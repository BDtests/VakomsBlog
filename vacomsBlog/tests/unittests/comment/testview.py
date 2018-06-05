from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from authentication.models import CustomUser
from unittest import mock
from comment import views


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class TestCommentView(TestCase):
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

    def test_post(self):
        with mock.patch('comment.views.Post') as mock_post:
            with mock.patch('comment.views.Comment') as mock_comment:
                with mock.patch('comment.views.send_email') as mock_email:

                    post = {}
                    author = {'email': 1}
                    post = dotdict(post)
                    post.author = dotdict(author)
                    mock_post.get_by_id.return_value = post

                    comment = {}
                    author = {'first_name': 'Bohdan'}
                    comment = dotdict(comment)
                    comment.author = dotdict(author)
                    mock_comment.create.return_value = comment

                    mock_email.return_value = True

                    url = reverse('comment:create_comment', kwargs={'post_id':1})
                    request = self.factory.post(url, {"key":"value"})
                    request.user = self.user
                    comment_view = views.CommentView()
                    response = comment_view.post(request, 1)
                    self.assertEqual(response.status_code, 302)


    def test_delete_comment(self):
        with mock.patch('comment.views.Comment') as mock_comment:
            comment = {}
            post = {'id': 1}
            comment = dotdict(comment)
            comment.post = dotdict(post)
            mock_comment.get_by_id.return_value = comment
            mock_comment.delete.return_value = True

            url = reverse('comment:delete_comment', kwargs={'comment_id':1})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)