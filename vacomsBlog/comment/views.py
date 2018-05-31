from .models import Comment
from django.views.generic.base import View
from post.models import Post
from django.http import HttpResponseRedirect
from django.urls import reverse
from utils.send_email import send_email


class CommentView(View):
    def post(self, request, post_id):
        data = request.POST
        post = Post.get_by_id(post_id)
        if data and request.user.is_authenticated:
            comment = Comment.create(content=data.get('content'),
                                     author=request.user,
                                     post=post)
            email_data = {'post': post.title,
                          'commentator': comment.author.first_name}

            subject = 'VakomsBlog New Comment'
            message = 'comment'
            template = 'comment.html'
            recipient = post.author.email
            send_email(subject,
                       message,
                       [recipient, ],
                       template,
                       email_data)
            return HttpResponseRedirect(reverse("post:index", kwargs={'post_id': post_id}))


def delete_comment(request, comment_id):
    if request.method == "GET":
        comment = Comment.get_by_id(comment_id)
        post_id = comment.post.id
        Comment.delete_comment_by_id(comment_id)
        return HttpResponseRedirect(reverse("post:index", kwargs={'post_id': post_id}))
