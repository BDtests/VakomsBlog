from authentication.models import CustomUser
from blog.models import Blog
from django.test import TestCase
from post.models import Post


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

    def test_str(self):
        self.assertEqual(self.post.__str__(), 'TestPost')

    def test_create(self):
        test_post = Post.create(title='CreatePostTitle',
                                content='Testing create() blog',
                                author=self.user,
                                blog=self.blog)

        self.assertEqual(test_post.title, 'CreatePostTitle')
        self.assertEqual(test_post.content, 'Testing create() blog')
        self.assertEqual(test_post.author, self.user)
        self.assertEqual(test_post.blog, self.blog)

    def test_get_all_posts(self):
        posts = Post.get_all_posts(self.blog)

        self.assertSetEqual(set(posts), {self.post})

    def test_get_by_id(self):
        test_post = Post.get_by_id(333)
        self.assertEqual(test_post, self.post)

    def test_delete_post_by_id(self):
        Post.delete_post_by_id(333)
        posts = Post.objects.all()
        self.assertEqual(len(posts), 0)