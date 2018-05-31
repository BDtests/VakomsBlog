from django.conf.urls import url
from .views import PostView, CreatePostView, delete_post

urlpatterns = [
    url(r'^(?P<post_id>\d+)/$', PostView.as_view(), name='index'),
    url(r'^create_post/(?P<blog_id>\d+)/$', CreatePostView.as_view(), name='create_post'),
    url(r'^delete_post/(?P<post_id>\d+)/$', delete_post, name='delete_post'),
]