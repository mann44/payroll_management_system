from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="login"),
    url(r'^employee-record$', views.listing, name="listing"),
    url(r'^employee-add$', views.add, name="add"),
    url(r'^delete/(?P<id>\w{0,50})/$', views.delete, name="delete"),
]	
