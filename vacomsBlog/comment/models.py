from django.db import models
from post.models import Post
from authentication.models import CustomUser


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create(content, author, post):
        comment = Comment(content=content, author=author, post=post)
        comment.save()
        return comment

    @staticmethod
    def get_all(post):
        comments = Comment.objects.filter(post=post).order_by('created_at')
        return comments

    @staticmethod
    def get_by_id(comment_id):
        comment = Comment.objects.get(id=comment_id)
        return comment

    @staticmethod
    def delete_comment_by_id(comment_id):
        comment = Comment.objects.get(id=comment_id)
        comment.delete()