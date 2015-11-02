# -*- coding: utf-8 -*-
'''
core.forms
'''

from django import forms

import models

class	BookAddForm(forms.Form):
	file		= forms.FileField(label=u'Файл', required=False)

class	BookEditForm(forms.ModelForm):
	class Meta:
		model = models.Book
