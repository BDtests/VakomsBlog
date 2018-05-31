from django.shortcuts import render
from blog.models import Blog
from blog.models import CustomUser
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            recent_blogs = Blog.get_recent_blogs()
            return render(request, 'home/index.html', {'recent_blogs':recent_blogs})
        else:
            return render(request, 'authentication/index.html')
    else:
        return RESPONSE_403_ACCESS_DENIED


def my_blogs(request):
    if request.method == "GET":
        user = request.user
        if user:
            user_blogs = Blog.get_by_author(user)
            return render(request, 'home/my_blogs.html', {'user_blogs':user_blogs})


def user_blogs(request):
    if request.method == "GET":
        user_email = request.GET.get('user_email')
        user = CustomUser.get_by_email(user_email)
        if user:
            user_blogs = Blog.get_by_author(user)
            return render(request, 'home/my_blogs.html', {'user_blogs':user_blogs})
        else:
            return HttpResponseRedirect(reverse("home:index"))
    return HttpResponseRedirect(reverse("home:index"))


def find_blog(request):
    print("WAS HERE")
    if request.method == "GET":
        blog_name = request.GET.get('blog_name')
        print("BLOG", blog_name)
        user_blogs = Blog.get_by_name(blog_name)
        print("USER BLOGS", user_blogs)
        if user_blogs:
            return render(request, 'home/my_blogs.html', {'user_blogs':user_blogs})
        else:
            return HttpResponseRedirect(reverse("home:index"))
    return HttpResponseRedirect(reverse("home:index"))