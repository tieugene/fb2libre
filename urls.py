# -*- coding: utf-8 -*-
'''
urls
fb2libre 0.0.1
'''
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/',			include(admin.site.urls)),
	url(r'^admin/jsi18n',		'django.views.i18n.javascript_catalog'), # hack to use admin form widgets
	url(r'^accounts/login/$',	login),
	url(r'^logout$',		logout),
	url(r'^$',			TemplateView.as_view(template_name='index.html'), name='index'),
	url(r'^about$',			TemplateView.as_view(template_name='about.html'), name='about'),
	url(r'^core/',			include('core.urls')),
)
urlpatterns += staticfiles_urlpatterns()
