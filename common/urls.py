# -*- coding: utf-8 -*-
'''
dasist.core.urls
'''

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

import views

urlpatterns = patterns('core.views',
    url(r'^l/$',		views.LangList.as_view(),     name='lang_list'),
    url(r'^l/(?P<pk>\d+)/$',	views.LangDetail.as_view(),   name='lang_view'),
    url(r'^s/$',                views.SeriesList.as_view(),   name='series_list'),
    url(r'^s/(?P<pk>\d+)/$',    views.SeriesDetail.as_view(), name='series_view'),
    url(r'^g/$',                views.GenreList.as_view(),    name='genre_list'),
    url(r'^g/(?P<pk>\d+)/$',    views.GenreDetail.as_view(),  name='genre_view'),
    url(r'^a/$',                views.AuthorList.as_view(),   name='author_list'),
    url(r'^a/(?P<pk>\d+)/$',    views.AuthorDetail.as_view(), name='author_view'),
    url(r'^b/$',                views.BookList.as_view(),     name='book_list'),
    url(r'^b/(?P<pk>\d+)/$',    views.BookDetail.as_view(),   name='book_view'),
    url(r'^b/(?P<pk>\d+)/g/$',  'book_get'),
    url(r'^b/(?P<pk>\d+)/h/$',  'book_html'),
)
