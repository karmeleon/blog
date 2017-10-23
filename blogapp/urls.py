from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^p/(?P<title>[-a-z]+)$', views.post, name='post')
]