from django.shortcuts import render
from django.views.generic.base import View
from .models import Blog
from utils.responsehelper import (RESPONSE_404_OBJECT_NOT_FOUND)
from post.models import Post
from django.http import HttpResponseRedirect
from django.urls import reverse


class BlogView(View):
    def get(self, request, blog_id):
        blog = Blog.get_by_id(blog_id)
        posts = Post.get_all_posts(blog)
        if not blog:
            return RESPONSE_404_OBJECT_NOT_FOUND
        return render(request, 'blog/index.html', {'blog':blog, 'posts':posts})


class CreateBlogView(View):
    def get(self, request):
        return render(request, "blog/blog_form.html")

    def post(self, request):
        data = request.POST
        if data and request.user.is_authenticated:
            blog = Blog.create(name=data.get('name'),
                               description=data.get('description'),
                               author=request.user)
            return HttpResponseRedirect(reverse("home:my_blogs"))


def delete_blog(request, blog_id):
    if request.method == "GET":
        Blog.delete_blog_by_id(blog_id)
        return HttpResponseRedirect(reverse("home:my_blogs"))
