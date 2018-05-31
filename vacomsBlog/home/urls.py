from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^my_blogs/$', views.my_blogs, name='my_blogs'),
    url(r'^find_user/$', views.user_blogs, name='user_blogs'),
    url(r'^find_blog/$', views.find_blog, name='find_blog'),
]