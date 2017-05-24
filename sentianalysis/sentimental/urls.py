from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^search/$', views.graph, name="search"),
    url(r'^drugdetail/$', views.drugdrtail, name="drugdetail"),

]