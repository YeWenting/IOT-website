#coding=utf-8

from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.switch_index),
    url(r'^devices/$', views.get_index, name="home"),
    # url(r'^contacts/$', views.getContacts, name="contacts"),
    # url(r'^cv/$', views.getCV),
    # url(r'^contacts/add/$', views.getAdd),
    url(r'^accounts/login/$', views.get_login),
    url(r'^accounts/sign-up/$', views.get_sign_up),

    # url(r'^accounts/login/$', views.get_login),
    url(r'^accounts/logout/$', views.get_logout),
    # url(r'^contacts/delete/$', views.delete),
    # url(r'^contacts/edit/$', views.edit),
    # url(r'^contacts/find/$', views.find)
    url(r'^api/getlist/', views.get_list),
    # url(r'^getform/$', views.get_form),
    url(r'^devices/add/$', views.add_device),
    url(r'^devices/update/$', views.update_device),
    url(r'^devices/delete/$', views.delete_device),
    url(r'^devices/history/$', views.get_history),
    url(r'^api/addlog/$', views.add_log),
    url(r'^api/getlog/$', views.get_log),
    url(r'^api/get_warning_log/$', views.get_warning_log),
    url(r'^devices/warn/$', views.get_warn_index)
]