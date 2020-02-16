"""fakeBlockWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from fakeBlockApi.views.api import (FakeNewsDetectorApi, )
from fakeBlockDemo.views.views import (DemoIndex, AboutPage, ApiDocsPage, handler404, handler500)

#TODO: hide admin page
#TODO: turn off debug mode
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DemoIndex.as_view(), name='demo_index_page'),
    path('api/fake', FakeNewsDetectorApi.as_view(), name='api_is_fake_news'),
    path('about/', AboutPage.as_view(), name='about_page'),
    path('api/', ApiDocsPage.as_view(), name='api_docs'),
]

# set custom HTTP error handler pages
handler404 = handler404
handler500 = handler500
