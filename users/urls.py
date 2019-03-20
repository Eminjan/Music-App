#!/usr/bin/env
# -*-coding:utf-8-*-
# @Author  : E🚀M

from django.conf.urls import url
from users import views


urlpatterns = [
    url(r'^',views.IndexView,name="index"),

]
