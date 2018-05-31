from django.shortcuts import render
from django.views.generic.base import View
from .models import Post
from utils.responsehelper import (RESPONSE_404_OBJECT_NOT_FOUND)
from comment.models import Comment
from blog.models import Blog
from django.http import HttpResponseRedirect
from django.urls import reverse


class PostView(View):
    """
    Handles get method that returns requested post and its comments.
    """
    def get(self, request, post_id=None):
        if post_id:
            post = Post.get_by_id(post_id)
            comments = Comment.get_all(post)
            if not post:
                return RESPONSE_404_OBJECT_NOT_FOUND
            return render(request, 'post/index.html', {'post':post, 'comments':comments})


class CreatePostView(View):
    """
    Handles get and post methods for Create Post page.
    """

    def get(self, request, blog_id):
        return render(request, "post/post_form.html", {'blog_id':blog_id})

    def post(self, request, blog_id):
        data = request.POST
        blog = Blog.get_by_id(blog_id)
        if data and request.user.is_authenticated and request.user.id == blog.author.id:
            post = Post.create(title=data.get('title'),
                               content=data.get('content'),
                               author=request.user,
                               blog = blog)

            return HttpResponseRedirect(reverse("blog:index", kwargs={'blog_id': blog_id}))


def delete_post(request, post_id):
    if request.method == "GET":
        post = Post.get_by_id(post_id)
        blog_id = post.blog.id
        Post.delete_post_by_id(post_id)
        return HttpResponseRedirect(reverse("blog:index", kwargs={'blog_id': blog_id}))
