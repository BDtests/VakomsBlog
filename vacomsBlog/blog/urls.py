from django.conf.urls import url
from .views import BlogView, CreateBlogView, delete_blog


urlpatterns = [
    url(r'^(?P<blog_id>\d+)/$', BlogView.as_view(), name='index'),
    url(r'^create_blog/$', CreateBlogView.as_view(), name='create_blog'),
    url(r'^delete_blog/(?P<blog_id>\d+)/$', delete_blog, name='delete_blog'),
]
