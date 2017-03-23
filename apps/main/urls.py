from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^home$', views.index, name='index'),
    url(r'^home/add$', views.add),
    url(r'^home/edit/([0-9]+)/$', views.edit),
    url(r'^home/delete/([0-9]+)$', views.delete),
    url(r'^home/edit/([0-9]+)/update$', views.update)
	]
	
