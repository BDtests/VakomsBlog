from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^registration/$', views.register, name='registration'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^activate/(?P<token>.+)$', views.activate, name='activate'),
]
