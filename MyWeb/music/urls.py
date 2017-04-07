from django.conf.urls import url

from . import views

app_name = 'music'

urlpatterns = [

    # music
    url(r'^$', views.index, name='index'),

    # /music/712/
    url(r'^(?P<album_id>[0-9]+)/$', views.details, name='details'),

    # /music/favourite/
    url(r'^(?P<album_id>[0-9]+)/favourite/$', views.favourite, name='favourite'),
]
