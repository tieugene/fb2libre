# -*- coding: utf-8 -*-
'''
core.models
'''

# 1. django
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db import transaction

# 2. 3rd parties

# 3. system
import os

# 4. local

class	Lang(models.Model):
	'''
	65
	TODO:
	+ename: ISO lang name
	+nname: Native name
	'''
	abbr	= models.CharField(unique=True, null=False, db_index=True, max_length=5, verbose_name=u'Аббр.')
	name	= models.CharField(null=True, blank=True, db_index=True, max_length=16, verbose_name=u'Наименование')

	def     __unicode__(self):
		return self.abbr

	class   Meta:
		ordering                = ('abbr',)
		verbose_name            = u'Язык'
		verbose_name_plural     = u'Языки'

class	Series(models.Model):
	'''
	33k
	'''
	name	= models.CharField(unique=True, null=False, db_index=True, max_length=64, verbose_name=u'Наименование')

	def     __unicode__(self):
		return self.name

	class   Meta:
		ordering                = ('name',)
		verbose_name            = u'Серия'
		verbose_name_plural     = u'Серии'

class	Genre(models.Model):
	'''
	300
	'''
	parent	= models.ForeignKey('self', null=True, blank=True, db_index=True, verbose_name=u'Атэц')
	abbr	= models.CharField(unique=True, null=False, db_index=True, max_length=32, verbose_name=u'Аббр.')
	name	= models.CharField(null=True, blank=True, db_index=True, max_length=64, verbose_name=u'Наименование')

	def     __unicode__(self):
		return self.abbr

	class   Meta:
		ordering                = ('abbr',)
		verbose_name            = u'Жанр'
		verbose_name_plural     = u'Жанры'

class	Author(models.Model):
	'''
	94k
	'''
	name    = models.CharField(unique=True, null=False, db_index=True, max_length=255, verbose_name=u'ФИО')
	#lname	= models.CharField(null=True, blank=True, db_index=True, max_length=64, verbose_name=u'Фамилия')
	#fname	= models.CharField(null=True, blank=True, db_index=True, max_length=64, verbose_name=u'Имя')
	#mname	= models.CharField(null=True, blank=True, db_index=True, max_length=64, verbose_name=u'Отчество')

	def     __unicode__(self):
		return self.name

	class   Meta:
                ordering                = ('name',)
		#ordering                = ('lname', 'fname', 'mname')
		#unique_together		= (('lname', 'fname', 'mname'),)
		verbose_name            = u'Автор'
		verbose_name_plural     = u'Авторы'

class	Lib(models.Model):
	'''
	'''
	abbr	= models.CharField(unique=True, null=False, db_index=True, max_length=4, verbose_name=u'Аббр.')
	name	= models.CharField(unique=True, null=False, db_index=True, max_length=16, verbose_name=u'Наименование')
	inpx	= models.CharField(unique=True, null=False, db_index=True, max_length=255, verbose_name=u'Путь к inpx')
	arch	= models.CharField(unique=True, null=False, db_index=True, max_length=255, verbose_name=u'Путь к архивам')
	bookurl	= models.CharField(unique=True, null=False, db_index=True, max_length=255, verbose_name=u'URL книг')

	def     __unicode__(self):
		return self.name

	class   Meta:
		ordering                = ('name',)
		verbose_name            = u'Библиотека'
		verbose_name_plural     = u'Библиотеки'

class	Arch(models.Model):
	'''
	'''
	lib	= models.ForeignKey(Lib, related_name='+', null=False, blank=False, db_index=True, verbose_name=u'Библиотека')
	fname	= models.CharField(null=False, blank=False, db_index=True, max_length=64, verbose_name=u'Наименование')

	def     __unicode__(self):
		return self.fname

	class   Meta:
		ordering                = ('lib', 'fname')
		verbose_name            = u'Архив'
		verbose_name_plural     = u'Архивы'

class	Book(models.Model):
	'''
	'''
	arch	= models.ForeignKey(Arch, null=False, blank=False, db_index=True, verbose_name=u'Архив')
	authors	= models.ManyToManyField(Author, null=True, blank=True, db_index=True, verbose_name=u'Авторы')
	genres	= models.ManyToManyField(Genre, null=True, blank=True, db_index=True, verbose_name=u'Жанры')
	title	= models.CharField(null=False, blank=False, db_index=True, max_length=255, verbose_name=u'Наименование')
	series	= models.ForeignKey(Series, null=True, blank=True, db_index=True, verbose_name=u'Серия')
	serno	= models.PositiveIntegerField(null=True, blank=True, db_index=True, verbose_name=u'№')
	#fname	= models.CharField(null=False, blank=False, db_index=True, max_length=64, verbose_name=u'Файл')
	fname	= models.PositiveIntegerField(null=False, blank=False, db_index=True, max_length=64, verbose_name=u'№')
	size	= models.PositiveIntegerField(null=False, blank=False, db_index=True, verbose_name=u'Размер')
	deleted	= models.BooleanField(null=False, blank=False, db_index=True, verbose_name=u'Удален')
	pubed	= models.DateField(null=False, blank=False, db_index=True, verbose_name=u'Опубликовано')
	lang	= models.ForeignKey(Lang, null=True, blank=True, db_index=True, verbose_name=u'Язык')
	rate	= models.PositiveIntegerField(null=True, blank=True, db_index=True, verbose_name=u'Рейтинг')

	def     __unicode__(self):
		return self.title

	def	get_absolute_url(self):
		return reverse('book_detail', args=[str(self.id)])

	def	get_lib_url(self):
		return self.arch.lib.bookurl % self.fname

	class   Meta:
		ordering                = ('title',)
		verbose_name            = u'Книга'
		verbose_name_plural     = u'Книги'

# Patch: lib, file_id, str_orig, str_new