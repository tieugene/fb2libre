# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *

# 1. inlines
class   ArchInLine(admin.TabularInline):
	model		= Arch
	fields		= ('fname',)
	#extra		= 1

class   BookInLine(admin.TabularInline):
	model		= Book
	fields		= ('title',)

# 2. odmins
class	LangAdmin(admin.ModelAdmin):
	ordering	= ('abbr',)
	list_display	= ('abbr', 'name',)

class	SeriesAdmin(admin.ModelAdmin):
	ordering	= ('name',)
	list_display	= ('name',)

class	GenreAdmin(admin.ModelAdmin):
	# TODO: parent
	ordering	= ('abbr',)
	list_display	= ('abbr', 'name',)

class	AuthorAdmin(admin.ModelAdmin):
	ordering	= ('name',)
	list_display	= ('name',)
	#ordering	= ('lname', 'fname', 'mname')
	#list_display	= ('lname', 'fname', 'mname')

class	LibAdmin(admin.ModelAdmin):
	ordering	= ('abbr', 'name',)
	list_display	= ('abbr', 'name',)
	inlines		= (ArchInLine,)

class	ArchAdmin(admin.ModelAdmin):
	ordering	= ('lib', 'fname')
	list_display	= ('lib', 'fname')
	inlines		= (BookInLine,)

class	BookAdmin(admin.ModelAdmin):
	ordering	= ('title',)
	list_display	= ('title',)
#	inlines		= (BookInLine,)

admin.site.register(Lang,	LangAdmin)
admin.site.register(Series,	SeriesAdmin)
admin.site.register(Genre,	GenreAdmin)
admin.site.register(Author,	AuthorAdmin)
admin.site.register(Lib,	LibAdmin)
admin.site.register(Arch,	ArchAdmin)
admin.site.register(Book,	BookAdmin)
