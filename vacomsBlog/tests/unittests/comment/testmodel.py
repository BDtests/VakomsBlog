from authentication.models import CustomUser
from blog.models import Blog
from django.test import TestCase
from post.models import Post
from comment.models import Comment
import datetime
from unittest import mock

TEST_DATE = datetime.datetime(2018, 2, 2, 12, 00)

class TestPostModel(TestCase):
    def setUp(self):
        CustomUser(id=1,
                   first_name='Bohdan',
                   last_name='Dubas',
                   phone='123456789',
                   email='dubas.bogdan@gmail.com',
                   is_active=False).save()

        self.user = CustomUser.objects.get(id=1)

        Blog(id=22,
             name='TestName',
             description='TestDescription',
             author=self.user).save()

        self.blog = Blog.objects.get(id=22)

        Post(id=333,
             title='TestPost',
             content='Just testing post',
             author=self.user,
             blog=self.blog).save()

        self.post = Post.objects.get(id=333)

        Comment(id=4444,
                author=self.user,
                post=self.post,
                content='Great post!',
                created_at=TEST_DATE).save()

        self.comment = Comment.objects.get(id=4444)

    def test_create(self):
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_DATE
            test_comment = Comment.create(content='amazing',
                                          author=self.user,
                                          post=self.post)

            self.assertEqual(test_comment.content, 'amazing')
            self.assertEqual(test_comment.author, self.user)
            self.assertEqual(test_comment.post, self.post)
            self.assertEqual(test_comment.created_at, TEST_DATE)

    def test_get_all(self):
        Comment(id=5,
                author=self.user,
                post=self.post,
                content='New Comment').save()
        new_comment = Comment.objects.get(id=5)
        expected_comments = [self.comment, new_comment]
        comments = Comment.get_all(self.post)
        self.assertEqual(list(comments), expected_comments)

    def test_get_by_id(self):
        comment = Comment.get_by_id(4444)
        self.assertEqual(comment, self.comment)

    def test_delete_comment_by_id(self):
        Comment.delete_comment_by_id(4444)
        comments = Comment.objects.all()
        self.assertEqual(len(comments), 0)
