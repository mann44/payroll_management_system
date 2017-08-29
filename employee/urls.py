from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="login"),
    url(r'^employee-record$', views.listing, name="listing"),
]	
