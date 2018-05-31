from django.conf.urls import url
from .views import CommentView, delete_comment

urlpatterns = [
    url(r'^(?P<post_id>\d+)/$', CommentView.as_view(), name='create_comment'),
    url(r'^delete_comment/(?P<comment_id>\d+)/$', delete_comment, name='delete_comment'),
]
