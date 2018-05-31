from django.db import models
from authentication.models import CustomUser


class Blog(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @staticmethod
    def create(name, description, author):
        blog = Blog(name=name, description=description, author=author)
        blog.save()
        return blog

    @staticmethod
    def get_by_author(author):
        author_blogs = Blog.objects.filter(author=author).order_by('-created_at')
        return author_blogs

    @staticmethod
    def get_by_name(name):
        blogs = Blog.objects.filter(name__icontains=name)
        return blogs

    @staticmethod
    def get_recent_blogs():
        recent_blogs = Blog.objects.order_by('-created_at')[0:10]
        return recent_blogs

    @staticmethod
    def get_by_id(blog_id):
        blog = Blog.objects.get(id=blog_id)
        return blog

    @staticmethod
    def delete_blog_by_id(blog_id):
        blog = Blog.get_by_id(blog_id)
        blog.delete()
