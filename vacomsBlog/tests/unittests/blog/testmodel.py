from authentication.models import CustomUser
from blog.models import Blog
from django.test import TestCase
import datetime
from unittest import mock

TEST_DATE = datetime.datetime(2018, 2, 2, 12, 00)


class TestBlogModel(TestCase):

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
             author=self.user,
             created_at=TEST_DATE).save()

        Blog(id=333,
             name='OlderBlog',
             description='Should be last in array',
             author=self.user).save()

        self.blog = Blog.objects.get(id=22)
        self.new_blog = Blog.objects.get(id=333)

    def test_str(self):
        self.assertEqual(self.blog.__str__(), 'TestName')

    def test_create(self):
        with mock.patch('django.utils.timezone.now') as mock_time:
            mock_time.return_value = TEST_DATE
            blog = Blog.create(name='CreateName',
                               description='CreateDescription',
                               author=self.user)
            self.assertEqual(blog.name, 'CreateName')
            self.assertEqual(blog.description, 'CreateDescription')
            self.assertEqual(blog.author, self.user)
            self.assertEqual(blog.created_at, TEST_DATE)

    def test_get_by_author(self):
        test_blogs = [self.new_blog, self.blog]
        blogs = Blog.get_by_author(self.user)
        self.assertListEqual(list(blogs), test_blogs)

    def test_get_by_name(self):
        result = Blog.get_by_name('Tes')
        self.assertSetEqual(set(result), {self.blog})

    def test_get_recent_blogs(self):
        test_blogs = [self.new_blog, self.blog]
        blogs = Blog.get_recent_blogs()
        self.assertListEqual(list(blogs), test_blogs)

    def test_get_by_id(self):
        blog = Blog.get_by_id(22)

        self.assertEqual(blog.id, 22)
        self.assertEqual(blog.name, 'TestName')
        self.assertEqual(blog.description, 'TestDescription')
        self.assertEqual(blog.author, self.user)

    def test_delete_blog_by_id(self):
        Blog.delete_blog_by_id(22)
        blog = Blog.objects.all()
        self.assertEqual(len(blog), 1)