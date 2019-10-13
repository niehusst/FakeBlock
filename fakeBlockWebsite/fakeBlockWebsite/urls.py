"""fakeBlockWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from fakeBlockApi.views.views import (ApiIndex, )
from fakeBlockDemo.views.views import demo_index_page #IndexPage

#TODO: hide admin page
#TODO: turn off debug mode
#TODO: don't commit secret code
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', demo_index_page, name='demo_index_page'),
    path('api/', ApiIndex.as_view(), name='api_index_page'),
]
