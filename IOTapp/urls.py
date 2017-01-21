#coding=utf-8

from django.conf.urls import url, include
from . import views


urlpatterns = [
    # Device page URL
    url(r'^$', views.switch_index),
    url(r'^devices/$', views.get_index, name="home"),
    url(r'^api/getlist/', views.get_list),
    url(r'^devices/add/$', views.add_device),
    url(r'^devices/update/$', views.update_device),
    url(r'^devices/delete/$', views.delete_device),

    # User control URL
    url(r'^accounts/login/$', views.get_login),
    url(r'^accounts/sign-up/$', views.get_sign_up),
    url(r'^accounts/logout/$', views.get_logout),
    url(r'^accounts/reset-password/$', views.get_reset_password),

    # Log page URL
    url(r'^devices/history/$', views.get_history),
    url(r'^api/addlog/$', views.add_log),
    url(r'^api/getlog/$', views.get_log),

    # Warning log URL
    url(r'^api/get_warning_log/$', views.get_warning_log),
    url(r'^devices/warn/$', views.get_warn_index),

    # Switch control API
    url(r'^api/close_device/$', views.close_device),
    url(r'^api/open_device/$', views.open_device),

    # 404 URL
    url(r'^', views.get_404)
]