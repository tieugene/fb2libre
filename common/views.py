# -*- coding: utf-8 -*-
'''
core.views
'''

# 1. django
#from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext, Context, loader
from django.db import transaction

# 2. system
import os, zipfile

# 4. my
import models, forms

PAGE_SIZE = 25

class   LangList(ListView):
        model = models.Lang
        paginate_by = PAGE_SIZE

class   LangDetail(DetailView):
        model = models.Lang

class   SeriesList(ListView):
        model = models.Series
        paginate_by = PAGE_SIZE

class   SeriesDetail(DetailView):
        model = models.Series

class   GenreList(ListView):
        model = models.Genre
        paginate_by = PAGE_SIZE

class   GenreDetail(DetailView):
        model = models.Genre

class   AuthorList(ListView):
        model = models.Author
        paginate_by = PAGE_SIZE

class   AuthorDetail(DetailView):
        model = models.Author

class	BookList(ListView):
	model = models.Book
	#template_name = 'core/book_list.html'
	paginate_by = PAGE_SIZE

class	BookDetail(DetailView):
	model = models.Book
	#template_name = 'core/book_view.html'

def	book_get(request, pk):
	book = models.Book.objects.get(pk=int(pk))
	z_path = os.path.join(book.arch.lib.arch, "%s.zip" % book.arch.fname)
	z = zipfile.ZipFile(z_path, 'r')
	fb2_name = "%d.fb2" % book.fname
	response = HttpResponse(content_type='application/x-fictionbook')	# application/x-fictionbook+xml
	response['Content-Transfer-Encoding'] = 'binary'
	response['Content-Disposition'] = '; filename=\"%s\"' % fb2_name
	fb2 = z.open(fb2_name)
	response.write(fb2.read())
	return response

def	book_html(request, pk):
	pass
