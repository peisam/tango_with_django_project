#!/usr/bin/env python
# coding=utf-8,
from django.conf.urls import patterns,url
from rango import views

urlpatterns = patterns('',
    url(r'^$', views.index,name='index'),
    url(r'^about/$', views.about,name='about'),
    url(r'^add_category/$', views.add_category,name='add_category'),
    url(r'^display_meta/$', views.display_meta, name='display_meta'),
    #url(r'^search/$', views.search, name='search'),
    url(r'^goto/$', views.track_url, name='goto'),
    #url(r'^add_profile', views)
    #url(r'^register/$', views.register, name='register'),
    #url(r'^login/$', views.login, name='login'),
    #url(r'^logout/$', views.logout, name='logout'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),



    )
