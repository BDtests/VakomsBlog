from django.db import models
from blog.models import Blog
from authentication.models import CustomUser


class Post(models.Model):

    title = models.CharField(max_length=300)
    content = models.CharField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @staticmethod
    def create(title, content, author, blog):
        post = Post(title=title, content=content, author=author, blog=blog)
        post.save()
        return post

    @staticmethod
    def get_all_posts(blog):
        posts = Post.objects.filter(blog=blog)
        return posts

    @staticmethod
    def get_by_id(post_id):
        post = Post.objects.get(id=post_id)
        return post

    @staticmethod
    def delete_post_by_id(post_id):
        post = Post.get_by_id(post_id)
        post.delete()