#coding=utf-8

from django.conf.urls import url
from . import views

from tastypie.api import Api
from IOTapp.api.resources import DevicelistResource

device_api = Api(api_name='device')
device_api.register(DevicelistResource())


urlpatterns = [
    url(r'^$', views.switch_index),
    url(r'^home/$', views.get_index, name="home"),
    # url(r'^contacts/$', views.getContacts, name="contacts"),
    # url(r'^cv/$', views.getCV),
    # url(r'^contacts/add/$', views.getAdd),
    url(r'^accounts/login/$', views.get_login),
    url(r'^accounts/sign-up/$', views.get_sign_up),

    # url(r'^accounts/login/$', views.get_login),
    url(r'^account/logout/$', views.get_logout),
    # url(r'^contacts/delete/$', views.delete),
    # url(r'^contacts/edit/$', views.edit),
    # url(r'^contacts/find/$', views.find)

    url(r'^api/', include(device_api.urls)),
]