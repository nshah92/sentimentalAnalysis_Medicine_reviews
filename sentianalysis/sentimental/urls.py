from django.conf.urls import url

from sentimental.src import home, drugdetails, index

urlpatterns = [
    url(r'^$', index.index, name="index"),
    url(r'^search/$', home.graph, name="search"),
    url(r'^drugdetail/$', drugdetails.drugdetail, name="drugdetail"),

]