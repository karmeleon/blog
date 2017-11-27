from django.conf import settings
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^p/(?P<title>[-a-z]+)$', views.post, name='post'),
    url(r'^p/(?P<title>[-a-z]+)/amp$', views.amp_post, name='amp_post'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns